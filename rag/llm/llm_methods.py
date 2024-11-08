from openai import OpenAI


def answer_with_documentation(doc_array: list[str] | str, query: str, client: OpenAI) -> str:
    """
    Helper function for answering on the question by the documentation that is provided.
    :param doc_array: documentation strings, that the result will be based on
    :param query: query with a question that is going to be searched in documentation strings
    :param client: language model that you want to generate text
    :return: string with an answer
    """
    rules = (
        "Always answer on russian. "
        "Formulate answers in the context of the documentation provided. "
        "Indicate if the request does not have an answer in the documentation. "
        "Formulate responses in a user-friendly way (e.g., a list if there are multiple items in the response). "
        "Provide examples of use cases if they are present in the documentation. "
        "Point to sections of the documentation that may be helpful in further exploring the question."
    )

    documentation = "\n".join(doc_array)
    query = f"Документация:{documentation} Запрос: {query}"
    return run_model(query=query, rules=rules, client=client)


def predict_answer(query: str, client: OpenAI) -> str:
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
    return run_model(query=query, rules=rules, client=client)


def run_model(query, rules, client):
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
