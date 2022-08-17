import logging
import os
import validators
from flask import Flask, redirect, render_template, request
from database import memgraph, populate_db
from extractor import rake
from node2vec import get_embeddings_as_properties, predict
from scraper import get_links
from tf_idf import get_recommendations
from link_prediction import link_prediction

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
        # TODO: solve in frontend after enabling 
    
    ind = url.rfind('/')
    url_name = url[ind+1:]
    method = int(request.form["model-method"])
    documents, all_urls = get_links(url)
    
    # TODO: method 1 and 2 are solely for developing purposes
    # will be structured differently in frontend (no choosing methods, all will be available on the same page)
    if method == 1:
        if len(documents) > 1:
            recommendations = get_recommendations(documents)
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
                if(result["n_name"] == i):
                    top_rec.append(result["n_url"])
                    break
            
        print("Top three recommendations", top_rec)
        
        # link prediction
        nodes, precise_edges = link_prediction()
        
        count = 0
        top_link_name = []
        top_link_rec = []
        
        for key in precise_edges:
            if count == 3:
                break
            if key[0] == url_name:
                top_link_name.append(key[1])
                count += 1
            elif key[1] == url_name:
                top_link_name.append(key[0])
                count += 1
             
        for i in top_link_name:   
            for result in nodes:
                if(result["n_name"] == i):
                    top_link_rec.append(result["n_url"])
                    break
                
        print("\nTop three link prediction recommendations", top_link_rec)
        
        # TODO: if there are no top recommendations, redirect to certain docs/wiki page?
    
    # TODO: resolve in frontend (without redirect)
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