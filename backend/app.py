import logging
import os
import time
from json import dumps
from typing import Tuple
import nltk
from flask import Flask, Response, make_response, render_template, request
from flask_cors import CORS
from gqlalchemy import Call, Match, Node
from gqlalchemy.query_builders.declarative_base import Order

from controller import Controller
from database import memgraph, names
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
            "link_prediction": controller.link_prediction_recs, "names": names}

    return make_response(dumps(recs), 200)


# TODO: pagerank in progress...
@app.route("/pagerank")
def get_page_rank():
    """Call the Page rank procedure and return top 30 in descending order."""
    #try:
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
        node_name = result["node_name"]
        rank = float(result["rank"])
        page_rank_dict = {"name": node_name, "rank": rank}
        dict_copy = page_rank_dict.copy()
        page_rank_list.append(dict_copy)

    res = {"page_rank": page_rank_list}
    return make_response(res, 200)
    """except Exception as e:
        log.info("Fetching users' ranks using pagerank went wrong.")
        log.info(e)
        return ("", 500)"""

@app.route("/webpage/")
def get_webpage():
    """Get info about specific web page."""
    args = request.args
    url = args["url"]
    
    try:
        results = Match() \
            .node(labels="WebPage", variable="node_a") \
            .to(relationship_type="SIMILAR_TO", variable="edge") \
            .node(labels="WebPage", variable="node_b") \
            .return_() \
            .execute()

        results_list = []
        links_set = set()
        nodes_set = set()
        parents = []
        
        for result in results:
            node: Node = result["node_a"]
            name_a = node._properties["name"]
            url_a = node._properties["url"]
            
            node2: Node = result["node_b"]
            name_b = node2._properties["name"]
            url_b = node2._properties["url"]

            results_list.append([(name_a, url_a), (name_b, url_b)])
            
        for result in results_list:
            if result[0][1] == url:
                source_name = result[0][0] 
                source_url = result[0][1] 
                source_label = "WebPage"

                target_name = result[1][0] 
                target_url = result[1][1] 
                target_label = "WebPage"
                
                nodes_set.add((source_name, source_url, source_label))
                nodes_set.add((target_name, target_url, target_label))
                if (source_name, target_name) not in links_set and (target_name, source_name) not in links_set:
                    links_set.add((source_name, target_name))
                
                if target_name not in parents:
                    parents.append(target_name) 
        
        for parent in parents:
            for result in results_list:
                if result[0][0] == parent:
                    source_name = result[0][0] 
                    source_url = result[0][1] 
                    source_label = "WebPage"

                    target_name = result[1][0] 
                    target_url = result[1][1] 
                    target_label = "WebPage"
                    
                    nodes_set.add((source_name, source_url, source_label))
                    nodes_set.add((target_name, target_url, target_label))
                    if (source_name, target_name) not in links_set and (target_name, source_name) not in links_set and target_name not in parents:
                        links_set.add((source_name, target_name))
            
        nodes = [{"id": node_url, "name": node_name, "label": node_label, } for node_url, node_name, node_label in nodes_set]
        links = [{"source": n_name, "target": m_name} for (n_name, m_name) in links_set]
        res = {"nodes": nodes, "links": links, "base_url": url}

        return make_response(res, 200)
    
    except Exception as e:
        log.info("Fetching URL went wrong.")
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
