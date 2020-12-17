import pytest


@pytest.mark.asyncio
async def test_getWebhookInfo_empty_wh(client_tgbot_json, mock_aioresponse):
    JSON_EMPTY_WH = {'ok': True, 'result': {'url': '', 'has_custom_certificate': False, 'pending_update_count': 0}}
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_json.token}/getWebhookInfo", payload=JSON_EMPTY_WH)

    response = await client_tgbot_json.getWebhookInfo()

    assert response.status == 200
    assert response.payload == JSON_EMPTY_WH


@pytest.mark.asyncio
async def test_deleteWebhook(client_tgbot_json, mock_aioresponse):
    URL = f"https://api.telegram.org/bot{client_tgbot_json.token}/deleteWebhook"
    JSON_FIRST = {'ok': True, 'result': True, 'description': 'Webhook was deleted'}
    JSON_SECOND = {'ok': True, 'result': True, 'description': 'Webhook is already deleted'}
    mock_aioresponse.get(URL, payload=JSON_FIRST)
    mock_aioresponse.get(URL, payload=JSON_SECOND)
    mock_aioresponse.get(URL, payload=JSON_SECOND)

    response1 = await client_tgbot_json.deleteWebhook()
    response2 = await client_tgbot_json.deleteWebhook()
    response3 = await client_tgbot_json.deleteWebhook()

    assert response1.status == 200
    assert response1.payload == JSON_FIRST
    assert response2.status == 200
    assert response2.payload == JSON_SECOND
    assert response3.status == 200
    assert response3.payload == JSON_SECOND


@pytest.mark.parametrize(
    "wh_url, json_response", [
        [
            "http://12345wrongurl/tg/wh",
            {'ok': False, 'error_code': 400,
             'description': 'Bad Request: bad webhook: Failed to resolve host: No address associated with hostname'},
        ],
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
async def test_setWebhook(client_tgbot_json, mock_aioresponse, wh_url, json_response):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_json.token}/setWebhook?url=" + str(wh_url), payload=json_response)

    response = await client_tgbot_json.setWebhook(wh_url)

    assert response.status == 200
    assert response.payload == json_response


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
async def test_getWebhhokInfo(client_tgbot_json, mock_aioresponse, wh_url, json_wh_status):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_json.token}/getWebhookInfo", payload=json_wh_status)

    response2 = await client_tgbot_json.getWebhookInfo()

    assert response2.status == 200
    assert response2.payload == json_wh_status


# @pytest.mark.asyncio
# async def test_recreate_webhook(client_tgbot_json, mock_aioresponse):
#     wh_url = "https://ffe88ca28f0c.ngrok.io/tg/wh"
#     JSON_DELETE = {'ok': True, 'result': True, 'description': 'Webhook was deleted'}
#     JSON_SET = {'ok': True, 'result': True, 'description': 'Webhook was set'}
#     JSON_INFO = {'ok': True, 'result': {'url': 'https://ffe88ca28f0c.ngrok.io/tg/wh', 'has_custom_certificate': False,
#                                         'pending_update_count': 0, 'max_connections': 40,
#                                         'ip_address': '3.134.125.175'}}
#
#     mock_aioresponse.get( f"https://api.telegram.org/bot{client_tgbot_json.token}/deleteWebhook", payload=JSON_DELETE)
#     mock_aioresponse.get( f"https://api.telegram.org/bot{client_tgbot_json.token}/setWebhook?url=" + str(wh_url), payload=JSON_SET)
#     mock_aioresponse.get( f"https://api.telegram.org/bot{client_tgbot_json.token}/getWebhookInfo", payload=JSON_INFO)
#
#     response = await client_tgbot_json.recreate_webhook(wh_url)
#
#     assert response.status == 200
#     assert response.payload == JSON_INFO


@pytest.mark.parametrize(
    "error_code, json_updates", [
        [409, {'ok': False, 'error_code': 409,
               'description': "Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first"}],
        [200, {'ok': True, 'result': []}],
        [200, {'ok': True, 'result': [{'update_id': 12210570, 'message': {'message_id': 785,
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
                                                                          'date': 1605745560, 'text': 'привет'}}]}],
    ]
)
@pytest.mark.asyncio
async def test_getUpdates(client_tgbot_json, mock_aioresponse, error_code, json_updates):
    mock_aioresponse.get(f"https://api.telegram.org/bot{client_tgbot_json.token}/getUpdates", status=error_code, payload=json_updates)

    response = await client_tgbot_json.getUpdates()

    assert response.status == error_code
    assert response.payload == json_updates



@pytest.mark.parametrize(
    "error_code, txt, json_response", [
        [200, "new_text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782835, 'text': 'new_text'}}],
        [200, "new.text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782836, 'text': 'new.text'}}],
    ])
@pytest.mark.asyncio
async def test_sendMessage(client_tgbot_json, mock_aioresponse, error_code, txt, json_response):
    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/sendMessage", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/sendMessage", status=error_code,  payload=json_response)

    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/sendMessage", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/sendMessage", status=error_code,  payload=json_response)



    response1 = await client_tgbot_json.sendMessage(435627225, txt)
    response2 = await client_tgbot_json.sendMessage(435627225, txt, parse_mode="markdown")

    assert response1.status == error_code
    assert response1.payload == json_response
    assert response2.status == error_code
    assert response2.payload == json_response



@pytest.mark.parametrize(
    "error_code, msg_id, json_response", [
        [400, 99999, {'ok': False, 'error_code': 400, 'description': 'Bad Request: message to delete not found'}],
        [200, 785, {'ok': True, 'result': True}],
    ])
@pytest.mark.asyncio
async def test_deleteMessage(client_tgbot_json, mock_aioresponse, error_code, msg_id, json_response):
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/deleteMessage", status=error_code,  payload=json_response)

    response = await client_tgbot_json.deleteMessage(435627225, msg_id)

    assert response.status == error_code
    assert response.payload == json_response

@pytest.mark.parametrize(
    "error_code, msg_id, txt, json_response", [
        [400, 99999, "new.txt", {'ok': False, 'error_code': 400, 'description': 'Bad Request: message to edit not found'}],
        [200, 786, "new_text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782835, 'text': 'new_text'}}],
        [200, 786, "new.text", {'ok': True, 'result': {'message_id': 786, 'from': {'id': 1357535845, 'is_bot': True, 'first_name': 'support-bot', 'username': 'AmoSupportBot'}, 'chat': {'id': 435627225, 'first_name': 'Дмитрий', 'last_name': 'Калекин', 'username': 'herr_horror', 'type': 'private'}, 'date': 1605747017, 'edit_date': 1605782836, 'text': 'new.text'}}],
    ])
@pytest.mark.asyncio
async def test_editMessageText(client_tgbot_json, mock_aioresponse, error_code, msg_id, txt, json_response):
    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/editMessageText", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/editMessageText", status=error_code,  payload=json_response)

    if "_" in txt:
        # wrong markdown causes second attempt to call POST
        mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/editMessageText", status=400,
                              payload={'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 3"})
    mock_aioresponse.post(f"https://api.telegram.org/bot{client_tgbot_json.token}/editMessageText", status=error_code,  payload=json_response)



    response1 = await client_tgbot_json.editMessageText(435627225, msg_id, txt)
    response2 = await client_tgbot_json.editMessageText(435627225, msg_id, txt, parse_mode="markdown")

    assert response1.status == error_code
    assert response1.payload == json_response
    assert response2.status == error_code
    assert response2.payload == json_response