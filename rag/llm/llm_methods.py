import requests
from openai import OpenAI
from build.public_consts import *


def answer_with_documentation(doc_array: list[str] | str, query: str, history: str = "", **kwargs) -> str:
    rules = RU_ANSWER_WITH_DOCUMENTATION

    documentation = "\n".join(doc_array)
    rules += f"Если запрос не является самостоятельным, то используй историю переписки: {history} " if history else ""
    query = f"Ответь по предоставленной документации на запрос.\nДокументация:{documentation} Запрос: {query}"
    return choose_and_run_model(query=query, rules=rules, **kwargs)


def predict_answer(query: str, history: str = "", **kwargs) -> str:
    rules = RU_PREDICT_ANSWER
    rules += (f"Если ты затрудняешься сгенерировать примерный ответ, то постарайся использовать историю переписки: "
              f"{history} ") if history else ""
    return choose_and_run_model(query=query, rules=rules, **kwargs)


def is_need_history(query: str, history: str, **kwargs) -> str:
    rules = RU_UPDATE_HISTORY
    query = f"Сказанное ранее: {history[history.find(':') + 1:history.find('|')]}. Текущий вопрос: {query}"
    ans = choose_and_run_model(query=query, rules=rules, **kwargs)
    # print(ans)
    return ans


def choose_and_run_model(query: str, rules: str, **kwargs) -> str:
    if kwargs.__contains__("llama"):
        return run_llama_model(query=query, rules=rules, client=kwargs["llama"])
    elif kwargs.__contains__("yandex_gpt"):
        return run_yandex_gpt_model(query=query, rules=rules, token=kwargs["yandex_gpt"])
    else:
        return "This model does not exist"


def run_llama_model(query: str, rules: str, client: OpenAI) -> str:
    completion = client.chat.completions.create(
        model="model-identifier",
        messages=[
            {"role": "system", "content": rules},
            {"role": "user", "content": query}
        ],
        temperature=0.7,
    )

    response = completion.choices[0].message.content
    return response


def run_yandex_gpt_model(query: str, rules: str, token: str) -> str:
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
                "text": rules
            },
            {
                "role": "user",
                "text": query
            }
        ]
    }
    # print(query)
    # Выполнение запроса
    response = requests.post(url, headers=headers, json=data)

    # Печать результата
    return response.json()['result']['alternatives'][0]['message']['text']
