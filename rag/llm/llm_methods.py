import requests
from openai import OpenAI


def answer_with_documentation(doc_array: list[str] | str, query: str, history: str="", **kwargs) -> str:
    """
    Helper function for answering on the question by the documentation that is provided.
    :param doc_array: documentation strings, that the result will be based on
    :param query: query with a question that is going to be searched in documentation strings
    :param client: language model that you want to generate text
    :return: string with an answer
    """
    rules = (
        "Always follow the ruleset.\n"
        "Ruleset: \n"
        "Style:"
        " Always answer on russian. "
        "Formulate answers in the context of the documentation provided. "
        "Format text like this: Alex has 20 friends, his friend says \"Alex has 20 friends\"[1]\n[1] - "
        "from 2.pdf on page 3, dated on 2020-11-20. "
        "Rules: "
        "If you do not know the answer, you should say: 'Извините, я не обладаю достаточной информацией, "
        "чтобы ответить на данный запрос. '\n And nothing else. "
        "Formulate responses in a user-friendly way (e.g., a list if there are multiple items in the response). "
        "Provide examples of use cases if they are present in the documentation. "
        "Point to sections of the documentation that may be helpful in further exploring the question. "
        "If there is more than one answer choice in the documentation, choose the most appropriate option. "
        "If the question asked is not related to the previous question, the dialog history should be cleared. "
        "Use only information from the documentation for your answers. Do not use data from your past trainings. "
        "If no answer to the question posed is found in the documentation provided, then report: "
        "'The documentation provided does not answer the question you have asked' and nothing else. "
        "Respond concisely to the given query without deviations. "
        "Include with your answer a link to which file the answer is located, on which page, "
        "and the date the file was created. For example: Question: What is the capital of Portugal? "
        "Your answer: Answer to the question: Lisbon. File name: file.name. "
        "The date the document was created: 2024-01-01. Page: 2. "
    )

    documentation = "\n".join(doc_array)
    rules += f"Если запрос не является самостоятельным, то используй историю переписки: {history} " if history else ""
    query = f"Документация:{documentation} Запрос: {query}"
    return choose_and_run_model(query=query, rules=rules, **kwargs)


def predict_answer(query: str, history: str="", **kwargs) -> str:
    """
    Function that predicts the answer even to make a better search
    :param query: string with a query
    :param client: OpenAI language model that you want to generate text
    :return: string with an answer
    """
    rules = (
        "Always answer on russian. "
        "Assume that you know an answer for my question. "
        "Try to predict the answer to my question. "
        "Do not tell me that you don't know the correct answer, cause you don't. "
        "Say only the predicted answer and nothing else. "
    )
    rules += (f"Если ты затрудняешься сгенерировать примерный ответ, то постарайся использовать историю переписки: "
              f"{history} ") if history else ""
    return choose_and_run_model(query=query, rules=rules, **kwargs)


def is_need_history(query: str, history: str, **kwargs) -> bool:
    rules = (
        "У тебя всего одна задача: \n"
        "Напиши TRUE, если вопрос относится к сказанному ранее. \n"
        "Напиши FALSE, если вопрос не относится к сказанному ранее. \n"
        "Итого твой ответ - одно слово: TRUE/FALSE"
    )
    query = f"Сказанное ранее: {history}. \n---------------\nТекущий вопрос {query}"
    ans = choose_and_run_model(query=query, rules=rules, **kwargs)
    # print(ans)
    return ans.find("TRUE") > -1


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

    # Выполнение запроса
    response = requests.post(url, headers=headers, json=data)

    # Печать результата
    return response.json()['result']['alternatives'][0]['message']['text']
