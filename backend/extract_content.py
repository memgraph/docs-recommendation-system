import requests
import justext

def extract_content_from_url(url):
    response = requests.get(url)
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    text = ""
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            text += paragraph.text + "\n"

    return text
