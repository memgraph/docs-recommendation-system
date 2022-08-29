from typing import List, Set

import justext
import nltk
import requests
from nltk.stem import WordNetLemmatizer

# extract plain text from certain url using jusText, without unnecessary sidebars, tags, footers, etc.
def extract_text(content, url: str) -> str:
    if url:
        response = requests.get(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    else:
        paragraphs = justext.justext(content, justext.get_stoplist("English"))

    stopwords = nltk.corpus.stopwords.words('english')
    lemmatizer = WordNetLemmatizer()

    text = ""
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            paragraph = paragraph.text.lower().split()
            paragraph = [lemmatizer.lemmatize(word) for word in paragraph if not (word in set(stopwords) or word.isnumeric())]
            if len(paragraph):
                paragraph = ' '.join(paragraph)
                text += paragraph + " "

    return text
