import requests
import string
import os
import re
from bs4 import BeautifulSoup


class ArticleScraper:
    def __init__(self, link, num, type_):
        self.link = link
        self.num = num
        self.type_ = type_
        self.article_urls = []

    @staticmethod
    def check_page(response) -> None:
        if response.status_code == 200:
            print('Page OK.')
        else:
            print('The URL returned ' + str(response.status_code) + '!')
            exit()

    def grab_links(self, page_url) -> None:
        r = requests.get(page_url)
        self.check_page(r)
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            article_type = article.find('span', {'class': 'c-meta__type'})
            if article_type.text == self.type_:
                article_link = article.find('a')
                self.article_urls.append('https://www.nature.com' + article_link.get('href'))

    @staticmethod
    def process_title(head) -> str:
        filename = head.translate(head.maketrans(' ', '_', string.punctuation))
        filename += '.txt'
        return filename

    @staticmethod
    def create_dir(digit) -> None:
        dir_name = f'Page_{str(digit)}'
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
            print(f'Folder /{dir_name} created')
        else:
            print(f'Folder /{dir_name} already exists')
        os.chdir(dir_name)
        print(f'Inside folder /{dir_name}')

    def save_article(self, article_url) -> None:
        r1 = requests.get(article_url)
        soup1 = BeautifulSoup(r1.content, 'html.parser')
        article_body = soup1.find(class_=re.compile(".*article-body.*"))
        headline = self.process_title(soup1.find('h1', {'class': 'c-article-magazine-title'}).text)
        print('File ' + headline + ' created successfully')
        my_file = open(headline, 'w', encoding='utf-8')
        my_file.write(article_body.text.strip())
        my_file.close()

    def main(self):
        for page in range(pages):
            self.grab_links(self.link + str(page+1))
            self.create_dir(page+1)
            for link in self.article_urls:
                self.save_article(link)
            self.article_urls = []
            os.chdir('..')


if __name__ == "__main__":
    url = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page=?page='
    pages = int(input('Number of pages: '))
    type_of_article = input('Type of articles: ')
    go_scrape_that = ArticleScraper(url, pages, type_of_article)
    go_scrape_that.main()
    print('Saved all articles.')

# '.*article.*body.*'
# use re.compile() on it to get ALL the possible body classes