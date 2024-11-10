import time
from rag import Rag
from chunker.chunker import Chunker


#rag = Rag()
# rag.create_db()
#path = "D:\\Backup\\Less Important\\My programs\\Git\\International-hackathon-08-11-2024\\rag\\data\\new_files\\Henry.txt"
# rag.add_file(path)
questions = (["В какие в года правил Генрих 13?",
              "Как за 5 лет изменилось количество телепрограмм, привлекающих более 4-х млн. зрителей в Великобритании",
              "А за десять?",
              "Сколько заработал Amazon на рекламе в 2023 году",
              "А за 4 квартала до августа 2023 года?",
              "Что входит в экосистему MediaDesk?"])

helper = Rag()
token = helper.token
history = helper.history
chunker = Chunker()
for question in questions:
    start_time = time.time()
    res = Rag.static_query(question, token, chunker=chunker, history=history)
    history = res["history"]
    print(res["answer"])
    print(str(time.time() - start_time) + " seconds")