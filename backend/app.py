import logging
import os
import threading
from json import dumps

from flask import Flask, make_response, render_template, request
from flask_cors import CORS
from gqlalchemy import Call, Match, Node
from gqlalchemy.query_builders.declarative_base import Order

from controller import Controller
from database import memgraph, names
from utils.scraper import Scraper

log = logging.getLogger(__name__)
args = None
app = Flask(__name__)
CORS(app)
controller = Controller()
scraper = Scraper()

@app.route("/")
def home():
    """Home endpoint."""
    return render_template("home.html")

@app.route("/recommendations", methods=["POST"])
def recommend_docs():
    """Returns recommendations based on tfidf, node2vec and link prediction algorithms."""
    url = request.form["url"]
    text = request.form["text"]

    try:
        documents, all_urls, status = scraper.get_links_and_documents(url)

        if status == 404:
            return make_response("", status)

        # recommend docs based on text input
        if text:
            documents.insert(0, text)
            all_urls.insert(0, url + "/new_document")

        # get the tail of the URL, i.e. its 'name' 
        first_url = all_urls[0] 
        ind = first_url.rfind('/')
        url_name = first_url[ind+1:]
        if url_name == "":
            first_url = first_url[:ind]
            ind = first_url.rfind('/')
            url_name = first_url[ind + 1:]
    
        recs_exist = False
        
        # call tf-idf algorithm
        x = threading.Thread(target=controller.tf_idf, args=(documents, all_urls,))
        x.start()
        
        # call node2vec algorithm
        y = threading.Thread(target=controller.node2vec, args=(documents, all_urls, url_name,))
        y.start()
        
        # call link prediction algorithm
        z = threading.Thread(target=controller.link_prediction, args=(url_name,))
        z.start()
        
        x.join()
        recs = controller.tf_idf_recs
        if recs: recs_exist = True
            
        y.join()
        recs = controller.node2vec_recs
        if recs: recs_exist = True
            
        z.join()
        recs = controller.link_prediction_recs
        if recs: recs_exist = True
        
        # alert if there are no recommendations    
        if not recs_exist:
            return make_response("", -1)
        
        recs = {"tf-idf": controller.tf_idf_recs, "similarities": controller.similarities,
                "top_keywords": controller.top_keywords, "node2vec": controller.node2vec_recs, 
                "link_prediction": controller.link_prediction_recs, "names": names}

        return make_response(dumps(recs), 200)
        
    except Exception as e:
        log.info("Something went wrong.")
        log.info(e)
        return ("", 500)

@app.route("/pagerank")
def get_pagerank():
    """Call the Pagerank procedure and return top 30 in descending order."""
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
            node_name = result["node_name"]
            rank = float(result["rank"])
            page_rank_dict = {"name": node_name, "rank": rank}
            dict_copy = page_rank_dict.copy()
            page_rank_list.append(dict_copy)

        res = {"page_rank": page_rank_list}
        return make_response(res, 200)

    except Exception as e:
        log.info("Fetching users' ranks using pagerank went wrong.")
        log.info(e)
        return ("", 500)

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
        names_set = set()
        nodes_set = set()
        
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
                main_name = result[0][0]
                source_url = result[0][1]

                target_name = result[1][0] 
                target_url = result[1][1]
                
                if source_name not in names_set:
                    nodes_set.add((source_name, source_url, 0))
                    names_set.add(source_name)
                
                if target_name not in names_set:
                    nodes_set.add((target_name, target_url, 1))
                    names_set.add(target_name)
                    links_set.add((source_name, target_name))                   

        for name in names_set:
            for result in results_list:
                if result[0][0] == name and result[0][0] != main_name:
                    source_name = result[0][0] 
                    source_url = result[0][1]

                    target_name = result[1][0] 
                    target_url = result[1][1]
                
                    if target_name not in names_set:
                        nodes_set.add((target_name, target_url, 2))
                        links_set.add((source_name, target_name))


        nodes = [{"id": node_url, "name": node_name, "depth": depth} for node_url, node_name, depth in nodes_set]
        links = [{"source": n_name, "target": m_name} for (n_name, m_name) in links_set]
        res = {"nodes": nodes, "links": links, "base_url": url}

        return make_response(res, 200)
    
    except Exception as e:
        log.info("Fetching URL went wrong.")
        log.info(e)
        return ("", 500)

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
        init_log()
        connect_to_memgraph()
    app.run(debug=True, host="0.0.0.0", port=5000)
