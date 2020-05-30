import json
import pickle

import nltk
from bson import json_util


def get_filtered_query_terms(stemmer, stopwords, article):
    filtered_terms = nltk.word_tokenize(article['title'])
    filtered_terms = [stemmer.stem(x) for x in filtered_terms if len(x) > 2 and x not in stopwords]
    # filtered_terms = [stemmer.stemWord(x) for x in filtered_terms if len(x) > 2 and x not in stopwords]
    return filtered_terms


def get_filtered_article_text(stemmer, stopwords, article):
    text_filtered_terms = nltk.word_tokenize(article['text'])
    text_filtered_terms = [stemmer.stem(x) for x in text_filtered_terms if len(x) > 2 and x not in stopwords]
    # text_filtered_terms = [stemmer.stemWord(x) for x in text_filtered_terms if len(x) > 2 and x not in stopwords]
    return text_filtered_terms


def remove_duplicated_articles(filtered_results):
    results_without_duplicates = []
    article_urls = []
    for (score, article) in filtered_results:
        article_url = article['canonical_link']
        if article_url not in article_urls:
            results_without_duplicates.append((score, article))
            article_urls.append(article_url)
    return results_without_duplicates


def print_model_into_file(data, output_path):
    with open(output_path, 'w') as file:
        json.dump(data, file, default=json_util.default, indent=4)


def print_model_into_pickle_file(data, output_path):
    with open(output_path, "wb") as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


def load_pickle_file(input_path):
    data = pickle.load(open(input_path, "rb"))
    return data
