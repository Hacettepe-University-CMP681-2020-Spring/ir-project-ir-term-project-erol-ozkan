import json
import os
from datetime import datetime

from bson import json_util

from run_05_search_query_bm25 import ModelQueryBM25
from utils import print_model_into_pickle_file, print_model_into_file


class EvaluatorBM25:
    def __init__(self):
        self.modelQuery = ModelQueryBM25(modelfile="model_files/output_bm25.data")
        self.results = {}

    def evaluate(self, path):
        for root, dirs, files in os.walk(path):
            self.results[root] = {}

            if root != 'news_resources/':
                print('files in ' + root + ': ' + ', '.join(files))

                for file in files:
                    if file.endswith('.json'):
                        fullpath = root + '/' + file
                        article = json.load(open(fullpath), object_hook=json_util.object_hook)  # load article.
                        results = self.modelQuery.search_for_query(article['title'])
                        self.results[root][article['article_id']] = {"results": results, "article": article}
        return self.results


start = datetime.now()
evaluator = EvaluatorBM25()
results = evaluator.evaluate("news_resources/")
print_model_into_pickle_file(results, "output/results_bm25.data")
end = datetime.now()
print_model_into_file({"time_start": start, "time_end": end, "diff": str(end - start)}, "output/timings/evaluation_bm25.json")
