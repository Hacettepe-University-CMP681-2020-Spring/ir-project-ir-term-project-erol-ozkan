import logging

from flask import Flask, request, render_template

from run_05_search_query_bm25 import ModelQueryBM25

ns = Flask(__name__)
modelQuery = ModelQueryBM25(modelfile="model_files/output_bm25.data")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@ns.route('/')
def index():
    return render_template('index.html')


@ns.route('/search')
def search():
    query = request.args.get('query')
    results = modelQuery.search_for_query(query=query)
    if not results:
        return not_found()
    else:
        return render_template('results.html', search_results=results, query=query)


def not_found():
    return render_template('not_found.html')


if __name__ == '__main__':
    ns.run(debug=True, host='0.0.0.0', port=8080)
