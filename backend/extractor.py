import requests
import justext
import string
from gensim.parsing.preprocessing import remove_stopwords, strip_numeric
import re
import openai
from rake_nltk import Rake
import nltk

# TODO: obrisati openAi?

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

# extract keywords from given text using openAi's GPT-3
# TODO: vise ne koristimo ovo
def open_ai(documents):
    new_docs = []
    for text in documents:
        if not text:
            new_docs.append({" "})
            continue
        text = "Extract keywords from this text: \n" + text
        openai.api_key = "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"

        response = openai.Completion.create(
            model="text-davinci-002",
            #model="text-curie-001",
            prompt= text,
            #za text curie je najbolja temp 0
            temperature=0.2,
            max_tokens=80,
            top_p=1.0,
            frequency_penalty=0.8,
            presence_penalty=0.0
        )
        output_label = response["choices"][0]["text"]
        new = remove_stopwords(output_label)
        new_t = strip_numeric(new)
        new = new_t.translate(str.maketrans('', '', string.punctuation))
        new_text = re.sub(' +', ' ', new)

        keywords = new_text.split(" ")
        unique_keywords = set(filter(None, keywords))
       
        new_docs.append(unique_keywords)
        
    return new_docs
