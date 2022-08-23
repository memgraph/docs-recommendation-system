from typing import List, Set

import justext
import nltk
import requests
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake

# extract plain text from certain url using jusText, without unnecessary sidebars, tags, footers, etc.
def extract_text(content, url: str) -> str:

    """nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')"""
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
            paragraph = paragraph.text
            paragraph = paragraph.lower()
            paragraph = paragraph.split()
            paragraph = [lemmatizer.lemmatize(word) for word in paragraph if not word in set(stopwords) and not word.isnumeric()]
            if len(paragraph):
                paragraph = ' '.join(paragraph)
                text += paragraph + " "

    return text

# extract keywords from given text using rake_nltk
def rake(documents: List[str]) -> List[Set[str]]:
    """nltk.download('stopwords')
    nltk.download('punkt')"""
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
