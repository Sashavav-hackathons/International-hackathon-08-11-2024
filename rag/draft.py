"""
Draft for testing syntax some methods
"""
#token = "t1.9euelZrLl4mKzpydic-XksaWkpvHku3rnpWanJLMlMeXnZGcmc7KypSVis_l8_cwf0VG-e9aKQVK_d3z93AtQ0b571opBUr9zef1656VmpySyZnOnseaiZ3HypCdiprH7_zF656VmpySyZnOnseaiZ3HypCdiprH.sbPvJ3yjHnnh3SuRiNp4UtE881ltLa-NctYlPQKBUMvHRpgs6geqbHO1seXU2DnZJHKaZBRNjZtj_DK4ktMWAw"
token = "t1.9euelZqKj53Kyc-PnMbGi5vMnJiLzO3rnpWanJLMlMeXnZGcmc7KypSVis_l8_d4fkVG-e8eNE5P_d3z9zgtQ0b57x40Tk_9zef1656VmpiZz5yOjI2VxpeVzonHzJmX7_zF656VmpiZz5yOjI2VxpeVzonHzJmX.AWCBHnNQHwrPff-bayw-OZdFMIWlnUr41OTPpECyBIzC53hbY7UyDkTCZcFKG-e07bIiPjMeWJg94BeFcPy3Cg"

import requests

# URL для API
url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

# Заголовки
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Данные запроса
data = {
    "modelUri": "gpt://bpf2qk3d4udr4rh05rni/yandexgpt/latest",
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
print(response.json())