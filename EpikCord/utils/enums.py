from __future__ import annotations

from enum import IntEnum
from logging import getLogger


class OpCode(IntEnum):
    """The opcodes used in the Discord Gateway."""

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class GatewayCloseCode(IntEnum):
    """The close codes used in the Discord Gateway."""

    ABNORMAL_CLOSURE = 1006
    UNKNOWN_ERROR = 4000
    UNKNOWN_OPCODE = 4001
    DECODE_ERROR = 4002
    NOT_AUTHENTICATED = 4003
    AUTHENTICATION_FAILED = 4004
    ALREADY_AUTHENTICATED = 4005
    INVALID_SEQUENCE = 4007
    RATE_LIMITED = 4008
    SESSION_TIMED_OUT = 4009
    INVALID_SHARD = 4010
    SHARDING_REQUIRED = 4011
    INVALID_API_VERSION = 4012
    INVALID_INTENTS = 4013
    DISALLOWED_INTENTS = 4014


class VoiceOpCode(IntEnum):
    """The opcodes used in the Discord Voice WebSocket connection."""

    IDENTIFY = 0
    SELECT_PROTOCOL = 1
    READY = 2
    HEARTBEAT = 3
    SESSION_DESCRIPTION = 4
    SPEAKING = 5
    HEARTBEAT_ACK = 6
    RESUME = 7
    HELLO = 8
    RESUMED = 9
    CLIENT_DISCONNECT = 13


class VoiceCloseCode(IntEnum):
    """The close codes used in the Discord Voice WebSocket connection."""

    UNKNOWN_OPCODE = 4001
    FAILED_TO_DECODE_PAYLOAD = 4002
    NOT_AUTHENTICATED = 4003
    AUTHENTICATION_FAILED = 4004
    ALREADY_AUTHENTICATED = 4005
    SESSION_NO_LONGER_VALID = 4006
    SESSION_TIMEOUT = 4009
    SERVER_NOT_FOUND = 4011
    UNKNOWN_PROTOCOL = 4012
    DISCONNECTED = 4014
    VOICE_SERVER_CRASHED = 4015
    UNKNOWN_ENCRYPTION_MODE = 4016


class StatusCode(IntEnum):
    pass


class HTTPCodes(StatusCode):
    """HTTP response codes."""

    OK = 200
    CREATED = 201

    NO_CONTENT = 204
    NOT_MODIFIED = 304

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405

    TOO_MANY_REQUESTS = 429

    GATEWAY_UNAVAILABLE = 502
    SERVER_ERROR = 500

    @classmethod
    def _missing_(cls, value: object) -> HTTPCodes:
        if not isinstance(value, int):
            raise ValueError(f"{value} is not a valid HTTP status code.")

        if HTTPCodes.SERVER_ERROR < value < 600:
            return HTTPCodes.SERVER_ERROR

        raise ValueError(
            f"HTTP Status Code `{value}` is undocumented.\n"
            "Please create an issue at:"
            " https://github.com/EpikCord/EpikCord.py/issues"
            " with the following traceback."
        )


