from pygramtic.models import Update, Message, WebhookInfo, ChatMember
from typing import List, cast
from .tgbot_json import TgBotJson

import logging

class TgException(Exception):
    pass


class TgBot:
    def __init__(self, token: str):
        self.token = token
        self._tg = TgBotJson(token)

    def _try_parse_result(self, response):
        if "result" not in response.payload:
            raise TgException(response.payload["description"])



    async def getUpdates(self, limit: int = 100, **kwargs) -> List[Update]:
        """
        Use this method to receive incoming updates using long polling (wiki). An Array of Update objects is returned.
        :param limit:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.getUpdates(limit, **kwargs)
        self._try_parse_result(response)
        return cast(List[Update], list([Update.parse_obj(obj) for obj in response.payload["result"]]))

    async def sendMessage(self, chat_id: int, text: str, **kwargs) -> Message:
        """
        Use this method to send text messages. On success, the sent Message is returned.
        :param chat_id:
        :param text:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.sendMessage(chat_id, text, **kwargs)
        self._try_parse_result(response)
        return Message.parse_obj(response.payload["result"])

    async def editMessageText(self, chat_id, message_id, text, **kwargs) -> Message:
        """
        Use this method to edit text and game messages.
        TODO: On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returne
        :param chat_id:
        :param message_id:
        :param text:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.editMessageText(chat_id, message_id, text, **kwargs)
        self._try_parse_result(response)
        return Message.parse_obj(response.payload["result"])

    async def deleteMessage(self, chat_id, message_id) -> bool:
        """
        Use this method to delete a message, including service messages, with the following limitations:
        - A message can only be deleted if it was sent less than 48 hours ago.
        - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
        - Bots can delete outgoing messages in private chats, groups, and supergroups.
        - Bots can delete incoming messages in private chats.
        - Bots granted can_post_messages permissions can delete outgoing messages in channels.
        - If the bot is an administrator of a group, it can delete any message there.
        - If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.
        Returns True on success.
        :param chat_id:
        :param message_id:
        :raises TgException
        :return:
        """
        response = await self._tg.deleteMessage(chat_id, message_id)
        self._try_parse_result(response)
        return True

    async def sendPhoto(self, chat_id: int, caption: str = "", **kwargs) -> Message:
        """
        Use this method to send photos. On success, the sent Message is returned.
        :param chat_id:
        :param caption:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.sendPhoto(chat_id, caption, **kwargs)
        self._try_parse_result(response)
        return Message.parse_obj(response.payload["result"])

    async def sendMediaGroup(self, chat_id: int, media: list, **kwargs) -> List[Message]:
        """
        Use this method to send a group of photos, videos, documents or audios as an album.
        Documents and audio files can be only grouped in an album with messages of the same type.
        On success, an array of Messages that were sent is returned.
        :param chat_id:
        :param media:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.sendMediaGroup(chat_id, media, **kwargs)
        self._try_parse_result(response)
        return [Message.parse_obj(obj) for obj in response.payload["result"]]

    async def sendAnimation(self, chat_id: int, **kwargs) -> Message:
        """
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound).
        On success, the sent Message is returned.
        Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        :param chat_id:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.sendAnimation(chat_id, **kwargs)
        self._try_parse_result(response)
        return Message.parse_obj(response.payload["result"])

    async def sendVideo(self, chat_id: int, **kwargs) -> Message:
        """
        Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as Document).
        On success, the sent Message is returned.
        Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        :param chat_id:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.sendVideo(chat_id, **kwargs)
        self._try_parse_result(response)
        return Message.parse_obj(response.payload["result"])

    async def setWebhook(self, wh_url: str) -> bool:
        """
        Use this method to specify a url and receive incoming updates via an outgoing webhook.
        Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url,
        containing a JSON-serialized Update.
        In case of an unsuccessful request, we will give up after a reasonable amount of attempts.
        Returns True on success.
        If you'd like to make sure that the Webhook request comes from Telegram,
        we recommend using a secret path in the URL, e.g. https://www.example.com/<token>.
        Since nobody else knows your bot's token, you can be pretty sure it's us.
        :param wh_url:
        :raises TgException
        :return:
        """
        response = await self._tg.setWebhook(wh_url)
        self._try_parse_result(response)
        return response.payload["result"]

    async def getWebhookInfo(self) -> WebhookInfo:
        """
        Use this method to get current webhook status.
        Requires no parameters.
        On success, returns a WebhookInfo object.
        If the bot is using getUpdates, will return an object with the url field empty.
        :raises TgException
        :return:
        """
        response = await self._tg.getWebhookInfo()
        self._try_parse_result(response)
        return WebhookInfo.parse_obj(response.payload["result"])

    async def deleteWebhook(self) -> bool:
        """
        Use this method to remove webhook integration if you decide to switch back to getUpdates.
        Returns True on success.
        :raises TgException
        :return:
        """
        response = await self._tg.deleteWebhook()
        self._try_parse_result(response)
        return response.payload["result"] == True

    async def getChatAdministrators(self, chat_id: int, **kwargs) -> List[ChatMember]:
        """
        Use this method to get a list of administrators in a chat.
        On success, returns an Array of ChatMember objects that contains information about all chat administrators except other bots.
        If the chat is a group or a supergroup and no administrators were appointed, only the creator will be returned.
        :param chat_id:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.getChatAdministrators(chat_id, **kwargs)
        self._try_parse_result(response)
        return [ChatMember.parse_obj(obj) for obj in response.payload["result"]]

    async def editMessageMedia(self, chat_id: int, message_id: int, media: dict, **kwargs) -> Message:
        """
        Use this method to edit animation, audio, document, photo, or video messages.
        If a message is part of a message album, then it can be edited only to an audio for audio albums,
        only to a document for document albums and to a photo or a video otherwise.
        When an inline message is edited, a new file can't be uploaded.
        Use a previously uploaded file via its file_id or specify a URL.
        TODO: On success, if the edited message was sent by the bot, the edited Message is returned, otherwise True is returned.
        :param chat_id:
        :param message_id:
        :param media:
        :param kwargs:
        :raises TgException
        :return:
        """
        response = await self._tg.editMessageMedia(chat_id, message_id, media, **kwargs)
        self._try_parse_result(response)
        return Message.parse_obj(response.payload["result"])
