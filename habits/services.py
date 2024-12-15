import requests

from config.settings import BOT_TOKEN, TELEGRAM_URL, BOT_ID


def send_tg_message(text, chat_id):
    """ Отправка сообщения на Телеграм"""

    params = {
        'text': text,
        'chat_id': chat_id,
    }
    requests.get(f'{TELEGRAM_URL}{BOT_TOKEN}/sendMessage', params=params)


def get_chat_id(username_tg):
    """ Получение chat_id Телеграм по username (если пользователь взаимодействовал с telegram_bot)"""

    response = requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/getUpdates", params={"chat_id": BOT_ID})
    data = response.json()
    chat_id = None
    if data['ok']:
        updates = data['result']
        for update in updates:
            if 'message' in update:
                if update['message']['chat']['username'] == username_tg[1:]:
                    chat_id = update['message']['chat']['id']
    return chat_id
