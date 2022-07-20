from flask import Flask, render_template, request, redirect
from extract_content import extract_content_from_url

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def redirect_docs():
    url = request.form["input-url"]
    content = extract_content_from_url(url)
    print(content)
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
