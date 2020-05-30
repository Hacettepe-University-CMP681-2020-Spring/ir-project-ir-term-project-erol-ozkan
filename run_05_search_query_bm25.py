import operator
import pickle

import nltk
from nltk.stem.snowball import SnowballStemmer
from snowballstemmer import TurkishStemmer

from utils_BM25 import get_query_result


class ModelQueryBM25:
    indexed_articles = {}

    def __init__(self, modelfile):
        self.stammer = SnowballStemmer('english')  # turkish is not supported.
        # self.stemmer = TurkishStemmer()
        self.model_data = pickle.load(open(modelfile, 'rb'))
        self.data_dict = {x['article_id']: x for x in self.model_data['article_list']}

    def tokenize_query(self, query):
        tokens = nltk.word_tokenize(query)
        tokens = [self.stammer.stem(x) for x in tokens]
        return tokens

    def search_for_query(self, query):
        tokens = self.tokenize_query(query)
        result = get_query_result(self.model_data['inverted_index'], self.model_data['document_lengths'], tokens)
        sorted_list = sorted(result.items(), key=operator.itemgetter(1))
        sorted_list.reverse()
        return_list = []

        for elem in sorted_list:
            return_list.append([elem[1], self.data_dict[elem[0]]])
        return return_list

# modelQuery = ModelQueryBM25(modelfile="model_files/output_bm25.data")
# print(modelQuery.search_for_query("gıda"))
