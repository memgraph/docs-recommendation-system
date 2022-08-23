import logging
import os
import time
from json import dumps

from flask import Flask, Response, make_response, render_template, request
from flask_cors import CORS
from gqlalchemy import Call, Node
from gqlalchemy.query_builders.declarative_base import Order

from database import memgraph, populate_db
from extractor import rake
from link_prediction import link_prediction
from node2vec import get_embeddings_as_properties, predict
from scraper import get_links_and_documents
from tf_idf import get_recommendations

log = logging.getLogger(__name__)
args = None
app = Flask(__name__)
CORS(app)
NUM_OF_RECS = 0

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
    if not text == "":
        documents.insert(0, text)
        all_urls.insert(0, url + "/new_document")

    first_url = all_urls[0] 
    ind = first_url.rfind('/')
    url_name = first_url[ind+1:]
    if url_name == "":
        first_url = first_url[:ind]
        ind = first_url.rfind('/')
        url_name = first_url[ind + 1:]

    tf_idf_recommendations, node2vec_recommendations, link_prediction_recs = [], [], []

    # tf-idf
    corpus_length = len(documents)
    if corpus_length > 1:
        recommendations, similarities, top_keywords = get_recommendations(documents)
        tf_idf_recommendations = [all_urls[i] for i in recommendations]
    else:
        return make_response("", -1)

    # node2vec
    new_docs = rake(documents)
    populate_db(all_urls, new_docs)
    nodes, node_embeddings = get_embeddings_as_properties()
    predicted_edges = predict(node_embeddings)

    NUM_OF_RECS = 0
    top_rec_name = []
    for key in predicted_edges:
        if NUM_OF_RECS == 3:
            break
        if key[0] == url_name:
            top_rec_name.append(key[1])
            NUM_OF_RECS += 1
        elif key[1] == url_name:
            top_rec_name.append(key[0])
            NUM_OF_RECS += 1

    for i in top_rec_name:
        for result in nodes:
            if(result["n_name"] == i):
                    node2vec_recommendations.append(result["n_url"])
                    break
    
    # link prediction
    nodes, precise_edges = link_prediction()

    NUM_OF_RECS = 0
    top_link_name = []

    for key in precise_edges:
        if NUM_OF_RECS == 3:
            break
        if key[0] == url_name:
            top_link_name.append(key[1])
            NUM_OF_RECS += 1
        elif key[1] == url_name:
            top_link_name.append(key[0])
            NUM_OF_RECS += 1

    for i in top_link_name:   
        for result in nodes:
            if(result["n_name"] == i):
                link_prediction_recs.append(result["n_url"])
                break   
                    
    # TODO: if there are no top recommendations, redirect to certain docs/wiki page?
    recs = {"tf-idf": tf_idf_recommendations, "similarities": similarities,
            "top_keywords": top_keywords, "node2vec": node2vec_recommendations , "link_prediction":link_prediction_recs}

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

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        #init_log()
        connect_to_memgraph()
    app.run(debug=True, host="0.0.0.0", port=5000)
