import requests
from build.private_consts import YANDEX_TOKEN


def get_yandex_gpt_token():
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

    # Данные для запроса
    data = {
        "yandexPassportOauthToken": YANDEX_TOKEN
    }

    # Выполнение POST-запроса
    response = requests.post(url, json=data)
    token = response.json()['iamToken']
    return token
