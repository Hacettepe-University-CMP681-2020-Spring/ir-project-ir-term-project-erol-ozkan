import pickle

import nltk
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from snowballstemmer import TurkishStemmer

from utils import remove_duplicated_articles


class ModelQuery:
    indexed_articles = {}

    def __init__(self, modelfile):
        self.stammer = SnowballStemmer('english')  # turkish is not supported.
        # self.stemmer = TurkishStemmer()
        self.indexed_articles = pickle.load(open(modelfile, 'rb'))

    def tokenize_query(self, query):
        tokens = nltk.word_tokenize(query)
        tokens = [self.stammer.stem(x) for x in tokens]
        return tokens

    def search_for_query(self, query):
        tokens = self.tokenize_query(query)

        scipy_sparse_matrix = self.indexed_articles['matrix']
        matrix = scipy_sparse_matrix.toarray()
        print("Matix shape: ", matrix.shape)

        articles = self.indexed_articles['articles']

        terms = self.indexed_articles['terms']
        number_of_terms = len(terms)

        bag = [0] * number_of_terms
        for term in tokens:
            if term in terms:
                bag[terms.index(term)] += 1
        bag = np.array(bag).astype(float)
        results = []
        article_count, words_count = matrix.shape
        for i in range(article_count):
            correlation_result = np.correlate(bag, matrix[i, :])
            results.append((correlation_result[0], articles[i]))

        results = sorted(results, key=lambda x: x[0], reverse=True)
        filtered_results = [(score, article) for (score, article) in results if score > 0]
        return remove_duplicated_articles(filtered_results)

#
# modelQuery = ModelQuery(modelfile="model_files/output.data")
# print(modelQuery.search_for_query("gıda"))
