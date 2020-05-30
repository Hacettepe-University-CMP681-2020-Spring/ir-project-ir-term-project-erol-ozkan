import json
import os
import threading
from urllib.parse import urlparse, ParseResult

import newspaper
import validators
from bson import json_util


class Crawler:
    articles_dir = 'news_resources/'

    def format_url(self, url):
        parsed_url = urlparse(url, 'http')
        site_location = parsed_url.netloc or parsed_url.path
        path = parsed_url.path if parsed_url.netloc else ''
        site_location = site_location.replace('www.', '')
        parsed_url = ParseResult('http', site_location, path, *parsed_url[3:])
        if not validators.url(parsed_url.geturl()):
            raise Exception("Error!")
        return parsed_url.geturl(), site_location

    def create_directory_if_doesnt_exist(self, articles_dir):
        if not os.path.exists(articles_dir):
            os.makedirs(articles_dir)

    def set_config(self, article):
        article.config.MIN_WORD_COUNT = 100  # num of word tokens in text
        article.config.MIN_SENT_COUNT = 3  # num of sentence tokens
        article.config.MAX_TITLE = 200  # num of chars
        article.config.MAX_TEXT = 1000000  # num of chars
        article.config.MAX_KEYWORDS = 70  # num of strings in list
        article.config.MAX_AUTHORS = 20  # num strings in list
        article.config.MAX_SUMMARY = 50000  # num of chars
        article.config.MAX_SUMMARY_SENT = 50  # num of sentences

    def write_to_file(self, directory, index, news_data):
        with open(directory + "/" + str(index) + ".json", 'w') as file:
            json.dump(news_data, file, default=json_util.default, indent=4)

    def get_article_as_json(self, article):
        data_to_save = {
            'article_id': article.link_hash,
            'title': article.title,
            'authors': article.authors,
            'canonical_link': article.canonical_link,
            'url': article.url,
            'top_img': article.top_img,
            'meta_img': article.meta_img,
            'movies': article.movies,
            'text': article.text,
            'keywords': article.keywords,
            'meta_keywords': article.meta_keywords,
            'publish_date': article.publish_date,
            'summary': article.summary,
            'article_html': article.article_html,
            'meta_description': article.meta_description,
            'meta_lang': article.meta_lang,
        }
        return data_to_save

    def download_articles(self, current_newspaper):
        current_newspaper, site_location = self.format_url(current_newspaper)
        current_directory = self.articles_dir + urlparse(current_newspaper).hostname.replace('.', '_')
        all_articles = newspaper.build(current_newspaper, memoize_articles=False)
        all_articles.print_summary()
        self.create_directory_if_doesnt_exist(current_directory)
        print(current_newspaper, current_directory)

        index = 0
        for article in all_articles.articles:
            if site_location in article.url:
                print('article : ' + article.url)
                self.set_config(article)
                article.download()
                if article.is_downloaded:
                    article.parse()
                    if article.is_valid_body():
                        article.nlp()
                        index += 1
                        news_data = self.get_article_as_json(article=article)
                        self.write_to_file(current_directory, index, news_data)
                    else:
                        print('Not a valid article: article : ' + article.url)
                else:
                    print('Could not download: article : ' + article.url)
            else:
                print('Didnt not download: article, not in path: ' + article.url)


newspaper_addresses = []
newspaper_addresses.append("https://www.haberturk.com/")
newspaper_addresses.append("https://www.cnnturk.com/")
newspaper_addresses.append("https://www.hurriyet.com.tr/")
newspaper_addresses.append("https://www.milliyet.com.tr/")
newspaper_addresses.append('https://www.ntv.com.tr/')
newspaper_addresses.append('https://tr.sputniknews.com/')

crawler = Crawler()
for newspaper_address in newspaper_addresses:
    t = threading.Thread(target=crawler.download_articles, args=(newspaper_address,))
    t.start()
