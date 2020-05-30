import json
import os
from datetime import datetime

from bson import json_util

from run_04_search_query import ModelQuery
from utils import print_model_into_pickle_file, print_model_into_file


class Evaluator:
    def __init__(self):
        self.modelQuery = ModelQuery(modelfile="model_files/output.data")
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
evaluator = Evaluator()
results = evaluator.evaluate("news_resources/")
print_model_into_pickle_file(results, "output/results.data")
end = datetime.now()
print_model_into_file({"time_start": start, "time_end": end, "diff": str(end - start)}, "output/timings/evaluation.json")
