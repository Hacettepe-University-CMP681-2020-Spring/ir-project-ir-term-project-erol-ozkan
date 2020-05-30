import logging

from flask import Flask, request, render_template

from run_04_search_query import ModelQuery

ns = Flask(__name__)
modelQuery = ModelQuery(modelfile="model_files/output.data")

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
