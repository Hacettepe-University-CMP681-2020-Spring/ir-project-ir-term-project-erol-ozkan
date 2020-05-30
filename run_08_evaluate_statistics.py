import pickle

from utils import load_pickle_file, print_model_into_file
from utils_evaluation import mean_reciprocal_rank, r_precision, precision_at_k, mean_average_precision


class FinalEvaluator:
    def __init__(self, path):
        self.all_articles = pickle.load(open("model_files/output.data", 'rb'))['articles']
        self.all_results = load_pickle_file(path)
        self.inner_results = {}
        self.directory_results = {}

    def final_evaluate(self):
        all_results_mrr = []

        for resources in self.all_results:
            self.inner_results[resources] = {}

            if resources == "news_resources/":
                continue

            directory_results_mrr = []
            resource_predictions = self.all_results[resources]

            for article_id in resource_predictions:
                resource_data = resource_predictions[article_id]
                inner_results = []

                for index, result in enumerate(resource_data['results']):
                    inner_results.append(int(result[1]['article_id'] == resource_data['article']['article_id']))

                self.inner_results[resources][article_id] = {}
                self.inner_results[resources][article_id]['data'] = ''.join(str(inner_results))
                self.inner_results[resources][article_id]['mean_reciprocal_rank'] = mean_reciprocal_rank([inner_results])
                self.inner_results[resources][article_id]['mean_average_precision'] = mean_average_precision([inner_results])
                self.inner_results[resources][article_id]['r_precision'] = r_precision(inner_results)
                self.inner_results[resources][article_id]['r_precision@1'] = precision_at_k(inner_results, 1)
                self.inner_results[resources][article_id]['r_precision@3'] = precision_at_k(inner_results, 4)
                self.inner_results[resources][article_id]['r_precision@5'] = precision_at_k(inner_results, 5)
                self.inner_results[resources][article_id]['r_precision@10'] = precision_at_k(inner_results, 10)

                directory_results_mrr.append(inner_results)

            self.directory_results[resources] = {}
            self.directory_results[resources]['mean_reciprocal_rank'] = mean_reciprocal_rank(directory_results_mrr)
            self.directory_results[resources]['mean_average_precision'] = mean_average_precision(directory_results_mrr)
            all_results_mrr += directory_results_mrr

        return self.inner_results, self.directory_results, {"mean_reciprocal_rank": mean_reciprocal_rank(all_results_mrr), "mean_average_precision": mean_average_precision(all_results_mrr)}


finalEvaluator = FinalEvaluator("output/results.data")
inner_results, directory_results, outer_results = finalEvaluator.final_evaluate()
print_model_into_file(inner_results, "output/basic_model/0_inner_results.json")
print_model_into_file(directory_results, "output/basic_model/1_directory_results.json")
print_model_into_file(outer_results, "output/basic_model/2_outer_results.json")

finalEvaluator = FinalEvaluator("output/results_bm25.data")
inner_results, directory_results, outer_results = finalEvaluator.final_evaluate()
print_model_into_file(inner_results, "output/bm25_model/0_inner_results.json")
print_model_into_file(directory_results, "output/bm25_model/1_directory_results.json")
print_model_into_file(outer_results, "output/bm25_model/2_outer_results.json")
