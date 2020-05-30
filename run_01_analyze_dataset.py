import json
import os

from bson import json_util
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from snowballstemmer import TurkishStemmer

from utils import get_filtered_query_terms, get_filtered_article_text, print_model_into_file


class DatasetAnalyzer:
    def __init__(self):
        self.stop = stopwords.words('turkish')
        self.stemmer = SnowballStemmer('english')  # turkish is not supported.
        # self.stemmer = TurkishStemmer()

        self.json_files = {}
        self.statistics = {}

        self.total_statistics = {}
        self.total_statistics['total_number_of_documents'] = 0
        self.total_statistics['total_avarage_query_length'] = 0
        self.total_statistics['total_avarage_text_length'] = 0

    def analyze(self, path):
        for root, dirs, files in os.walk(path):
            if root != 'news_resources/':
                print('files in ' + root + ': ' + ', '.join(files))

                self.json_files[root] = []
                self.statistics[root] = {}
                query_lengths = 0
                text_lengths = 0

                for file in files:
                    if file.endswith('.json'):
                        fullpath = root + '/' + file

                        article = json.load(open(fullpath), object_hook=json_util.object_hook)  # load article.
                        self.json_files[root].append(article)  # append it to json files.

                        filtered_query_terms = get_filtered_query_terms(self.stemmer, self.stop, article)  # get filtered query terms.
                        text_filtered_terms = get_filtered_article_text(self.stemmer, self.stop, article)  # get filtered text terms

                        query_lengths += len(filtered_query_terms)  # sum query lengths
                        text_lengths += len(text_filtered_terms)  # sum text lengths

                self.statistics[root]['number_of_documents'] = len(self.json_files[root])
                self.statistics[root]['avarage_query_length'] = query_lengths / len(self.json_files[root])
                self.statistics[root]['avarage_text_length'] = text_lengths / len(self.json_files[root])

                self.total_statistics['total_number_of_documents'] += len(self.json_files[root])
                self.total_statistics['total_avarage_query_length'] += self.statistics[root]['avarage_query_length']
                self.total_statistics['total_avarage_text_length'] += self.statistics[root]['avarage_text_length']

        self.total_statistics['total_avarage_query_length'] /= len(self.json_files)
        self.total_statistics['total_avarage_text_length'] /= len(self.json_files)

        return self.json_files, self.statistics, self.total_statistics


INPUT_DIRECTORY = "news_resources/"
OUTPUT_FILEPATH = "output/"

datasetAnalyzer = DatasetAnalyzer()
json_files, statistics, total_statistics = datasetAnalyzer.analyze(INPUT_DIRECTORY)
print_model_into_file(statistics, OUTPUT_FILEPATH + "/dataset_statistics/statistics.json")
print_model_into_file(total_statistics, OUTPUT_FILEPATH + "/dataset_statistics/total_statistics.json")
