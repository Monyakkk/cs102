# coding=utf-8
import pandas as pd
import requests
import textwrap
import gensim
import pymorphy2


from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamulticore import LdaModel
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()


stop_words = []



def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get 

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """

    code = {"owner_id": owner_id, "domain": domain, "offset": offset, "count": count, "filter": filter, "extended": extended, "fields": fields, "v": v}
    access_token = 'f4ef6e136dcf4940d22b88efb3ac94e0e6c320efc646a67654805178dcbd92518cc09625ee07ebe55421d'
    response = requests.post(url="https://api.vk.com/method/execute", data={"code": f'return API.wall.get({code});', "access_token": access_token, "v": v})

    result = response.json()
    return result

def prep_text(wall, count: int) -> list:
    text = ''
    for i in range(count):
        try:
            text += wall['response']['items'][i]['text']
            text += ' '
        except IndexError:
            pass
        
    new = ''
    for c in text:
        if c.isalpha() is True or c == ' ':
            new += c
        if c == '\n':
            new += ' '
            
    textlist = text.split()
    result = []
    for w in textlist:
        if 'https://' not in w and '#'  not in w and 'http://' not in w and w not in stop_words:
            result.append(morph.parse(w)[0].normal_form) 
   
    return result

def LDA(textlist: list, num_topics: int):
    textlist = [textlist]
    common_dictionary = Dictionary(textlist)
    common_corpus = [common_dictionary.doc2bow(text) for text in textlist]
    lda = LdaModel(common_corpus, num_topics=num_topics)
    return lda









    
    
