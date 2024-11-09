import requests
from private_consts import YANDEX_TOKEN

# URL для API
url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

# Данные для запроса
data = {
    "yandexPassportOauthToken": YANDEX_TOKEN
}

# Выполнение POST-запроса
response = requests.post(url, json=data)
token = response.json()['iamToken']
# Печать результата
print(response.json())

#token ="t1.9euelZrJkIqWmZ6PnJHGysqXnJzMj-3rnpWanJLMlMeXnZGcmc7KypSVis_l9PcUJUNG-e8rXWej3fT3VFNARvnvK11no83n9euelZrLyZXJk4-PxpmTl8ubj8iQmO_8xeuelZrLyZXJk4-PxpmTl8ubj8iQmA.awrGoLmv2tpbtpsOtVzYFNaWtwoGqSi2DbKvUPQ37Lm3cUVJNWyCJx_6oN23HuO7sQ0D2qsN-Nfo3edqn4OpAg"


# URL для API
url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

# Заголовки
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Данные запроса
data = {
    "modelUri": "gpt://b1gjp5vama10h4due384/yandexgpt/latest",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": 2000
    },
    "messages": [
        {
            "role": "system",
            "text": "Ты — умный ассистент."
        },
        {
            "role": "user",
            "text": "Назови любые три группы товаров в магазине техники!"
        }
    ]
}

# Выполнение запроса
response = requests.post(url, headers=headers, json=data)

# Печать результата
print(response.json()['result'])
