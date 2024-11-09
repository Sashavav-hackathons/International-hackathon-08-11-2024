import os
import time

from openai import OpenAI

from llm.llm_methods import answer_with_documentation, predict_answer
from chunker.chunker import Chunker
from get_project_root import root_path
from build.local_variables import YANDEX_GPT_TOKEN


class Rag:
    """
    Main class for Rag model
    """

    def __init__(self):
        # self.client = OpenAI(base_url="http://192.168.1.70:1234/v1", api_key="lm-studio")
        # TODO TOKEN UPDATE
        # self.token = YANDEX_GPT_TOKEN
        self.token = "t1.9euelZrKyJzKk5CMnpqYm8mdkozPlO3rnpWanJLMlMeXnZGcmc7KypSVis_l9PcHJEJG-e8XEias3fT3R1I_RvnvFxImrM3n9euelZqcjJual8nHjo7MioqJjJ6Kju_8xeuelZqcjJual8nHjo7MioqJjJ6Kjg.pKjVRowuKOzHLq7YCT9Z0BAx_eukO7jpn3uHO7PNpRFZ95bktNUXCWcu9uzEVaaCNAeWmVgUaFkg6JSDour1Dg"
        project_root = root_path(ignore_cwd=False)
        self.project_root = project_root
        self.k = 5
        self.chunker = Chunker(project_root)

    def query(self, q: str) -> str:
        """
        Main function that searches answer to the query in the documentation
        :param q: query, that you want to search
        :return: answer to the query
        """
        q_gen = predict_answer(q, yandex_gpt=self.token)
        q_docs = self.search_in_documents(q)
        q_docs = q_docs if isinstance(q_docs, list) else [q_docs]
        q_gen_docs = self.search_in_documents(q_gen)
        q_gen_docs = q_gen_docs if isinstance(q_gen_docs, list) else [q_gen_docs]
        q_docs.extend(q_gen_docs)
        answer = answer_with_documentation(q_docs, q, yandex_gpt=self.token)
        return answer

    def search_in_documents(self, q: str) -> list[str]:
        res = self.chunker.find_best_in_db(query=q, k=self.k)
        return res

    def create_db(self):
        self.chunker.create_chunk_db()


rag = Rag()
questions = (["В какие в года правил Генрих 13?",
              "Как за 10 лет изменилось количество телепрограмм, привлекающих более 4-х млн. зрителей в Великобритании",
              "Сколько заработал амазон на рекламе в 2023 году",
              "Какая часть поколения Z считает, что стилизация их аватара в интернете важнее чем их стиль"
              " в реальной жизни? Какая динамика?",
              "Что говорит о человеке его аватар?",
              "Какой процент людей в возрасте от 18 до 64 лет считает, что лучше всего связываются с брендом,"
              " у которого есть уникальная аудио-идентичность?"])

for question in questions:
    start_time = time.time()
    print(rag.query(question))
    print(str(time.time() - start_time) + " seconds")
