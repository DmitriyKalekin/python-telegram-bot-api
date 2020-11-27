from aiohttp import ClientSession, ClientResponse

class TgBotJson:
    def __init__(self, token: str = None):
        assert token and token != ""
        self.token = token
        self.url = "https://api.telegram.org/bot" + token + "/"

    def __repr__(self):
        return self.url   # pragma: no cover

    async def getUpdates(self, limit: int = 100, **kwargs) -> ClientResponse:
        url = self.url + "getUpdates"
        params = {'limit': limit, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.get(url, json=params)

    async def sendMessage(self, chat_id: int, text: str, **kwargs) -> ClientResponse:
        assert text and text != ""
        if "parse_mode" not in kwargs and "@" not in text:
            kwargs["parse_mode"] = "markdown"
        url = self.url + 'sendMessage'
        params = {'chat_id': chat_id, 'text': text, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.post(url, json=params)
            r = await response.json()
            if response.status == 400 and "can't parse entities" in r.get("description", ""):
                del params["parse_mode"]
                response2 = await c.post(url, json=params)
                return response2
            return response

    async def editMessageText(self, chat_id: int, message_id: int, text: str, **kwargs) -> ClientResponse:
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

    async def deleteMessage(self, chat_id: int, message_id: int) -> ClientResponse:
        url = self.url + 'deleteMessage'
        params = {'chat_id': chat_id, 'message_id': message_id}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.post(url, json=params)

    async def sendPhoto(self, chat_id: int, caption: str = "", **kwargs) -> ClientResponse:
        if "parse_mode" not in kwargs:
            kwargs["parse_mode"] = "html"
        url = self.url + 'sendPhoto'
        params = {'chat_id': chat_id, 'caption': caption, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.post(url, json=params)

    async def sendMediaGroup(self, chat_id: int, media: list, **kwargs) -> ClientResponse:
        url = self.url + 'sendMediaGroup'
        params = {'chat_id': chat_id, "media": media, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.post(url, json=params)

    async def sendAnimation(self, chat_id: int, **kwargs) -> ClientResponse:
        url = self.url + 'sendAnimation'
        params = {'chat_id': chat_id, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.post(url, json=params)

    async def sendVideo(self, chat_id: int, **kwargs) -> ClientResponse:
        url = self.url + 'sendVideo'
        params = {'chat_id': chat_id, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.post(url, json=params)

    async def setWebhook(self, wh_url: str) -> ClientResponse:
        url = self.url + "setWebhook?url=" + wh_url
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.get(url)

    async def getWebhookInfo(self) -> ClientResponse:
        url = self.url + "getWebhookInfo"
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.get(url)

    async def deleteWebhook(self) -> ClientResponse:
        url = self.url + "deleteWebhook"
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.get(url)

    async def getChatAdministrators(self, chat_id: int, **kwargs) -> ClientResponse:
        url = self.url + 'getChatAdministrators'
        params = {'chat_id': chat_id, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.post(url, json=params)

    async def editMessageMedia(self, chat_id: int, message_id: int, media: dict, **kwargs) -> ClientResponse:
        url = self.url + 'editMessageMedia'
        params = {'chat_id': chat_id, 'message_id': message_id, 'media': media, **kwargs}
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            return await c.post(url, json=params)

