import json
import os
from datetime import datetime

import numpy as np
import scipy
from bson import json_util
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from snowballstemmer import TurkishStemmer

from utils import get_filtered_article_text, print_model_into_pickle_file, print_model_into_file


class Indexer:
    def __init__(self):
        self.stop = stopwords.words('turkish')
        self.stemmer = SnowballStemmer('english')  # turkish is not supported.
        # self.stemmer = TurkishStemmer()

        self.article_list = []  # List of articles
        self.terms_by_article = []  # Terms by article
        self.terms = []  # All terms
        self.bag_of_words = []  # Bag of words

    def fill_terms(self, path):
        for root, dirs, files in os.walk(path):
            print('files: ' + ', '.join(files))
            for file in files:
                if file.endswith('.json'):
                    fullpath = root + '/' + file
                    print('Processing file: ' + fullpath)
                    article = json.load(open(fullpath), object_hook=json_util.object_hook)
                    filtered_terms = get_filtered_article_text(self.stemmer, self.stop, article)
                    self.article_list.append(article)
                    self.terms_by_article.append(filtered_terms)
                    self.terms += filtered_terms
            for directory in dirs:
                self.fill_terms(directory)
        self.terms = list(set(self.terms))  # eliminate duplicates

    def fill_bags_of_words(self):
        number_of_terms = len(self.terms)
        number_of_articles = len(self.terms_by_article)
        for i in range(number_of_articles):
            bag = [0] * number_of_terms  # create empty array
            for term in self.terms_by_article[i]:  # foreach article
                bag[self.terms.index(term)] += 1
            self.bag_of_words.append(bag)
        self.bag_of_words = np.array(indexer.bag_of_words).astype(float)

    def append_inverse_document_frequency(self):
        docs, words = self.bag_of_words.shape
        for i in range(words):
            frequency_per_doc = self.bag_of_words[:, i]
            nw = 0
            for j in range(len(frequency_per_doc)):
                if frequency_per_doc[j] != 0:
                    nw += 1
            idf = np.log(docs / nw)
            self.bag_of_words[:, i] *= idf


start = datetime.now()
indexer = Indexer()
indexer.fill_terms("news_resources/")
indexer.fill_bags_of_words()
indexer.append_inverse_document_frequency()
print_model_into_pickle_file({'matrix': scipy.sparse.csr_matrix(indexer.bag_of_words), 'articles': indexer.article_list, 'terms': indexer.terms}, "model_files/output.data")
end = datetime.now()
print_model_into_file({"time_start": start, "time_end": end, "diff": str(end - start)}, "output/timings/index_creation.json")
