import requests
import justext
from rake_nltk import Rake
import nltk

# extract plain text from certain url using jusText, without unnecessary sidebars, tags, footers, etc.
def extract_text(content, url):
    if url:
        response = requests.get(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    else:
        paragraphs = justext.justext(content, justext.get_stoplist("English"))

    text = ""
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            text += paragraph.text + "\n"

    return text

# extract keywords from given text using rake_nltk
def rake(documents):
    nltk.download('stopwords')
    nltk.download('punkt')
    new_docs = []
    r = Rake()
    for text in documents:
        if not text:
            new_docs.append({" "})
            continue
        r.extract_keywords_from_text(text)
        a = set(r.get_ranked_phrases())
        new_docs.append(a)   
    return new_docs