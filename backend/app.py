from flask import Flask, render_template, request, redirect
from scraper import get_links
from tf_idf import get_recommendations
from extractor import open_ai

app = Flask(__name__)

#u scraperu je stavljen break nakon 5 urlova

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def redirect_docs():
    url = request.form["input-url"]
    method = int(request.form["model-method"])

    documents, all_urls = get_links(url)
    
    if method == 1:
        if len(documents) > 1:
            recommendations = get_recommendations(documents)
            for i in recommendations:
                print("i:", i)
                print("all_urls[i]:", all_urls[i])
        else:
            print("Only 1 or 0 documents, nothing to recommend!")

    elif method == 2:
        new_docs = open_ai(documents)
        for i in new_docs:
            print("i: ", i)

    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
