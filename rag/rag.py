from get_project_root import root_path

from chunker.chunker import Chunker
from llm.llm_methods import answer_with_documentation, predict_answer, add_context_to_query


class Rag:
    """
    Основной класс, реализующий работу с RAG моделью
    """

    @staticmethod
    def static_query(q: str, token: str, chunker: Chunker = Chunker(),
                     k: int = 2, history: str = "") -> dict[str, str | Chunker]:
        """
        Метод получения ответа на запрос по имеющейся документации
        :param q: Текстовый вопрос по документации
        :param token: Токен доступа к модели Yandex GPT
        :param chunker: Объект класса Chunker, необходимый для работы с БД
        :param k: Количество искомых отрывков на один запрос
        :param history: Тестовый лог истории
        :return Словарь с ключами Answer и History в которых лежат обновленные ответ и история соответственно
        """
        new_q = add_context_to_query(q, history=history, yandex_gpt=token)
        if new_q.find("no data") == -1:
            q = new_q
        else:
            history = ""
        q_gen = predict_answer(q, yandex_gpt=token)
        q_docs = chunker.find_best_in_db(query=q, k=k)
        q_docs = q_docs if isinstance(q_docs, list) else [q_docs]
        q_gen_docs = chunker.find_best_in_db(query=q_gen, k=k)
        q_gen_docs = q_gen_docs if isinstance(q_gen_docs, list) else [q_gen_docs]
        q_docs.extend(q_gen_docs)
        answer = answer_with_documentation(q_docs, q, yandex_gpt=token)
        history += f"Вопрос: {q}| Ответ: {answer}\n"
        res = dict()
        res["answer"] = answer if answer.find("К сожалению, я") == -1 else ("К сожалению, я не владею данной "
                                                                            "информацией.")
        res["history"] = history
        return res

    @staticmethod
    def push_new_files_to_db(chunker: Chunker = Chunker()):
        """
        Метод добавления всех элементов папки rag/data/new_files в БД
        :param chunker: Объект класса Chunker для работы с векторной БД
        """
        chunker.add_file()
