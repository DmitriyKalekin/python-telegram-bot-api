# Telegram Bot API - Python SDK (using aiohttp)

<p align="center">
<img src="https://img.shields.io/badge/tests-pytest-orange?style=for-the-badge" alt="pytest"/>
<img src="https://img.shields.io/badge/async-asyncio, aiohttp-green?style=for-the-badge" alt="asyncio, aiohttp"/>
<a href="https://t.me/herr_horror"><img src="https://img.shields.io/badge/Telegram Chat-@herr_horror-2CA5E0.svg?logo=telegram&style=for-the-badge" alt="Chat on Telegram"/></a>
<img src="https://img.shields.io/badge/version-v.0.0.7-green?style=for-the-badge" alt="Last Release"/>
</p>


Simple and fast client to call rest-api endpoints `api.telegram.org` using aiohttp package.  

View at:
https://pypi.org/project/python-telegram-bot-api/


## How to install
```bash
pip3 install python-telegram-bot-api
```


## Usage

Main example:
```python
import asyncio
from api_tgbot import TgBot, TgException


TGBOT_TOKEN = "12345:YOUR_TOKEN"
APP_HOSTNAME = "https://YOUR_HOSTNAME.ngrok.io"
CHAT_ID = 123456789  # your chat id

client_tgbot = TgBot(token=TGBOT_TOKEN)


async def main_async():
    try:
        response = await client_tgbot.setWebhook("{hostname}/tgbot/wh".format(hostname=APP_HOSTNAME))
        assert type(response) == bool
        assert response == True
    except TgException as e:
        print(e)
        
    try:
        sent_msg = await client_tgbot.sendMessage(CHAT_ID, "Hello from Telegram Bot!")
        assert sent_msg.chat.id == CHAT_ID
        print(sent_msg.text)
    except TgException as e:
        print(e)


if __name__ == "__main__":
    asyncio.run_until_complete(main_async())

```

Simple JSON-Example if you are not interested in pydantic models and want to use dict in answers:   
```python
import asyncio
from api_tgbot import TgBotJson


TGBOT_TOKEN = "12345:YOUR_TOKEN"
APP_HOSTNAME = "https://YOUR_HOSTNAME.ngrok.io"
CHAT_ID = 123456789  # your chat id

client_tgbot = TgBotJson(token=TGBOT_TOKEN)


async def main_async():
    response = await client_tgbot.setWebhook("{hostname}/tgbot/wh".format(hostname=APP_HOSTNAME))
    print(response.status)  # 200
    print(response.payload) # {'ok': True, 'result': True, 'description': 'Webhook was set'}

    response = await client_tgbot.sendMessage(CHAT_ID, "Hello from Telegram Bot!")
    print(response.status)  # 200
    print(response.payload) # {'ok': True, 'result': {'message_id': 786, 'from': {'id': ... } ... }


if __name__ == "__main__":
    asyncio.run_until_complete(main_async())

```


### Docs
1. How to publish pypi package [Medium article in Russian](https://medium.com/nuances-of-programming/python-%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-%D0%B2%D0%B0%D1%88%D0%B8%D1%85-%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%B2-pypi-11dd3216581c)


## Dependencies
This package depends on [devtud / pygramtic >= 0.2.0][link-pygramtic] package.


## Disclaimer

This project and its author is neither associated, nor affiliated with [Telegram](https://telegram.org/) in anyway.
See License section for more details.


## License

This project is released under the [GNU LESSER GENERAL PUBLIC LICENSE][link-license] License.

[link-author]: https://github.com/DmitriyKalekin
[link-repo]: https://github.com/DmitriyKalekin/python-telegram-bot-api
[link-pygramtic]: https://github.com/devtud/pygramtic
[link-issues]: https://github.com/DmitriyKalekin/python-telegram-bot-api/issues
[link-contributors]: https://github.com/DmitriyKalekin/python-telegram-bot-api/contributors
[link-docs]: https://telegram-bot-api.readme.io/docs
[link-license]: https://github.com/DmitriyKalekin/python-telegram-bot-api/blob/main/LICENSE
[link-telegram-bot-api]: https://core.telegram.org/bots
[link-awesome-telegram-bots]: https://github.com/telegram-bot-sdk/awesome-telegram-bots
