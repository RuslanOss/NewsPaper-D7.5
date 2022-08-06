from django import template
import re

register = template.Library()

WORDS_TO_CATCH = [
    'пох',
    'полнейший',
    'Америке',
    'Рогозин',
    'дно',
    'гимн',
]



@register.filter()
def censor(text):

    new_text = re.sub(r'[^\w\s]', '', text)
    word_list = new_text.strip().split()
    new_stop_list = [x.lower() for x in WORDS_TO_CATCH]

    for word in word_list:
        word_len = len(word)
        if (word.lower() in new_stop_list) or (
                (word.lower()[-1] == 's') and (word.lower()[:word_len - 1] in new_stop_list)):
            substitute = word[0] + '*' * (len(word) - 2) + word[-1]  # about -> a***t
            text = text.replace(word, substitute)

    return text