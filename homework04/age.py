import requests
import json
from datetime import datetime 
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id, 'bdate')
    ages = []
    for i in range(friends['response']['count']):
        try:
            birth_date = friends['response']['items'][i]['bdate']
            day, month, year = birth_date.split('.')
            day, month, year = int(day), int(month), int(year)
        except (KeyError, ValueError) as e:
            continue

        current_month, current_day = datetime.now().month, datetime.now().day
        
        if current_month < month:
            ages.append(datetime.now().year - year -1)
        if current_month > month:
            ages.append(datetime.now().year - year)
        if current_month == month:
            if current_day < day:
                ages.append(datetime.now().year - year -1)
            if current_day >= day:
                ages.append(datetime.now().year - year)
        
    result = median(ages)
    return result


