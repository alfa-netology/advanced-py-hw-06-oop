from datetime import datetime as dt
from datetime import timedelta
import re

import mechanicalsoup
from tqdm import tqdm

class HabrParser:
    def __init__(self, url, keywords):
        self.browser = mechanicalsoup.StatefulBrowser()
        self.url = url
        self.search_pattern = '|'.join([f"\\b{word}\\b" for word in keywords])        
        self.articles = self._get_articles()

    def _get_articles(self):
        self.browser.open(self.url)
        return self.browser.get_current_page().find_all('article', class_='post_preview')

    @staticmethod
    def _date_beautify(date):
        today = str(dt.date(dt.now()))
        yesterday = str(dt.date(dt.now()) - timedelta(days=1))
        return date.replace('сегодня', today).replace('вчера', yesterday)

    def _get_article_full_text(self, link):
        self.browser.open(link)
        article_text = self.browser.get_current_page().find('div', class_='post__body')
        return article_text.text if article_text else ''

    def find_articles_by_keywords(self):
        find_in_preview, find_in_full_text = (), ()
        for article in tqdm(self.articles, desc='collect data:'):
            date = self._date_beautify(article.find('span', class_='post__time').text)
            link = article.find('a', class_='post__title_link').get('href')
            title = article.find('a', class_='post__title_link').text
            preview = article.find('div', class_='post__text').text
            full_text = self._get_article_full_text(link)

            if re.search(self.search_pattern, preview, flags=re.I):
                found_words = re.findall(self.search_pattern, preview, flags=re.I)
                find_in_preview += (f"<{date}> - <{title}> - <{link}> - найденые слова: {found_words}",)

            if re.search(self.search_pattern, full_text, flags=re.I):
                found_words = re.findall(self.search_pattern, full_text, flags=re.I)
                find_in_full_text += (f"<{date}> - <{title}> - <{link}> - найденые слова: {found_words}",)

        return find_in_preview, find_in_full_text
