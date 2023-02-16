from discord_typings import (
    ApplicationCommandInteractionData,
    InteractionData,
    ResolvedInteractionDataData,
)

from .client import Client
from .file import Attachment
from .flags import Permissions
from .guild import GuildMember, Role
from .user import User
from .utils import (
    InteractionType,
    Locale,
    instance_or_none,
    int_or_none,
    ApplicationCommandType,
)


class BaseInteraction:
    def __init__(self, client: Client, data: InteractionData):
        self.client: Client = client
        self._data = data
        self.id = int(data["id"])
        self.application_id = int(data["application_id"])
        self.type: InteractionType = InteractionType(data["type"])
        self.guild_id = int_or_none(data.get("guild_id"))
        self.channel_id = int_or_none(data.get("channel_id"))
        self.author = instance_or_none(
            User, data.get("user"), client, data.get("user"), ignore_value=True
        ) or instance_or_none(
            GuildMember,
            data.get("member"),
            client,
            data.get("member"),
            ignore_value=True,
        )
        self.token = data["token"]
        self.version = data["version"]
        self.app_permissions = instance_or_none(
            Permissions, data.get("app_permissions")
        )
        self.locale = instance_or_none(Locale, data.get("locale"))
        self.guild_locale = instance_or_none(Locale, data.get("guild_locale"))


class ResolvedInteractionData:
    def __init__(self, client: Client, data: ResolvedInteractionDataData):
        self.users = {
            int(k): User(client, v) for k, v in data.get("users", {}).items()
        }
        self.members = {
            int(k): GuildMember(client, v)
            for k, v in data.get("members", {}).items()
        }
        self.roles = {
            int(k): Role(client, v) for k, v in data.get("roles", {}).items()
        }
        # CHANNELS
        # MESSAGES
        self.attachments = {
            int(k): Attachment(v)
            for k, v in data.get("attachments", {}).items()
        }


class BaseApplicationCommandInteraction(BaseInteraction):
    def __init__(self, client: Client, data: ApplicationCommandInteractionData):
        super().__init__(client, data)
        self.data = data["data"]
        self.command_id = int(self.data["id"])
        self.command_name = self.data["name"]
        self.command_type: ApplicationCommandType = ApplicationCommandType(
            self.data["type"]
        )
        self.resolved = instance_or_none(
            ResolvedInteractionData, data.get("resolved")
        )


# class ChatInputCommandInteraction():
#     def __init__(self, client: Client, data: ApplicationCommandInteractionData):
#         super().__init__(client, data)
#         # OPTIONS

# class ContextMenuInteraction(BaseInteraction):
