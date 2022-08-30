from typing import List, Set

import numpy as np
from gqlalchemy import Field, Memgraph, Node, Relationship

from utils.utils import create_matrix, get_name

memgraph = Memgraph()
names = {}

class WebPage(Node):
    url: str = Field(index=True, exist=True, unique=True, db=memgraph)
    name: str = Field(index=True, exist=True, unique=True, db=memgraph)

class SimilarTo(Relationship, type="SIMILAR_TO"):
    pass

# import data into Memgraph db
def populate_db(urls: List[str], key_sets: List[Set[str]]) -> None:
    
    query = """MATCH (n) DETACH DELETE (n);"""
    memgraph.execute(query)
    
    # create nodes of urls
    names.clear()
    for url in urls:
        s = get_name(names, url)
        names[url] = s
        WebPage(name=s, url=url).save(memgraph)
    
    similarity_matrix = create_matrix(key_sets)
    
    for i in range(len(urls)):
        similar_nodes = []
        url = urls[i]
        row = similarity_matrix[i]
        row_as_array = np.array(row)
        
        num_of_connections = 4
        # most similar nodes in certain row
        similar_nodes_indices = np.argpartition(row_as_array, -num_of_connections)[-num_of_connections:]
        
        s = names[url]
        s_node = WebPage(url=url, name=s).load(db=memgraph)
        
        for index in similar_nodes_indices:
            if index:
                similar_nodes.append(urls[index])
        
        # create relationships
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
