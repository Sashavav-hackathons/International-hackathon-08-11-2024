import time
from rag import Rag


rag = Rag()
# rag.create_db()
path = "D:\\Backup\\Less Important\\My programs\\Git\\International-hackathon-08-11-2024\\rag\\data\\new_files\\Henry.txt"
# rag.add_file(path)
questions = (["В какие в года правил Генрих 13?",
              "Как за 5 лет изменилось количество телепрограмм, привлекающих более 4-х млн. зрителей в Великобритании",
              "А за десять?",
              "Сколько заработал Amazon на рекламе в 2023 году",
              "А за 4 квартала до августа 2023 года?",
              "Что входит в экосистему MediaDesk?"])

for question in questions:
    start_time = time.time()
    print(rag.query(question))
    print(str(time.time() - start_time) + " seconds")
