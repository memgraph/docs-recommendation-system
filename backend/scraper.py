import os
from csv import writer
from multiprocessing.pool import ThreadPool
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
g_url = ""
counter = 0

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

def scrape(link):
    global documents, all_urls, counter
    
    counter += 1 
    path = link.get('href')
    joined_path = is_valid_url(g_url, path)
    if joined_path and counter < 15:
        all_urls.append(joined_path)
        text = extract_text("", joined_path)
        documents.append(text)
                
# extract all urls from given website using BS
def first_run(url):
    global all_urls, todo_urls, documents, g_url
    all_urls, todo_urls, documents = [], [], []
    response, content = http.request(url)

    joined_path = is_valid_url(url, url)
    if joined_path:
        all_urls.append(joined_path)

    text = extract_text(content, "")
    documents.append(text)
    g_url = url
    soup = BeautifulSoup(content, features="lxml")

    with ThreadPool(20) as pool:
        pool.map(scrape, soup.find_all('a', href=True))
        
    #create_csv()
    return documents, all_urls

# TODO: currently not used but still a possibility 
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

# TODO: currently not used but still a possibility
def create_csv():
    with open(PATH + '\dataset\links.csv', 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f)
        header = ['All URLs:']
        thewriter.writerow(header)
        for path in all_urls:
            thewriter.writerow([path])

# provides recommendations within the same documentation              
def check_domain(path, url):
    domain = urlparse(path).netloc
    maindomain = urlparse(url).netloc

    if domain == maindomain:
        return True
    else:
        return False
    
def get_links(url):
    return first_run(url)
