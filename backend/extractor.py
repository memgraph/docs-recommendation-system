import requests
import justext
import string
from gensim.parsing.preprocessing import remove_stopwords, strip_numeric
import os
import re
import openai

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

new_docs = []

def open_ai(documents):
    for text in documents:
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

        array = new_text.split(" ")
        test_list = list(filter(None, array))
       
        new_docs.append(test_list)
        
    return new_docs