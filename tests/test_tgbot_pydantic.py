import pytest
from pygramtic.models import Update, Message, WebhookInfo, ChatMember
from typing import List
from api_tgbot import TgException
import logging


@pytest.mark.asyncio
async def test_getWebhookInfo_empty_wh(client_tgbot_pydantic, mock_aioresponse):
    JSON_EMPTY_WH = {'ok': True, 'result': {'url': '', 'has_custom_certificate': False, 'pending_update_count': 0}}
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/getWebhookInfo", payload=JSON_EMPTY_WH)

    response = await client_tgbot_pydantic.getWebhookInfo()

    assert type(response) == WebhookInfo
    assert response == WebhookInfo.parse_obj(JSON_EMPTY_WH["result"])


@pytest.mark.asyncio
async def test_deleteWebhook(client_tgbot_pydantic, mock_aioresponse):
    URL = f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/deleteWebhook"
    JSON_FIRST = {'ok': True, 'result': True, 'description': 'Webhook was deleted'}
    JSON_SECOND = {'ok': True, 'result': True, 'description': 'Webhook is already deleted'}
    mock_aioresponse.get(URL, payload=JSON_FIRST)
    mock_aioresponse.get(URL, payload=JSON_SECOND)
    mock_aioresponse.get(URL, payload=JSON_SECOND)

    response1 = await client_tgbot_pydantic.deleteWebhook()
    response2 = await client_tgbot_pydantic.deleteWebhook()
    response3 = await client_tgbot_pydantic.deleteWebhook()

    assert response1 == True
    assert response2 == True
    assert response3 == True


@pytest.mark.parametrize(
    "error, wh_url, json_response", [
        [
            TgException,
            "http://12345wrongurl/tg/wh",
            {'ok': False, 'error_code': 400,
             'description': 'Bad Request: bad webhook: Failed to resolve host: No address associated with hostname'},
        ],
    ]
)
@pytest.mark.asyncio
async def test_setWebhook_exceptions(client_tgbot_pydantic, mock_aioresponse, error, wh_url, json_response):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/setWebhook?url=" + str(wh_url), payload=json_response)
    with pytest.raises(error) as e:
        response = await client_tgbot_pydantic.setWebhook(wh_url)
    assert type(e.value) == error
    assert str(e.value) == json_response["description"]
    # assert getattr(e, 'message', repr(e))


@pytest.mark.parametrize(
    "wh_url, json_response", [
        [
            "https://ffe88ca28f0c.ngrok.io/tg/wh",
            {'ok': True, 'result': True, 'description': 'Webhook was set'},
        ],
        [
            "https://ffe88ca28f0c.ngrok.io/tg/wh",
            {'ok': True, 'result': True, 'description': 'Webhook is already set'},
        ]
    ]
)
@pytest.mark.asyncio
async def test_setWebhook(client_tgbot_pydantic, mock_aioresponse, wh_url, json_response):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/setWebhook?url=" + str(wh_url), payload=json_response)

    response = await client_tgbot_pydantic.setWebhook(wh_url)

    assert type(response) == bool
    assert response == json_response["result"]


@pytest.mark.parametrize(
    "wh_url, json_wh_status", [
        [
            "http://12345wrongurl/tg/wh",
            {'ok': True, 'result': {'url': '', 'has_custom_certificate': False, 'pending_update_count': 0}}
        ],
        [
            "https://ffe88ca28f0c.ngrok.io/tg/wh",
            {'ok': True, 'result': {'url': 'https://ffe88ca28f0c.ngrok.io/tg/wh', 'has_custom_certificate': False,
                                    'pending_update_count': 0, 'max_connections': 40, 'ip_address': '3.134.125.175'}}
        ],
        [
            "https://ffe88ca28f0c.ngrok.io/tg/wh",
            {'ok': True, 'result': {'url': 'https://ffe88ca28f0c.ngrok.io/tg/wh', 'has_custom_certificate': False,
                                    'pending_update_count': 0, 'max_connections': 40, 'ip_address': '3.134.125.175'}}
        ]
    ]
)
@pytest.mark.asyncio
async def test_getWebhhokInfo(client_tgbot_pydantic, mock_aioresponse, wh_url, json_wh_status):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/getWebhookInfo", payload=json_wh_status)

    response = await client_tgbot_pydantic.getWebhookInfo()

    assert type(response) == WebhookInfo
    assert response == WebhookInfo.parse_obj(json_wh_status["result"])



@pytest.mark.parametrize(
    "error, json_response", [
        [TgException, {'ok': False, 'error_code': 409,
               'description': "Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first"}],
    ]
)
@pytest.mark.asyncio
async def test_getUpdates_exceptions(client_tgbot_pydantic, mock_aioresponse, error, json_response):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/getUpdates", payload=json_response)

    with pytest.raises(error) as e:
        response = await client_tgbot_pydantic.getUpdates()
    assert type(e.value) == error
    assert str(e.value) == json_response["description"]

