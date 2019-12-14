from stop_words import get_stop_words
import pandas as pd
import pymorphy2
import requests
import textwrap
import gensim
import config
import emoji

from pandas.io.json import json_normalize
from string import Template
from gensim import corpora
from pprint import pprint
from tqdm import tqdm

extra_chars = ['-', ',', '.', '!', '?', '(', ')', '[', ']', '\n']

morph = pymorphy2.MorphAnalyzer()
stop_words = get_stop_words('ru')


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
    code = ("return API.wall.get({" +
        f"'owner_id': '{owner_id}'," +
        f"'domain': '{domain}'," +
        f"'offset': {offset}," +
        f"'count': {count}," +
        f"'filter': '{filter}'," +
        f"'extended': {extended}," +
        f"'fields': '{fields}'," +
        f"'v': {v}," +
    "});")

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": config.VK_CONFIG["access_token"],
                "v": "5.103"
            }
    )

    return response.json()['response']['items']


def delete_links(text):
    if "http" in text:
        ind = text.index("http")
        bg = ind

        while ind < len(text) and text[ind] != " ":
            ind += 1

        text = text[:bg] + text[ind:]

        delete_links(text)

    return text


def delete_emojis(text):
  return ''.join(c for c in text if not c in emoji.UNICODE_EMOJI)


def delete_stopwords(text):
    for char in extra_chars:
        text = text.replace(char, " ")

    text = text.split()

    return " ".join([word for word in text if not word in stop_words])


def preparation_text(text):
    text = delete_links(text)
    text = delete_emojis(text)
    text = delete_stopwords(text)

    return [morph.parse(word)[0].normal_form for word in text.split()]


def normilize_texts(domain):
    posts_list = get_wall(domain=domain)
    posts_texts = [post["text"].lower() for post in posts_list]

    for post_ind, post_text in enumerate(posts_texts):
        posts_texts[post_ind] =  preparation_text(post_text)

    return posts_texts
