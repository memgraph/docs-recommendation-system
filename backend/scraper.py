from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin
from urllib.parse import urlparse
import pandas as pd
import requests
import httplib2
import os.path
import os
from csv import writer
from os.path import dirname, abspath


url = "https://memgraph.com/docs/memgraph"
http = httplib2.Http()

todo_urls=[]
todo_urls1=[]
all_urls = []
counter = 1
#PATH = abspath(dirname(__file__))
PATH = abspath(os.path.join(os.path.dirname(__file__),".."))
    
def first_run(url_a):
    
    response, content = http.request(url_a)
    soup = BeautifulSoup(content, features="lxml")
    
    for link in soup.find_all('a', href= True):
        path = link.get('href')
        if path and path.startswith('#'):
            continue
        if path and path.startswith('/'):
            path = urljoin(url, path)
        if path and path.endswith('/'):
            path = path[:-1]
        if check_domain(path) == True:
            if path not in all_urls:
                all_urls.append(path)
                todo_urls.append(path)
        """#ako ne zelimo provjeravati domenu ovo otkomentiramo i zakomentiramo prethodne cetiri linije
        urls.append(path)""" 
    while todo_urls:
        second_run()
   
    create_csv()

def second_run():
    url_a = todo_urls.pop(0)
    response, content = http.request(url_a)
    soup = BeautifulSoup(content, features="lxml")
    
    for link in soup.find_all('a', href= True):
        path = link.get('href')
        if path and path.startswith('#'):
            continue
        if path and path.startswith('/'):
            path = urljoin(url, path)
        if path and path.endswith('/'):
            path = path[:-1]
        if check_domain(path) == True:
            if path not in all_urls:
                all_urls.append(path)       
    
def create_csv():
    global counter, urls1

    with open(PATH + '\dataset\links.csv', 'w', encoding = 'utf8', newline='') as f:
        thewriter = writer(f)
        header = ['All URLs:']
        thewriter.writerow(header)
        for path in all_urls:
            thewriter.writerow([path])
                 
def check_domain(path):
    domain = urlparse(path).netloc
    maindomain = urlparse(url).netloc
    
    if domain == maindomain:
        return True
    else:
        return False
    
first_run(url)


