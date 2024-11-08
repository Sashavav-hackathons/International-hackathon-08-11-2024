import os
import time

from openai import OpenAI

from llm.llm_methods import answer_with_documentation, predict_answer
from chunker.chunker import Chunker
from get_project_root import root_path


class Rag:
    """
    Main class for Rag model
    """

    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
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
        q_gen = predict_answer(q, self.client)
        q_docs = self.search_in_documents(q)
        q_docs = q_docs if isinstance(q_docs, list) else [q_docs]
        q_gen_docs = self.search_in_documents(q_gen)
        q_gen_docs = q_gen_docs if isinstance(q_gen_docs, list) else [q_gen_docs]
        q_docs.extend(q_gen_docs)
        answer = answer_with_documentation(q_docs, q, self.client)
        return answer

    def search_in_documents(self, q: str) -> list[str]:
        res = self.chunker.find_best_in_db(query=q, k=self.k)
        return res


rag = Rag()
#print(rag.query("Сколько месяцев в году?"))
#print(rag.search_in_documents("Кто такой Генрих 13"))
#print(rag.chunker.create_chunk_db())
#print(rag.search_in_documents(""))
start_time = time.time()
question = "В какие в года правил Генрих 13?"
print(rag.query(question))
print(str(time.time() - start_time) + " seconds")
start_time = time.time()
question = "В какие в года правил Генрих 13?"
print(rag.query(question))
print(str(time.time() - start_time) + " seconds")
start_time = time.time()
question = "Кто такой Михаил Мерзликин?"
print(rag.query(question))
print(str(time.time() - start_time) + " seconds")
start_time = time.time()
question = "Основные столпы RAG архитектуры"
print(rag.query(question))
print(str(time.time() - start_time) + " seconds")