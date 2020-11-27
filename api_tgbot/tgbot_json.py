from aiohttp import ClientSession, ClientResponse

class TgBotJson:
    def __init__(self, token: str = None):
        assert token and token != ""
        self.token = token
        self.url = "https://api.telegram.org/bot" + token + "/"

    def __repr__(self):
        return self.url   # pragma: no cover

    async def getUpdates(self, json: dict = None) -> ClientResponse:
        url = self.url + "getUpdates"
        async with ClientSession() as c:
            return await c.get(url)

    async def sendMessage(self, chat_id, text, **kwargs) -> ClientResponse:
        assert text and text != ""
        if "parse_mode" not in kwargs and "@" not in text:
            kwargs["parse_mode"] = "markdown"
        url = self.url + 'sendMessage'
        params = {'chat_id': chat_id, 'text': text, **kwargs}
        async with ClientSession() as c:
            response = await c.post(url, json=params)
            r = await response.json()
            if response.status == 400 and "can't parse entities" in r.get("description", ""):
                del params["parse_mode"]
                response2 = await c.post(url, json=params)
                return response2
            return response

    # async def sendPhoto(self, chat_id, **kwargs) -> ClientResponse:
    #     """
    #     @example photo="http://www.aisystems.ru/temp/hor/img/logo.png",
    #     caption="<b>Возвращение квантового кота</b>", parse_mode="html"
    #     """
    #     url = self.url + 'sendPhoto'
    #     params = {'chat_id': chat_id, **kwargs}
    #     async with ClientSession() as c:
    #         return await c.post(url, json=params)
    #
    # async def sendMediaGroup(self, chat_id, media: list, **kwargs) -> ClientResponse:
    #     """
    #     @example photo="http://www.aisystems.ru/temp/hor/img/logo.png",
    #     caption="<b>Возвращение квантового кота</b>", parse_mode="html"
    #     """
    #     url = self.url + 'sendMediaGroup'
    #     params = {'chat_id': chat_id, "media": media, **kwargs}
    #     async with ClientSession() as c:
    #         return await c.post(url, json=params)
    #
    # async def sendAnimation(self, chat_id, **kwargs) -> ClientResponse:
    #     url = self.url + 'sendAnimation'
    #     params = {'chat_id': chat_id, **kwargs}
    #     async with ClientSession() as c:
    #         return await c.post(url, json=params)
    #
    # async def sendVideo(self, chat_id, **kwargs) -> ClientResponse:
    #     url = self.url + 'sendVideo'
    #     params = {'chat_id': chat_id, **kwargs}
    #     async with ClientSession() as c:
    #         return await c.post(url, json=params)

    async def setWebhook(self, wh_url) -> ClientResponse:
        url = self.url + "setWebhook?url=" + wh_url
        async with ClientSession() as c:
            return await c.get(url)

    async def getWebhookInfo(self) -> ClientResponse:
        url = self.url + "getWebhookInfo"
        async with ClientSession() as c:
            return await c.get(url)

    async def deleteWebhook(self) -> ClientResponse:
        url = self.url + "deleteWebhook"
        async with ClientSession() as c:
            return await c.get(url)

    # async def getChatAdministrators(self, chat_id, **kwargs) -> ClientResponse:
    #     url = self.url + 'getChatAdministrators'
    #     params = {'chat_id': chat_id, **kwargs}
    #     async with ClientSession() as c:
    #         return await c.post(url, json=params)

    async def deleteMessage(self, chat_id, message_id) -> ClientResponse:
        url = self.url + 'deleteMessage'
        params = {'chat_id': chat_id, 'message_id': message_id}
        async with ClientSession() as c:
            return await c.post(url, json=params)

    async def editMessageText(self, chat_id, message_id, text, **kwargs) -> ClientResponse:
        if "parse_mode" not in kwargs and "@" not in text:
            kwargs["parse_mode"] = "markdown"
        url = self.url + 'editMessageText'
        params = {'chat_id': chat_id, 'message_id': message_id, 'text': text, **kwargs}
        async with ClientSession() as c:
            response = await c.post(url, json=params)
            r = await response.json()
            if response.status == 400 and "can't parse entities" in r.get("description", ""):
                del params["parse_mode"]
                response2 = await c.post(url, json=params)
                return response2
            return response


    # async def editMessageMedia(self, chat_id, message_id, media, **kwargs) -> ClientResponse:
    #     url = self.url + 'editMessageMedia'
    #     params = {'chat_id': chat_id, 'message_id': message_id, 'media': media, **kwargs}
    #     async with ClientSession() as c:
    #         return await c.post(url, json=params)

    # async def paramsCallbackQuery(self, callback_query_id, text, **kwargs) -> ClientResponse:
    #     url = self.url + 'paramsCallbackQuery'
    #     params = {'callback_query_id': callback_query_id, 'text': text, **kwargs}
    #     async with ClientSession() as c:
    #         return await c.post(url, json=params)
