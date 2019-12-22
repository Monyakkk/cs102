import requests
import time
import json
from random import *

import config



def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 0.1
    for i in range (max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            time.sleep(delay)
            delay = min(backoff_factor * (2 ** i), timeout)
            
            

def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    #assert isinstance(user_id, int), "user_id must be positive integer"
    #assert isinstance(fields, str), "fields must be string"
    #assert user_id > 0, "user_id must be positive integer"

   
    domain = "https://api.vk.com/method"
    access_token = '224c7265815817046887a124c3fb93e19fd57180b84c00a7bb90e8ff45b88f8c5f0a8e0106c8380f5f6fe'
    v = '5.103'

    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = requests.get(query)
    friends = response.json()
    return friends


def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE




