# Telegram Bot API - Python SDK (using aiohttp)

<p align="center">
<img src="https://img.shields.io/badge/tests-pytest-orange?style=for-the-badge" alt="pytest"/>
<img src="https://img.shields.io/badge/async-asyncio, aiohttp-green?style=for-the-badge" alt="asyncio, aiohttp"/>
<a href="https://t.me/herr_horror"><img src="https://img.shields.io/badge/Telegram Chat-@herr_horror-2CA5E0.svg?logo=telegram&style=for-the-badge" alt="Chat on Telegram"/></a>
<img src="https://img.shields.io/badge/version-v.0.0.1-green?style=for-the-badge" alt="Last Release"/>
</p>


Simple and fast client to call rest-api endpoints `api.telegram.org` using aiohttp package.  

View at:
`https://test.pypi.org/project/python-telegram-bot-api`


## How to install
```bash
pip3 install python-telegram-bot-api
```


## Usage
```python
import asyncio
from telegrambotapi import TgBotJson


TGBOT_TOKEN = "12345:YOUR_TOKEN"
APP_HOSTNAME = "https://YOUR_HOSTNAME.ngrok.io"
CHAT_ID = 123456789  # your chat id

client_tgbot = TgBotJson(token=TGBOT_TOKEN)


async def main_async():
    response = await app.client_tgbot.setWebhook("{hostname}/tgbot/wh".format(hostname=APP_HOSTNAME))
    r = await response.json()
    print(r)

    response = await app.client_tgbot.sendMessage(CHAT_ID, "Hello from Telegram Bot!")
    r = await response.json()
    print(r)


if __name__ == "__main__":
    asyncio.run_until_complete(main_async())

```


### Docs
1. How to publish pypi package [Medium article in Russian](https://medium.com/nuances-of-programming/python-%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-%D0%B2%D0%B0%D1%88%D0%B8%D1%85-%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%B2-pypi-11dd3216581c)



## Disclaimer

This project and its author is neither associated, nor affiliated with [Telegram](https://telegram.org/) in anyway.
See License section for more details.



## License

This project is released under the [GNU LESSER GENERAL PUBLIC LICENSE][link-license] License.

[link-author]: https://github.com/DmitriyKalekin
[link-repo]: https://github.com/DmitriyKalekin/python-telegram-bot-api
[link-issues]: https://github.com/DmitriyKalekin/python-telegram-bot-api/issues
[link-contributors]: https://github.com/DmitriyKalekin/python-telegram-bot-api/contributors
[link-docs]: https://telegram-bot-api.readme.io/docs
[link-license]: https://github.com/DmitriyKalekin/python-telegram-bot-api/blob/main/LICENSE
[link-telegram-bot-api]: https://core.telegram.org/bots
[link-awesome-telegram-bots]: https://github.com/telegram-bot-sdk/awesome-telegram-bots