class JSONErrorCodes(StatusCode):
    GENERAL_ERROR = 0

    UNKNOWN_ACCOUNT = 10001
    UNKNOWN_APPLICATION = 10002
    UNKNOWN_CHANNEL = 10003
    UNKNOWN_GUILD = 10004
    UNKNOWN_INTEGRATION = 10005
    UNKNOWN_INVITE = 10006
    UNKNOWN_MEMBER = 10007
    UNKNOWN_MESSAGE = 10008
    UNKNOWN_OVERWRITE = 10009
    UNKNOWN_PROVIDER = 10010
    UNKNOWN_ROLE = 10011
    UNKNOWN_TOKEN = 10012
    UNKNOWN_USER = 10013
    UNKNOWN_EMOJI = 10014
    UNKNOWN_WEBHOOK = 10015
    UNKNOWN_WEBHOOK_SERVICE = 10016

    UNKNOWN_SESSION = 10020

    UNKNOWN_BAN = 10026
    UNKNOWN_SKU = 10027

    UNKNOWN_STORE_LISTING = 10028
    UNKNOWN_ENTITLEMENT = 10029

    UNKNOWN_BUILD = 10030
    UNKNOWN_LOBBY = 10031

    UNKNOWN_BRANCH = 10032
    UNKNOWN_STORE_DIRECTORY_LAYOUT = 10033

    UNKNOWN_REDISTRIBUTABLE = 10036

    UNKNOWN_GIFT_CODE = 10038

    UNKNOWN_STREAM = 10049
    UNKNOWN_PREMIUM_SERVER_SUB_COOLDOWN = 10050

    UNKNOWN_GUILD_TEMPLATE = 10057

    UNKNOWN_DISCOVERABLE_SERVER_CATEGORY = 10059
    UNKNOWN_STICKER = 10060

    UNKNOWN_INTERACTION = 10062
    UNKNOWN_APPLICATION_COMMAND = 10063

    UNKNOWN_VOICE_STATE = 10065
    UNKNOWN_APP_COMMAND_PERMS = 10066
    UNKNOWN_STAGE_INSTANCE = 10067
    UNKNOWN_GUILD_MEMBER_VERIFICATION_FORM = 10068
    UNKNOWN_GUILD_WELCOME_SCREEN = 10069
    UNKNOWN_GUILD_SCHEDULED_EVENT = 10070
    UNKNOWN_GUILD_SCHEDULED_EVENT_USER = 10071

    UNKNOWN_TAG = 10087

    NOT_BOT_ENDPOINT = 20001
    ONLY_BOT_ENDPOINT = 20002

    EXPLICIT_CONTENT_CANNOT_BE_SEND = 20009

    APP_UNAUTHORIZED = 20012

    SLOWMODE_LIMIT_FAILURE = 20016

    ACCOUNT_OWNERSHIP_REQUIRED = 20018

    ANNOUNCEMENT_RATE_LIMIT = 20022

    CHANNEL_WRITE_RATE_LIMIT = 20028
    SERVER_ACTION_RATE_LIMIT = 20029

    METHOD_NOT_ALLOWED = 20031

    INSUFFICIENT_GUILD_PREMIUM_SUBSCRIPTION = 20035

    MAX_GUILD_REACHED = 30001
    MAX_FRIENDS_REACHED = 30002
    MAX_PINS_REACHED = 30003
    MAX_RECIPIENT_REACHED = 30004
    MAX_GUILD_ROLE_REACHED = 30005

    MAX_WEBHOOKS_REACHED = 30007
    MAX_EMOJIS_REACHED = 30008

    MAX_REACTIONS_REACHED = 30010

    MAX_GUILD_CHANNELS_REACHED = 30013

    MAX_ATTACHMENTS_REACHED = 30015
    MAX_INVITE_CODES_REACHED = 30016

    MAX_ANIMATED_EMOTES_REACHED = 30018
    MAX_SERVER_MEMBER_REACHED = 30019

    MAX_SERVER_CATEGORY_REACHED = 30030
    GUILD_ALREADY_HAS_TEMPLATE = 30031

    MAX_THREAD_PARTICIPANTS_REACHED = 30033

    MAX_NON_GUILD_BANS_REACHED = 30035

    MAX_BAN_FETCH_REACHED = 30037
    MAX_INCOMPLETE_GUILD_SCHEDULED_EVENTS_REACHED = 30038
    MAX_STICKER_REACHED = 30039
    MAX_MEMBER_PRUNE_REACHED = 30040

    MAX_GUILD_WIDGET_UPDATE_REACHED = 30042

    MAX_SUP_HOUR_EDIT = 30046
    MAX_PIN_THREAD_REACHED = 30047
    MAX_TAG_REACHED = 30048

    UNAUTHORIZED_TOKEN = 40001
    ACCOUNT_VERIFICATION_NEEDED = 40002
    DIRECT_MESSAGE_RATE_LIMITED = 40003
    SEND_MESSAGE_DISABLED = 40004
    REQUEST_TOO_LARGE = 40005
    DISABLED_FEATURE = 40006
    BANNED_FROM_GUILD = 40007

    NOT_CONNECTED_TO_VOICE = 40032
    ALREADY_CROSSPOSTED = 40033

    APP_COMMAND_ALREADY_EXIST = 40041

    INTERACTION_ALREADY_ACKNOWLEDGED = 40060

    MISSING_ACCESS = 50001
    INVALID_ACCOUNT_TYPE = 50002
    DM_CHANNEL_ACTION_PROHIBITED = 50003
    GUILD_WIDGET_DISABLED = 50004
    MESSAGE_AUTHORED_BY_ANOTHER_USER = 50005
    EMPTY_MESSAGE = 50006
    USER_NOT_MESSAGABLE = 50007
    NON_TEXT_CHANNEL = 50008
    CHANNEL_VERIFICATION_TOO_HIGH = 50009
    OAUTH2_APPLICATION_BOT_AUTH_INVALID = 50010
    OAUTH2_APP_LIMIT_REACHED = 50011
    INVALID_OAUTH2_STATE = 50012
    ACTION_PERMISSION_MISSING = 50013
    INVALID_AUTH_TOKEN = 50014
    NOTE_TOO_LONG = 50015
    DELETE_OUT_OF_RANGE = 50016

    INVALID_PIN_CHANNEL = 50019
    INVALID_INVITE_CODE = 50020
    ACTION_ON_SYSTEM_MESSAGE_PROHIBITED = 50021

    ACTION_ON_WRONG_CHANNEL_TYPE = 50024
    OAUTH2_TOKEN_INVALID = 50025
    MISSING_OAUTH2_SCOPE = 50026
    INVALID_WEBHOOK_TOKEN = 50027
    INVALID_ROLE = 50028

    INVALID_RECIPIENT = 50033
    MESSAGE_TOO_OLD = 50034
    INVALID_FORM_BODY = 50035
    INVITE_ACCEPTED_TO_GUILD_NOT_MEMBER = 50036

    INVALID_API_VERSION = 50041

    FILE_UPLOAD_SIZE_LIMIT_EXCEEDED = 50045
    INVALID_FILE_UPLOAD = 50046

    CANNOT_SELF_REDEEM_GIFT = 50054
    INVALID_GUILD = 50055

    INVALID_MESSAGE_TYPE = 50068

    PAYMENT_SOURCE_REQUIRED = 50070

    CHANNEL_REQUIRED_FOR_COMMUNITY_GUILD = 50074

    CANNOT_EDIT_MESSAGE_STICKER = 50080
    INVALID_STICKER_SEND = 50081

    INVALID_ACTION_ON_THREAD_ARCHIVED = 50083
    INVALID_THREAD_NOTIFICATION_SETTINGS = 50084
    BEFORE_DATE_EARLIER_THAN_THEAD_CREATION = 50085
    COMMUNITY_CHANNEL_MUST_BE_A_TEXT_CHANNEL = 50086

    SERVER_NOT_AVAILABLE_FOR_LOCATION = 50095

    SERVER_REQUIRED_MONETIZATION = 50097

    SERVER_BOOTS_INSUFFICIENT = 50101

    INVALID_JSON_BODY = 50109

    STICKER_PERMISSION_MISSING = 50600
    TWO_FACTOR_AUTH_REQUIRED = 50603

    DISCORD_TAG_UNALLOCATED = 80004

    REACTION_BLOCKED = 90001

    API_RESOURCE_OVERLOADED = 130000
    STAGE_ALREADY_OPEN = 150006

    HISTORY_PERMISSION_MISSING_TO_REPLY = 160002

    THREAD_ALREADY_CREATED_FOR_MESSAGE = 160004
    LOCKED_THREAD = 160005
    MAX_ACTIVE_THREADS_REACHED = 160006
    MAX_MEMBER_ACTIVE_ANNOUNCEMENTS_THREAD_REACHED = 160007

    INVALID_JSON_LOTTIE_FILE = 170001
    RASTERIZED_IMG_IN_LOTTIE_FILE = 170002
    MAX_STICKER_FRAMERATE_REACHED = 170003
    STICKER_FRAME_COUNT_EXCEEDED = 170004
    LOTTIE_ANIMATION_DIMENSIONS_EXCEEDED = 170005
    STICKER_FRAME_RATE_OUT_OF_RANGE = 170006
    STICKER_ANIMATION_DURATION_EXCEEDED = 170007

    CANNOT_UPLOAD_FINISHED_EVENT = 180000

    STAGE_CREATION_ON_STAGE_EVENT_FAILED = 180002

    @classmethod
    def _missing_(cls, value: object) -> JSONErrorCodes:
        logger = getLogger("EpikCord.exceptions")
        logger.warning(f"Unknown JSON error code: {value}")
        return cls.GENERAL_ERROR
