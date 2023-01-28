from __future__ import annotations

import asyncio
from collections import defaultdict
from sys import platform
from time import perf_counter_ns
import zlib
from discord_typings import HelloData
from importlib.util import find_spec
from functools import partial
from typing import (
    Any,
    DefaultDict,
    Dict,
    Optional,
    TYPE_CHECKING,
    List,
    Union,
)
from logging import getLogger

import aiohttp
from .rate_limit_handling_tools import GatewayRateLimiter
from ..flags import Intents
from ..presence import Presence
from ..utils import AsyncFunction, OpCode, IdentifyCommand

_ORJSON = find_spec("orjson")


if _ORJSON:
    import orjson as json
else:
    import json  # type: ignore

if TYPE_CHECKING:
    from .client import TokenStore
    from .http import HTTPClient

logger = getLogger("EpikCord.websocket")

class WaitForEvent:
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        opcode: Optional[OpCode] = None,
        timeout: Optional[float] = None,
        check: Optional[AsyncFunction],
    ):
        self.event_name = name
        self.opcode = opcode
        self.timeout = timeout
        self.future: asyncio.Future = asyncio.Future()
        self.check = check


class GatewayEventHandler:
    def __init__(self, client: WebSocketClient):
        self.client = client
        self.wait_for_events: DefaultDict[Union[str, int], List] = defaultdict(list)
        self.event_mapping: Dict[OpCode, AsyncFunction] = {
            OpCode.HELLO: self.hello,
            OpCode.HEARTBEAT: partial(self.heartbeat, forced=True),
        }

    def wait_for(
        self,
        *,
        name: Optional[str] = None,
        opcode: Optional[OpCode] = None,
        check: Optional[AsyncFunction] = None,
        timeout: Optional[float] = None,
    ):
        if not name and not opcode:
            raise ValueError("Either name or opcode must be provided.")
        elif name and opcode:
            raise ValueError("Only name or opcode can be provided.")

        event = WaitForEvent(name=name, opcode=opcode, timeout=timeout, check=check)

        if name:
            self.wait_for_events[name].append(event)
        elif opcode:
            self.wait_for_events[opcode.value].append(event)

        return asyncio.wait_for(event.future, timeout=timeout)

    async def send_json(self, payload: Any):
        if not self.client.ws:
            logger.error("Tried to send a payload without a websocket connection.")
            return
        await self.client.rate_limiter.tick()
        logger.debug("Sending %s to Gateway", payload)
        await self.client.ws.send_json(payload)

    async def identify(self):
        payload: IdentifyCommand = {
            "op": OpCode.IDENTIFY,
            "d": {
                "token": self.client.token.value,
                "intents": self.client.intents.value,
                "properties": {
                    "os": platform,
                    "browser": "EpikCord.py",
                    "device": "EpikCord.py",
                },
                "compress": True,
                "large_threshold": 50,
            },
        }

        if self.client.presence:
            payload["d"]["presence"] = self.client.presence.to_dict()

        await self.send_json(payload)

    async def hello(self, data: HelloData):
        """Handle the hello event. OpCode 10."""
        self.client.heartbeat_interval = data["heartbeat_interval"] / 1000
        await self.identify()

        async def heartbeat_task():
            while True:
                await self.heartbeat()

        asyncio.create_task(heartbeat_task())

    async def heartbeat(self, *, forced: Optional[bool] = False):
        """Send a heartbeat to the gateway.

        Parameters
        ----------
        forced : Optional[bool]
            Whether or not to send the heartbeat now.
        """

        if not self.client.heartbeat_interval:
            logger.error("Tried to send a heartbeat without an interval.")
            return

        if not forced:
            await asyncio.sleep(self.client.heartbeat_interval)

        await self.send_json({"op": OpCode.HEARTBEAT, "d": None})

        start = perf_counter_ns()

        await self.wait_for(
            opcode=OpCode.HEARTBEAT_ACK, timeout=self.client.heartbeat_interval
        )

        end = perf_counter_ns()

        self.client._heartbeats.append(end - start)

    async def handle(self, message: DiscordWSMessage):
        try:
            event = message.json()
        except json.JSONDecodeError:
            logger.error("Failed to decode message: %s", message.data)
            return
        if event["op"] in self.wait_for_events:
            for event in self.wait_for_events[event["op"]]:
                if event.check:
                    try:
                        if await event.check(event):
                            event.future.set_result(event)
                    except Exception as exception:
                        event.future.set_exception(exception)
                else:
                    event.future.set_result(event)

        elif event.get("t") and event["t"].lower() in self.wait_for_events:
            for event in self.wait_for_events[event["t"].lower()]:
                if event.check:
                    try:
                        if await event.check(event):
                            event.future.set_result(event)
                    except Exception as exception:
                        event.future.set_exception(exception)
                else:
                    event.future.set_result(event)

        if event["op"] != OpCode.DISPATCH:
            await self.event_mapping[event["op"]](event["d"])

class DiscordWSMessage:
    def __init__(self, *, data, type, extra):
        self.data = data
        self.type = type
        self.extra = extra

    def json(self) -> Any:
        return json.loads(self.data)


class GatewayWebSocket(aiohttp.ClientWebSocketResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer: bytearray = bytearray()
        self.inflator = zlib.decompressobj()

    async def receive(self, *args, **kwargs):
        ws_message = await super().receive(*args, **kwargs)
        message = ws_message.data

        if isinstance(message, bytes):

            self.buffer.extend(message)

            if len(message) < 4 or message[-4:] != b"\x00\x00\xff\xff":
                return

            message = self.inflator.decompress(self.buffer)

            message = message.decode("utf-8")
            self.buffer = bytearray()

        return DiscordWSMessage(
            data=message, type=ws_message.type, extra=ws_message.extra
        )


class WebSocketClient:
    def __init__(
        self,
        token: TokenStore,
        intents: Intents,
        *,
        presence: Optional[Presence] = None,
        http: HTTPClient,
    ):
        self.token: TokenStore = token
        self.intents: Intents = intents
        self.presence: Optional[Presence] = presence

        self.ws: Optional[GatewayWebSocket] = None
        self.http: HTTPClient = http

        self.rate_limiter: GatewayRateLimiter = GatewayRateLimiter()
        self.event_handler: GatewayEventHandler = GatewayEventHandler(self)

        self.sequence: Optional[int] = None
        self.session_id: Optional[str] = None
        self.heartbeat_interval: Optional[float] = None
        self._heartbeats: List[int] = []

    @property
    def latency(self) -> Optional[float]:
        if not self._heartbeats:
            return None
        return sum(self._heartbeats) / len(self._heartbeats)

    async def connect(self):
        url = await self.http.get_gateway()
        version = self.http.version.value
        asyncio.create_task(self.rate_limiter.reset.start())
        self.ws = await self.http.ws_connect(f"{url}?v={version}&encoding=json&compress=zlib-stream")
        async for message in self.ws:
            logger.debug("Received message: %s", message.json())
            await self.event_handler.handle(message)  # type: ignore
