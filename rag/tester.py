import time
from rag import Rag
from chunker.chunker import Chunker
# from build.update_yandex_gpt_token import get_yandex_gpt_token


f = open("data/tests/test.txt", "r", encoding="utf-8")
questions = f.readlines()[160:]
output = ""

token = "t1.9euelZqSiYuSx42LlpmJjp6bx5CSnO3rnpWanJLMlMeXnZGcmc7KypSVis_l8_cVQz9G-e9cBm0__t3z91VxPEb571wGbT_-zef1656VmpiRypnHmpyXyJOSj5rNz46K7_zF656VmpiRypnHmpyXyJOSj5rNz46K.IHY3Rxlb7gdBdpeWe_MgwpGS_p4JHs_UZEMLF03e2fCylv8K--iutVT2OSg0rnyGoN06kJsj6Br7q0_EHg1LAg"
# token = get_yandex_gpt_token()
history = ""
chunker = Chunker()
for question in questions:
    start_time = time.time()
    res = Rag.static_query(question, token, chunker=chunker, history=history)
    history = res["history"]
    #print(res["answer"])
    #print(str(time.time() - start_time) + " seconds")
    text = res["answer"].replace("\n", " ")
    output += text + "\n"


fw = open("data/tests/ans.txt", "w", encoding='utf-8')
fw.write(output)