import requests
from bs4 import BeautifulSoup as BS
import time
import random

base_url = "https://news.ycombinator.com/newest"


def extract_news(soup):
    first = soup.find_all('tr', attrs={'class': 'athing'})
    second = soup.find_all('td', attrs={'class': 'subtext'})

    part1 = []
    part2 = []
    articles = []
    for f in first:
        title = f.find('a', attrs={'class': 'storylink'}).text
        url = f.find('a', attrs={'class': 'storylink'})['href']
        part1.append({'title': title, 'url': url})
    for s in second:
        author = s.find('a', attrs={'class': 'hnuser'}).text
        comments = s.text.split()
        if comments[14] == 'discuss':
            comments[14] = 0
        else:
            comments[14] = int(comments[14])
        points = s.find('span', attrs={'class': 'score'}).text.split()
        part2.append({'author': author, 'comments': comments[14], 'points': points[0]})

    for i in range(len(part2)):
        articles.append({'title': part1[i]['title'], 'url': part1[i]['url'], 'author': part2[i]['author'],
                         'comments': part2[i]['comments'], 'points': part2[i]['points']})

    return articles


def extract_next_page(soup):
    pages = soup.find_all('table', attrs={'class': 'itemlist'})
    for page in pages:
        next = page.find('a', attrs={'class': 'morelink'})['href']

    return next


def get_news(url, n_pages):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)

        if response.status_code == 200:
            soup = BS(response.content, "html.parser")
            news_list = extract_news(soup)
            next_page = extract_next_page(soup)
            url = "https://news.ycombinator.com/" + next_page
            news.extend(news_list)
            n_pages -= 1

    return news
