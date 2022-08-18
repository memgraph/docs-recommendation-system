from typing import List
import numpy as np
from gqlalchemy import Field, Match, Memgraph, Node, Relationship, Create

memgraph = Memgraph()
names = {}

class WebPage(Node):
    url: str = Field(index=True, exist=True, unique=True, db=memgraph)
    name: str = Field(index=True, exist=True, unique=True, db=memgraph)

class SimilarTo(Relationship, type="SIMILAR_TO"):
    pass

# jaccard's measure between two sets of keywords
def jaccard_set(set1, set2):
    
    intersection = len(list(set(set1).intersection(set2)))
    union = (len(set1) + len(set2)) - intersection
    
    return 0 if union == 0 else float(intersection) / union

# creates url matrix based on jaccard's measure 
def create_matrix(key_sets): 
    
    length = len(key_sets)
    A = np.empty((length, length))
    
    for i in range(length):
        for j in range(length):
            A[i][j] = 0 if i == j else jaccard_set(key_sets[i], key_sets[j])
    return A

def find2nd(string , ch) :
    s = string[::-1]
    occur = 0;
 
    for i in range(len(s)) :
        if (s[i] == ch) :
            occur += 1;
 
        if (occur == 2) :
            return len(s)-i-1;
    
    return -1;

def getName(string):
    index = string.rfind('/')
    name = string[index+1:]
    
    for key in names:
        if names[key] == name:
            index = find2nd(string, '/')
            name = string[index+1:]
    return name

# import data into Memgraph db
def populate_db(urls, key_sets):
    
    query = """MATCH (n) DETACH DELETE (n);"""
    memgraph.execute(query)
    
    # create nods of urls
    for url in urls:
        s = getName(url)
        names[url] = s
        WebPage(name=s, url=url).save(memgraph)
        
    similarity_matrix = create_matrix(key_sets)
    
    for i in range(len(urls)):
        similar_nodes = []
        url = urls[i]
        row = similarity_matrix[i]
        row_as_array = np.array(row)
        n = 5
        # 5 most similar nods in certain row
        similar_nodes_indices = np.argpartition(row_as_array, -n)[-n:]
        
        s = names[url]
        s_node = WebPage(url=url, name=s).load(db=memgraph)
       
        for index in similar_nodes_indices:
            if index:
                similar_nodes.append(urls[index])
        
        # create realtionships
        for similar_node in similar_nodes:
            e = names[similar_node]
            e_node = WebPage(url=similar_node, name=e).load(db=memgraph)
            
            if url != similar_node:
                similar_rel = SimilarTo(
                    _start_node_id = s_node._id,
                    _end_node_id = e_node._id
                ).save(memgraph)
                
    # embeddings 
    query = """CALL node2vec.set_embeddings(False, 2.0, 0.5, 4, 5, 2) YIELD *;"""
    memgraph.execute(query)