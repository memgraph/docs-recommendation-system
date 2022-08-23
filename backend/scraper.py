import os
from csv import writer
from os.path import abspath
from urllib.parse import urljoin, urlparse

import httplib2
from bs4 import BeautifulSoup

from extractor import extract_text

http = httplib2.Http()
PATH = abspath(os.path.join(os.path.dirname(__file__),".."))
todo_urls = []
all_urls = []
documents = []
counter = 1

# clean up url and check its domain
def is_valid_url(url, path):
    if path and "#" in path:
        return False
    if path and path.startswith('/'):
        path = urljoin(url, path)
    if path and path.endswith('/'):
        path = path[:-1]
    if check_domain(path, url):
        if path not in all_urls:
            return path
    return False

# extract all urls from given website using BS
def first_run(url: str):
    global all_urls, todo_urls, documents
    all_urls, todo_urls, documents = [], [], []

    response, content = http.request(url)

    if response.status == 404:
        return [], [], 404

    joined_path = is_valid_url(url, url)
    if joined_path:
        all_urls.append(joined_path)

    text = extract_text(content, "")
    documents.append(text)

    soup = BeautifulSoup(content, features="lxml")
    for link in soup.find_all('a', href=True):
        path = link.get('href')
        joined_path = is_valid_url(url, path)
        if joined_path:
            all_urls.append(joined_path)
            text = extract_text("", joined_path)
            documents.append(text)
   
    #create_csv()
    return documents, all_urls, 200

def second_run(url: str):
    url_a = todo_urls.pop(0)
    response, content = http.request(url_a)

    text = extract_text(content, "")
    documents.append(text)

    soup = BeautifulSoup(content, features="lxml")
    
    for link in soup.find_all('a', href=True):
        path = link.get('href')
        joined_path = is_valid_url(url, path)
        if joined_path:
            all_urls.append(joined_path)
            text = extract_text("", joined_path)
            documents.append(text)

def create_csv() -> None:
    with open(PATH + '\dataset\links.csv', 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f)
        header = ['All URLs:']
        thewriter.writerow(header)
        for path in all_urls:
            thewriter.writerow([path])

# provides recommendations within the same documentation              
def check_domain(path: str, url: str):
    domain = urlparse(path).netloc
    maindomain = urlparse(url).netloc

    return True if domain == maindomain else False

def get_links_and_documents(url: str):
    return first_run(url)
