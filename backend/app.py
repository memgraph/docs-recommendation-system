from flask import Flask, render_template, request, redirect
from scraper import get_links
from tf_idf import get_recommendations
from extractor import rake
from database import populate_db, predict, memgraph, get_embeddings_as_properties
from os.path import abspath
from typing import Dict, List, Tuple
import os
import logging
import validators

#memgraph = gqlalchemy.Memgraph(host="memgraph-mage", port=7687)

log = logging.getLogger(__name__)
args = None
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def redirect_docs():
    url = request.form["input-url"]
    
    # check if input url is valid
    valid = validators.url(url)
    if not valid:
        print("Please input valid url!")
        # TODO: ponovni unos i napraviti alert
    
    ind = url.rfind('/')
    url_name = url[ind+1:]
    method = int(request.form["model-method"])
    documents, all_urls = get_links(url)
    
    if method == 1:
        if len(documents) > 1:
            recommendations = get_recommendations(documents)
            """for i in recommendations:
                print("i:", i)
                print("all_urls[i]:", all_urls[i])"""
        else:
            print("Only 1 or 0 documents, nothing to recommend!")

    elif method == 2:
        new_docs = rake(documents)
        populate_db(all_urls, new_docs)
        nodes, node_embeddings = get_embeddings_as_properties()
        predicted_edges = predict(node_embeddings)
        
        count = 0
        top_rec_name = []
        top_rec = []
        
        for key in predicted_edges:
            if count == 3:
                break
            if key[0] == url_name:
                top_rec_name.append(key[1])
                count += 1
            elif key[1] == url_name:
                top_rec_name.append(key[0])
                count += 1
             
        for i in top_rec_name:   
            for result in nodes:
                node: Node = result["node"]
                if not "name" in node._properties:
                    continue
                else:
                    if node._properties["name"] == i:
                        top_rec.append(node._properties["url"])
                        break
        print("Top three recommendations", top_rec)
        
        # TODO: ako je top_rec prazan, tj count==0 onda napraviti neku funkciju koja poveze s wikipedijom?
    
    # TODO: bez redirecta, dodati opciju da redirecta na recommendation ako zeli
    return redirect(url)

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
