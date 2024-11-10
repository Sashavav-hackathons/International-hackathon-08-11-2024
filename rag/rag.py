import os
import time

from openai import OpenAI

from llm.llm_methods import answer_with_documentation, predict_answer, is_need_history
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
        self.token = "t1.9euelZqSiYuSx42LlpmJjp6bx5CSnO3rnpWanJLMlMeXnZGcmc7KypSVis_l8_cVQz9G-e9cBm0__t3z91VxPEb571wGbT_-zef1656VmpiRypnHmpyXyJOSj5rNz46K7_zF656VmpiRypnHmpyXyJOSj5rNz46K.IHY3Rxlb7gdBdpeWe_MgwpGS_p4JHs_UZEMLF03e2fCylv8K--iutVT2OSg0rnyGoN06kJsj6Br7q0_EHg1LAg"

        project_root = root_path(ignore_cwd=False)
        self.project_root = project_root
        self.k = 2
        self.chunker = Chunker(project_root)
        self.history = ""

    def query(self, q: str) -> str:
        """
        Main function that searches answer to the query in the documentation
        :param q: query, that you want to search
        :return: answer to the query
        """
        # self.history = self.history \
        #    if self.history != "" and is_need_history(q, history=self.history, yandex_gpt=self.token) else ""
        new_q = is_need_history(q, history=self.history, yandex_gpt=self.token)
        if new_q.find("no data") == -1:
            q = new_q
        else:
            self.history = ""
        q_gen = predict_answer(q, yandex_gpt=self.token)
        q_docs = self.search_in_documents(q)
        q_docs = q_docs if isinstance(q_docs, list) else [q_docs]
        q_gen_docs = self.search_in_documents(q_gen)
        q_gen_docs = q_gen_docs if isinstance(q_gen_docs, list) else [q_gen_docs]
        q_docs.extend(q_gen_docs)
        answer = answer_with_documentation(q_docs, q, yandex_gpt=self.token)
        self.history += f"Вопрос: {q}| Ответ: {answer}\n"
        return answer if answer.find("К сожалению, я") == -1 else "К сожалению, я не владею данной информацией."

    def search_in_documents(self, q: str) -> list[str]:
        res = self.chunker.find_best_in_db(query=q, k=self.k)
        return res

    def create_db(self):
        self.chunker.create_chunk_db()

    def add_file(self, path: str):
        self.chunker.add_file(path)
