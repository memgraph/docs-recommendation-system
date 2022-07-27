import requests
import justext

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

