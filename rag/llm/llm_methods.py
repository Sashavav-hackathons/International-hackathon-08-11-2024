import requests
from openai import OpenAI
from build.public_consts import *


def answer_with_documentation(doc_array: list[str] | str, query: str, **kwargs) -> str:
    """
    Функция ответа по документации
    :param doc_array: Текстовая документация, на которой должен основываться ответ
    :param query: Текстовый запрос к модели
    :param kwargs: Выбор между моделями, для работы с yandex_gpt нужно положить свой токен в поле yandex_gpt
    :return Текстовый ответ на поставленный вопрос по выданной документации
    """
    rules = RU_ANSWER_WITH_DOCUMENTATION

    documentation = "\n".join(doc_array)
    query = f"Ответь по предоставленной документации на запрос.\nДокументация:{documentation} Запрос: {query}"
    return choose_and_run_model(query=query, rules=rules, **kwargs)


def predict_answer(query: str, **kwargs) -> str:
    """
    Функция прогнозирования ответа
    :param query: Текстовый запрос к модели
    :param kwargs: Выбор между моделями, для работы с yandex_gpt нужно положить свой токен в поле yandex_gpt
    :return Текстовый ответ, представляющий прогноз реального ответа
    """
    rules = RU_PREDICT_ANSWER
    return choose_and_run_model(query=query, rules=rules, **kwargs)


def add_context_to_query(query: str, history: str, **kwargs) -> str:
    """
    Функция выделения нового вопроса из старых при их взаимосвязи
    :param query: Текущий вопрос
    :param history: История предыдущих вопросов
    :param kwargs: Выбор между моделями, для работы с yandex_gpt нужно положить свой токен в поле yandex_gpt
    :return Текстовый ответ, являющийся либо синтезом текущего вопроса с предыдущими, либо 'no data'
    """
    rules = RU_UPDATE_HISTORY
    query = f"Сказанное ранее: {history[history.find(':') + 1:history.find('|')]}. Текущий вопрос: " + query
    ans = choose_and_run_model(query=query, rules=rules, **kwargs)
    # print(ans)
    return ans


def choose_and_run_model(query: str, rules: str, **kwargs) -> str:
    """
    Функция выбора между моделями и их запуск
    :param query: Текстовый запрос
    :param rules: Набор правил, которым должна следовать генеративная модель
    :param kwargs: Выбор между моделями, для работы с yandex_gpt нужно положить свой токен в поле yandex_gpt
    :return Текстовый ответ на запрос с известными правилами
    """
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
    try:
        return response.json()['result']['alternatives'][0]['message']['text']
    except Exception as e:
        raise "Token is expired"