import datetime as dt
from statistics import median
from typing import Optional
import config
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
    friends_ages = []
    friend_info = get_friends(user_id, 'bdate')
    date_now = dt.datetime.now()
    date_now = dt.datetime.strftime(date_now, "%d.%m.%Y")
    date_now = dt.datetime.strptime(date_now, "%d.%m.%Y")
    # преобразоваваем сегоднещнюю дату в нужный нам формат
    print(date_now)

    year_in_seconds = 3.154e7
    for i in friend_info['response']['items']:
        try:
            friends_birthday = i['bdate']

            friends_birthday = dt.datetime.strptime(friends_birthday, "%d.%m.%Y")
            print(friends_birthday)
            age = ((date_now - friends_birthday).total_seconds()) // year_in_seconds
            # поулчаем возраст друга при помоши деления дат в секундах
            friends_ages.append(age)
        except:
            pass
    print(median(friends_ages))
    return median(friends_ages)


age_predict(config.user_id)
