import os
from csv import writer
from multiprocessing.pool import ThreadPool
from os.path import abspath
from urllib.parse import urljoin, urlparse

import httplib2
from bs4 import BeautifulSoup

from extractor import extract_text

class Scraper:
    http = httplib2.Http()
    PATH = abspath(os.path.join(os.path.dirname(__file__),".."))

    todo_urls = []
    all_urls = []
    documents = []
    g_url = ""
    
    # clean up url and check its domain
    def is_valid_url(self, url, path):
        if path and "#" in path:
            return False
        if path and path.startswith('/'):
            path = urljoin(url, path)
        if path and path.endswith('/'):
            path = path[:-1]
        if self.check_domain(path, url):
            if path not in self.all_urls:
                return path
        return False

    def scrape(self, link):
        path = link.get('href')
        joined_path = self.is_valid_url(self.g_url, path)
        if joined_path:
            text = extract_text("", joined_path)
            if text and joined_path not in self.all_urls:
                self.all_urls.append(joined_path)
                self.documents.append(text)
                   
    # extract all urls from given website using BS
    def first_run(self, url):
        self.all_urls, self.documents = [], []
        self.g_url = url
        response, content = self.http.request(url)
        
        if response.status == 404:
            return [], [], 404
        
        joined_path = self.is_valid_url(url, url)
        if joined_path:
            text = extract_text(content, "")
            if text and joined_path not in self.all_urls:
                self.all_urls.append(joined_path)
                self.documents.append(text)
            
        soup = BeautifulSoup(content, features="lxml")

        with ThreadPool(20) as pool:
            pool.map(self.scrape, soup.find_all('a', href=True))
            
        #self.create_csv()
        return self.documents, self.all_urls, 200

    # TODO: currently not used but still a possibility 
    def second_run(self, url):
        url_a = self.todo_urls.pop(0)
        response, content = self.http.request(url_a)

        text = extract_text(content, "")
        self.documents.append(text)

        soup = BeautifulSoup(content, features="lxml")
        
        for link in soup.find_all('a', href=True):
            path = link.get('href')
            joined_path = self.is_valid_url(url, path)
            if joined_path and joined_path not in self.all_urls:
                self.all_urls.append(joined_path)
                text = extract_text("", joined_path)
                self.documents.append(text)

    # TODO: currently not used but still a possibility
    def create_csv(self) -> None:
        with open(self.PATH + '\dataset\links.csv', 'w', encoding='utf8', newline='') as f:
            thewriter = writer(f)
            header = ['All URLs:']
            thewriter.writerow(header)
            for path in self.all_urls:
                thewriter.writerow([path])

    # provides recommendations within the same documentation
    def check_domain(self, path: str, url:str):
        domain = urlparse(path).netloc
        maindomain = urlparse(url).netloc

        return True if domain == maindomain else False
    
def get_links_and_documents(url:str):
    scraper = Scraper()
    return scraper.first_run(url)
