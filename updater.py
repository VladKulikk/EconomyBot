import threading
import time
from typing import Callable

from news import NewsList


class Updater:
    news: NewsList
    onUpdate: Callable[[list], None]

    def __init__(self, func) -> None:
        self.news = NewsList()
        self.onUpdate = func

    def update(self):
        old_news = self.news.news.copy()
        self.news.load()

        updated_news = []
        for news in self.news.news:
            if len(old_news) > 0 and news == old_news[0]:
                break

            updated_news.append(news)

        self.onUpdate(updated_news)

    def thread(self):
        while True:
            self.update()
            time.sleep(15 * 60)

    def start(self):
        threading.Thread(target=self.thread).start()
