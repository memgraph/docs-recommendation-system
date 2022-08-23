import logging
import os
import time
from json import dumps

import nltk
from flask import Flask, Response, make_response, render_template, request
from flask_cors import CORS
from gqlalchemy import Call
from gqlalchemy.query_builders.declarative_base import Order

from controller import Controller
from database import memgraph
from scraper import get_links_and_documents

log = logging.getLogger(__name__)
args = None
app = Flask(__name__)
CORS(app)
controller = Controller()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/recommendations", methods=["POST"])
def recommend_docs():
    url = request.form["url"]
    text = request.form["text"]

    documents, all_urls, status = get_links_and_documents(url)

    if status == 404:
        return make_response("", status)

    # recommend docs based on text input
    if text:
        documents.insert(0, text)
        all_urls.insert(0, url + "/new_document")

    first_url = all_urls[0] 
    ind = first_url.rfind('/')
    url_name = first_url[ind+1:]
    if url_name == "":
        first_url = first_url[:ind]
        ind = first_url.rfind('/')
        url_name = first_url[ind + 1:]

    # tf-idf
    res = controller.tf_idf(documents, all_urls)
    if not res:
        return make_response("", -1)

    # node2vec
    controller.node2vec(documents, all_urls, url_name)
    #TODO: add exceptions?
    
    # link prediction
    controller.link_prediction(url_name)
    #TODO: add exceptions? 
                    
    #TODO: if there are no top recommendations, redirect to certain docs/wiki page?
    recs = {"tf-idf": controller.tf_idf_recs, "similarities": controller.similarities,
            "top_keywords": controller.top_keywords, "node2vec": controller.node2vec_recs, 
            "link_prediction": controller.link_prediction_recs}

    return make_response(dumps(recs), 200)

# TODO: pagerank in progress...
@app.route("/page-rank")
def get_page_rank():
    """Call the Page rank procedure and return top 30 in descending order."""
    try:
        results = list(
            Call("pagerank.get")
            .yield_()
            .with_(["node", "rank"])
            .return_([("node.name", "node_name"), "rank"])
            .order_by(properties=("rank", Order.DESC))
            .limit(30)
            .execute()
        )
        page_rank_dict = dict()
        page_rank_list = list()
        for result in results:
            user_name = result["node_name"]
            rank = float(result["rank"])
            page_rank_dict = {"name": user_name, "rank": rank}
            dict_copy = page_rank_dict.copy()
            page_rank_list.append(dict_copy)
        response = {"page_rank": page_rank_list}
        return Response(
            response=dumps(response), status=200, mimetype="application/json"
        )
    except Exception as e:
        log.info("Fetching users' ranks using pagerank went wrong.")
        log.info(e)
        return ("", 500)

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info(f"Time for {func.__name__} is {duration}")
        return result

    return wrapper

def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

def connect_to_memgraph():
    connection_established = False
    while not connection_established:
        if memgraph._get_cached_connection().is_active():
            connection_established = True

def download_nltk_packages():
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('punkt')

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        #init_log()
        connect_to_memgraph()
        download_nltk_packages()
    app.run(debug=True, host="0.0.0.0", port=5000)
