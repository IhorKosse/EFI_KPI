from typing import Self

from aiogram import types


class BotCtx:
    def __init__(self, bot, rc, ai) -> None:
        self.bot = bot
        self.redis = rc
        self.ai = ai


class TelegramMessageCtx:
    def __init__(self, message: types.Message) -> None:
        self._message = message
        self._modified_text = None

    @property
    def message(self) -> types.Message:
        return self._message

    @property
    def modified_text(self) -> str:
        return self._modified_text if self._modified_text is not None else self._message.text

    def update_message_text(self, new_text: str) -> None:
        self._modified_text = new_text

   

class TelegramChatCtx:
    """
    Combines user context and chat context
    """

    def __init__(self, user_id: int, chat_id: int) -> None:
        self._user_id = user_id
        self._chat_id = chat_id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id = value

    @classmethod
    def from_message_context(cls, message_ctx: TelegramMessageCtx) -> Self:
        ctx = TelegramChatCtx(0, 0)

        if message_ctx.message.from_user.is_bot:
            ctx.user_id = message_ctx.message.chat.id
            ctx.chat_id = message_ctx.message.from_user.id
        else:
            ctx.user_id = message_ctx.message.from_user.id
            ctx.chat_id = message_ctx.message.chat.id

        return ctx


class TelegramUserCtx:
    def __init__(self, id: int) -> None:
        self._id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @classmethod
    def from_message_context(cls, message_ctx: TelegramMessageCtx) -> Self:
        ctx = TelegramUserCtx(0)

        ctx.id = (
            message_ctx.message.chat.id if message_ctx.message.from_user.is_bot else message_ctx.message.from_user.id
        )
        return ctx

    @classmethod
    def from_chat_context(cls, chat: TelegramChatCtx) -> Self:
        ctx = TelegramUserCtx(0)
        ctx.id = chat.user_id
        return ctx


# class TelegramFullMessageCtx:
#     def __init__(self, user_id: int, chat_id: int, message_id: int) -> None:
#         self._user_id = user_id
#         self._chat_id = chat_id
#         self._message_id = message_id

#     @property
#     def user_id(self):
#         return self._user_id

#     @user_id.setter
#     def user_id(self, value):
#         self._user_id = value

#     @property
#     def chat_id(self):
#         return self._chat_id

#     @chat_id.setter
#     def chat_id(self, value):
#         self._chat_id = value

#     @property
#     def message_id(self):
#         return self._message_id

#     @message_id.setter
#     def message_id(self, value):
#         self._message_id = value

#     @classmethod
#     def from_message_context(cls, message_ctx: TelegramMessageCtx) -> Self:
#         ctx = TelegramFullMessageCtx(0, 0, 0)

#         ctx.user_id = (
#             message_ctx.message.chat.id if message_ctx.message.from_user.is_bot else message_ctx.message.from_user.id
#         )

#         ctx.chat_id = message_ctx.message.chat.id
#         ctx.message_id = message_ctx.message.message_id

#         return ctx
