import requests
from bs4 import BeautifulSoup as BS
import bottle
from bottle import (
    route, run, template, request, redirect
)

from scraputils import base_url
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@bottle.route('/')
@route("/news")
def news_list():
    s = session()

    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    s = session()
    id = request.query['id']
    label = request.query['label']
    news = s.query(News).get(id)

    news.label = label
    s.commit()
    redirect('/news')


@route("/update")
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    s = session()
    NEWS = get_news(base_url, 1)
    for i in range(len(NEWS)):
        title = NEWS[i]['title']
        author = NEWS[i]['author']
        news = s.query(News).filter(News.title == title, News.author == author).all()
        if news == []:
            n = News(title=title, author=author, url=NEWS[i]['url'], comments=NEWS[i]['comments'],
                     points=NEWS[i]['points'])
            s.add(n)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