@pytest.mark.parametrize(
    "json_updates", [
        {'ok': True, 'result': []},
        {'ok': True, 'result': [{'update_id': 12210570, 'message': {'message_id': 785,
                                                                          'from': {'id': 435627225, 'is_bot': False,
                                                                                   'first_name': 'Дмитрий',
                                                                                   'last_name': 'Калекин',
                                                                                   'username': 'herr_horror',
                                                                                   'language_code': 'en'},
                                                                          'chat': {'id': 435627225,
                                                                                   'first_name': 'Дмитрий',
                                                                                   'last_name': 'Калекин',
                                                                                   'username': 'herr_horror',
                                                                                   'type': 'private'},
                                                                          'date': 1605745560, 'text': 'привет'}}]},
    ]
)
@pytest.mark.asyncio
async def test_getUpdates(client_tgbot_pydantic, mock_aioresponse, json_updates):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/getUpdates", payload=json_updates)

    response = await client_tgbot_pydantic.getUpdates()

    assert type(response) == list
    assert response == [Update.parse_obj(obj) for obj in json_updates["result"]]


@pytest.mark.parametrize(
    "error_code, txt, json_response", [
        [200, "new_text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782835, 'text': 'new_text'}}],
        [200, "new.text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782836, 'text': 'new.text'}}],
    ])
@pytest.mark.asyncio
async def test_sendMessage(client_tgbot_pydantic, mock_aioresponse, error_code, txt, json_response):
    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/sendMessage", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/sendMessage", status=error_code,  payload=json_response)

    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/sendMessage", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/sendMessage", status=error_code,  payload=json_response)



    response1 = await client_tgbot_pydantic.sendMessage(435627225, txt)
    response2 = await client_tgbot_pydantic.sendMessage(435627225, txt, parse_mode="markdown")

    assert type(response1) == Message
    assert response1 == Message.parse_obj(json_response["result"])
    assert type(response2) == Message
    assert response2 == Message.parse_obj(json_response["result"])



@pytest.mark.parametrize(
    "error, msg_id, json_response", [
        [TgException, 99999, {'ok': False, 'error_code': 400, 'description': 'Bad Request: message to delete not found'}],
    ])
@pytest.mark.asyncio
async def test_deleteMessage_exception(client_tgbot_pydantic, mock_aioresponse, error, msg_id, json_response):
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/deleteMessage", payload=json_response)

    with pytest.raises(error) as e:
        response = await client_tgbot_pydantic.deleteMessage(435627225, msg_id)
    assert type(e.value) == error
    assert str(e.value) == json_response["description"]


@pytest.mark.parametrize(
    "msg_id, json_response", [
        [785, {'ok': True, 'result': True}],
    ])
@pytest.mark.asyncio
async def test_deleteMessage(client_tgbot_pydantic, mock_aioresponse, msg_id, json_response):
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/deleteMessage", payload=json_response)

    response = await client_tgbot_pydantic.deleteMessage(435627225, msg_id)

    assert type(response) == bool
    assert response == json_response["result"]

@pytest.mark.parametrize(
    "error, msg_id, txt, json_response", [
        [TgException, 99999, "new.txt", {'ok': False, 'error_code': 400, 'description': 'Bad Request: message to edit not found'}],
    ])
@pytest.mark.asyncio
async def test_editMessageText_exceptions(client_tgbot_pydantic, mock_aioresponse, error, msg_id, txt, json_response):
    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText",  payload=json_response)

    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText", payload=json_response)


    with pytest.raises(error) as e:
        response1 = await client_tgbot_pydantic.editMessageText(435627225, msg_id, txt)
    assert type(e.value) == error
    assert str(e.value) == json_response["description"]

    with pytest.raises(error):
        response2 = await client_tgbot_pydantic.editMessageText(435627225, msg_id, txt, parse_mode="markdown")
    assert type(e.value) == error
    assert str(e.value) == json_response["description"]

@pytest.mark.parametrize(
    "msg_id, txt, json_response", [
        [786, "new_text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782835, 'text': 'new_text'}}],
        [786, "new.text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782836, 'text': 'new.text'}}],
    ])
@pytest.mark.asyncio
async def test_editMessageText(client_tgbot_pydantic, mock_aioresponse, msg_id, txt, json_response):
    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText",  payload=json_response)

    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_pydantic.token}/editMessageText", payload=json_response)


    response1 = await client_tgbot_pydantic.editMessageText(435627225, msg_id, txt)

    response2 = await client_tgbot_pydantic.editMessageText(435627225, msg_id, txt, parse_mode="markdown")

    assert type(response1) == Message
    assert response1 == Message.parse_obj(json_response["result"])
    assert type(response2) == Message
    assert response2 == Message.parse_obj(json_response["result"])