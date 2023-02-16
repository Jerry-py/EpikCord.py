from datetime import datetime

from discord_typings import GuildMemberData, RoleData, RoleTagsData

from .client import Client
from .flags import GuildMemberFlags, Permissions
from .user import User
from .utils import instance_or_none, int_or_none


class GuildMember:
    def __init__(self, client: Client, data: GuildMemberData):
        self.client = client
        self.user = instance_or_none(
            User, data.get("user"), client, data.get("user"), ignore_value=True
        )
        self.nick = data.get("nick")
        self.avatar = data.get("avatar")
        # self.roles = [Role(client, role) for role in data.get("roles", [])]
        self.roles = data["roles"]
        self.joined_at = (
            datetime.fromisoformat(data["joined_at"])
            if data.get("joined_at")
            else None
        )
        self.premium_since = instance_or_none(
            datetime.fromisoformat, data.get("premium_since")
        )
        self.deaf = data["deaf"]
        self.mute = data["mute"]
        self.flags = GuildMemberFlags(data["flags"])  # type: ignore # DiscordTyping/32
        self.pending = data.get("pending")
        self.permissions = instance_or_none(
            Permissions, data.get("permissions")
        )
        self.communication_disabled_until = instance_or_none(
            datetime.fromisoformat, data.get("communication_disabled_until")
        )


class RoleTags:
    def __init__(self, data: RoleTagsData):
        self._data = data
        self.bot_id = int_or_none(data.get("bot_id"))
        self.integration_id = int_or_none(data.get("integration_id"))
        self.premium_subscriber = (
            True if data.get("premium_subscriber") else False
        )
        self.subscription_listing_id = int_or_none(
            data.get("subscription_listing_id")
        )
        self.available_for_purchase = (
            True if data.get("available_for_purchase") else False
        )
        self.guild_connections = (
            True if data.get("guild_connections") else False
        )


class Role:
    def __init__(self, client: Client, data: RoleData):
        self.client = client
        self._data = data
        self.id = int(data["id"])
        self.name = data["name"]
        self.color = int(data["color"])
        self.hoist = data["hoist"]
        self.icon = data.get("icon")
        self.unicode_emoji = data.get("unicode_emoji")
        self.position = data["position"]
        self.permissions = Permissions(int(data["permissions"]))
        self.managed = data["managed"]
        self.mentionable = data["mentionable"]
        self.tags = instance_or_none(RoleTags, data.get("tags"))
