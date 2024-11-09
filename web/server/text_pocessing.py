import re

def remove_redundant_newlines(text):
    # Замена 5 и более подряд идущих переносов строки на один
    return re.sub(r'\n{5,}', '\n', text)
