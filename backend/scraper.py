from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import httplib2
import os
from csv import writer
from os.path import abspath
from extractor import extract_text

http = httplib2.Http()

todo_urls = []
all_urls = []
counter = 1
PATH = abspath(os.path.join(os.path.dirname(__file__),".."))

documents = []

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

def first_run(url):
    global all_urls, todo_urls, documents
    all_urls, todo_urls, documents = [], [], []
    response, content = http.request(url)

    joined_path = is_valid_url(url, url)
    if joined_path:
        all_urls.append(joined_path)

    text = extract_text(content, "")
    documents.append(text)

    soup = BeautifulSoup(content, features="lxml")
    i = 0
    for link in soup.find_all('a', href=True):
        path = link.get('href')
        joined_path = is_valid_url(url, path)
        if joined_path:
            all_urls.append(joined_path)
            # todo_urls.append(joined_path)
            text = extract_text("", joined_path)
            documents.append(text)
            i += 1
            print(i)
            """if i == 5:
                break"""
    # i = 0
    """while todo_urls:
        i += 1
        print(i)
        second_run(url)"""
   
    create_csv()
    print("all urls:", all_urls)
    print("urls len:", len(all_urls), "docs len:", len(documents))
    return documents, all_urls

def second_run(url):
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
    
def create_csv():
    global counter

    with open(PATH + '\dataset\links.csv', 'w', encoding = 'utf8', newline='') as f:
        thewriter = writer(f)
        header = ['All URLs:']
        thewriter.writerow(header)
        for path in all_urls:
            thewriter.writerow([path])
                 
def check_domain(path, url):
    domain = urlparse(path).netloc
    maindomain = urlparse(url).netloc

    """print("domain:", domain)
    print("maindomain:", maindomain)"""
    if domain == maindomain:
        return True
    else:
        return False
    

def get_links(url):
    return first_run(url)
