from flask import Flask, render_template, request, redirect
from scraper import get_links

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def redirect_docs():
    url = request.form["input-url"]
    print(url)
    documents = get_links(url)
    print("total docs: ", len(documents))
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
