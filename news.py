import threading

import requests

from bs4 import BeautifulSoup


class News:
    title: str
    time: str

    def __init__(self, raw_news) -> None:
        self.title = raw_news.find("span", {'class': 'item__title'}).text.strip()
        self.time = raw_news.find("span", {'class': 'item__category'}).text.strip()

    def __eq__(self, o) -> bool:
        return self.title == o.title

    def __str__(self) -> str:
        return f"{self.title}\n{self.time}"


class NewsList:
    news: list

    def __init__(self) -> None:
        threading.Thread(target=self.load).start()

    def text(self) -> str:
        return "\n".join(list(map(str, self.news)))

    def load(self):
        html = requests.get('https://quote.rbc.ru/short_news/').text
        soup = BeautifulSoup(html)

        find = soup.find_all('div', {'class': 'item'})

        self.news = list(map(News, find))
