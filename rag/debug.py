import time
from rag import Rag
from chunker.chunker import Chunker
from build.update_yandex_gpt_token import get_yandex_gpt_token

questions = (["В какие в года правил Генрих 13?",
              "Как за 5 лет изменилось количество телепрограмм, привлекающих более 4-х млн. зрителей в Великобритании",
              "А за десять?",
              "Сколько заработал Amazon на рекламе в 2023 году",
              "А за 4 квартала до августа 2023 года?",
              "Что входит в экосистему MediaDesk?"])

#token = "t1.9euelZqSiYuSx42LlpmJjp6bx5CSnO3rnpWanJLMlMeXnZGcmc7KypSVis_l8_cVQz9G-e9cBm0__t3z91VxPEb571wGbT_-zef1656VmpiRypnHmpyXyJOSj5rNz46K7_zF656VmpiRypnHmpyXyJOSj5rNz46K.IHY3Rxlb7gdBdpeWe_MgwpGS_p4JHs_UZEMLF03e2fCylv8K--iutVT2OSg0rnyGoN06kJsj6Br7q0_EHg1LAg"
token = get_yandex_gpt_token()
history = ""
chunker = Chunker()
for question in questions:
    start_time = time.time()
    res = Rag.static_query(question, token, chunker=chunker, history=history)
    history = res["history"]
    print(res["answer"])
    print(str(time.time() - start_time) + " seconds")