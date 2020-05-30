import json
import os
from datetime import datetime

from bson import json_util
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from snowballstemmer import TurkishStemmer

from utils import print_model_into_pickle_file, get_filtered_article_text, print_model_into_file
from utils_BM25 import InvertedIndex, DocumentLengthTable


class Evaluator:
    def __init__(self):
        self.stop = stopwords.words('turkish')
        self.stemmer = SnowballStemmer('english')  # turkish is not supported.
        # self.stemmer = TurkishStemmer()

        self.article_list = []  # List of articles
        self.inverted_index = InvertedIndex()
        self.document_lengths = DocumentLengthTable()

    def build(self, path):
        for root, dirs, files in os.walk(path):
            if root != 'news_resources/':
                print('files in ' + root + ': ' + ', '.join(files))
                for file in files:
                    if file.endswith('.json'):
                        fullpath = root + '/' + file

                        article = json.load(open(fullpath), object_hook=json_util.object_hook)  # load article.
                        text_filtered_terms = get_filtered_article_text(self.stemmer, self.stop, article)  # get filtered text terms
                        self.article_list.append(article)

                        for word in text_filtered_terms:
                            self.inverted_index.add(str(word), str(article['article_id']))
                        self.document_lengths.add(str(article['article_id']), len(text_filtered_terms))

        return self.inverted_index, self.article_list, self.document_lengths


start = datetime.now()
evaluator = Evaluator()
inverted_index, article_list, document_lengths = evaluator.build("news_resources/")
print_model_into_pickle_file({'inverted_index': inverted_index, 'article_list': article_list, 'document_lengths': document_lengths}, "model_files/output_bm25.data")
end = datetime.now()
print_model_into_file({"time_start": start, "time_end": end, "diff": str(end - start)}, "output/timings/index_creation_bm25.json")
