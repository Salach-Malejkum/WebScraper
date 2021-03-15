import string
import os

import requests
from bs4 import BeautifulSoup

number_of_pages = int(input())
type_of_article = input()

for page in range(number_of_pages):
    page_content = requests.get("https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page="\
                                + str(page + 1), headers={'Accept-Language': 'en-US,en;q=0.5'}).content
    soup = BeautifulSoup(page_content, 'html.parser')

    os.mkdir("Page_" + str(page + 1))
    os.chdir("Page_" + str(page + 1))
    for article in soup.find_all("article"):
        find_news = article.find('span', attrs={"data-test": "article.type"})
        if find_news.find('span').get_text() == type_of_article:
            article_data = article.find('a', attrs={"data-track-action": "view article"})
            article_title = article_data.get_text()
            for i in string.punctuation:
                article_title = article_title.replace(i, "")
            article_title = article_title.replace(" ", "_")
            file = open(article_title + ".txt", "wb")
            article_page = requests.get("https://www.nature.com" + article_data.get('href')).content
            article_soup = BeautifulSoup(article_page, 'html.parser')
            if article_soup.find("div", attrs={"class": "article-item__body"}) is not None:
                file.write(article_soup.find("div", attrs={"class": "article-item__body"}).text.encode('utf-8'))
            elif article_soup.find("div", attrs={"class": "article__body cleared"}) is not None:
                file.write(article_soup.find("div", attrs={"class": "article__body cleared"}).text.encode('utf-8'))
            file.close()
    os.chdir(os.path.dirname(os.getcwd()))
