import os
from http import HTTPStatus
from multiprocessing.pool import ThreadPool
from os.path import abspath
from typing import List, Tuple
from urllib.parse import urljoin, urlparse

import httplib2
from bs4 import BeautifulSoup

from utils.extractor import extract_text

class Scraper:
    http = httplib2.Http()
    PATH = abspath(os.path.join(os.path.dirname(__file__),".."))

    def __init__(self):
        self.all_urls = []
        self.documents = []
        self.g_url = ""
    
    # provides recommendations within the same documentation
    def check_domain(self, path: str, url:str):
        domain = urlparse(path).netloc
        maindomain = urlparse(url).netloc

        return True if domain == maindomain else False
    
    # clean up url and check its domain
    def is_valid_url(self, url: str, path: str) -> bool:
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

    # get all links from given page and its content 
    def scrape(self, link: str) -> None:
        path = link.get('href')
        joined_path = self.is_valid_url(self.g_url, path)
        if joined_path:
            text = extract_text("", joined_path)
            if text and joined_path not in self.all_urls:
                self.all_urls.append(joined_path)
                self.documents.append(text)
                   
    # extract all urls from given website using BS
    def get_links_and_documents(self, url: str) -> Tuple[List[str], List[str], int]:
        self.all_urls, self.documents = [], []
        self.g_url = url
        response, content = self.http.request(url)
        
        if response.status == HTTPStatus.NOT_FOUND:
            return [], [], HTTPStatus.NOT_FOUND
        
        joined_path = self.is_valid_url(url, url)
        if joined_path:
            text = extract_text(content, "")
            if text and joined_path not in self.all_urls:
                self.all_urls.append(joined_path)
                self.documents.append(text)
            
        soup = BeautifulSoup(content, features="lxml")

        with ThreadPool(30) as pool:
            pool.map(self.scrape, soup.find_all('a', href=True))
            
        return self.documents, self.all_urls, HTTPStatus.OK
