from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import httplib2
import os
from csv import writer
from os.path import abspath
from extract_content import extract_text

http = httplib2.Http()

todo_urls = []
all_urls = []
counter = 1
PATH = abspath(os.path.join(os.path.dirname(__file__),".."))

documents = []

def first_run(url):
    global all_urls, documents
    all_urls = []
    response, content = http.request(url)

    text = extract_text(content, "")
    documents.append(text)
    print(documents)

    soup = BeautifulSoup(content, features="lxml")
    
    for link in soup.find_all('a', href=True):
        path = link.get('href')
        if path and path.startswith('#'):
            continue
        if path and path.startswith('/'):
            path = urljoin(url, path)
        if path and path.endswith('/'):
            path = path[:-1]
        if check_domain(path, url):
            if path not in all_urls:
                all_urls.append(path)
                todo_urls.append(path)
        """#ako ne zelimo provjeravati domenu ovo otkomentiramo i zakomentiramo prethodne cetiri linije
        urls.append(path)"""
    # print("todo_urls:", todo_urls)
    while todo_urls:
        second_run(url)
        break
   
    create_csv()
    print(len(documents))
    return documents

def second_run(url):
    url_a = todo_urls.pop(0)
    print(url_a)
    response, content = http.request(url_a)

    text = extract_text(content, "")
    documents.append(text)
    print(len(documents))

    soup = BeautifulSoup(content, features="lxml")
    
    for link in soup.find_all('a', href=True):
        path = link.get('href')
        if path and path.startswith('#'):
            continue
        if path and path.startswith('/'):
            path = urljoin(url, path)
        if path and path.endswith('/'):
            path = path[:-1]
        if check_domain(path, url):
            if path not in all_urls:
                all_urls.append(path)
                text = extract_text("", path)
                documents.append(text)
                print(path)
    # print("all_urls:", all_urls)
    
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

    # print("domain:", domain)
    # print("maindomain:", maindomain)
    if domain == maindomain:
        return True
    else:
        return False
    

def get_links(url):
    return first_run(url)
