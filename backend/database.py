from gqlalchemy import Memgraph, Match, Node
from typing import Dict, List, Tuple
import itertools
import gc
import numpy as np

#memgraph = Memgraph(host="memgraph-mage", port=7687)
memgraph = Memgraph()
PRECISION_AT_K_CONST = 2 ** 8

# jaccard's measure between two sets of keywords
def jaccard_set(set1, set2):
    
    intersection = len(list(set(set1).intersection(set2)))
    union = (len(set1) + len(set2)) - intersection
    if union == 0:
        return 0
    else:
        return float(intersection) / union

# creates url matrix based on jaccard's measure 
def create_matrix(key_sets): 
    
    length = len(key_sets)
    A = np.empty((length, length))
    
    for i in range(length):
        for j in range(length):
            if i == j:
                A[i][j] = 0
            else:
                A[i][j] = jaccard_set(key_sets[i], key_sets[j])
    return A

# import data into Memgraph db
def populate_db(urls, key_sets):
    
    similarity_matrix = create_matrix(key_sets)
    query = """MATCH (n) DETACH DELETE (n);"""
    memgraph.execute(query)
    
    # create nods of urls
    for url in urls:
        index = url.rfind('/')
        s = url[index+1:]
        query = """CREATE (n:WebPage) SET n.name = '{str}',  n.url = '{url}';""".format(url=url, str=s)
        memgraph.execute(query)

    for i in range(len(urls)):
        similar_nodes = []
        url = urls[i]
        row = similarity_matrix[i]
        row_as_array = np.array(row)
        n = 5
        # 5 most similar nods in certain row
        similar_nodes_indices = np.argpartition(row_as_array, -n)[-n:]
        
        for index in similar_nodes_indices:
            if index:
                similar_nodes.append(urls[index])
        
        # create realtionships
        for similar_node in similar_nodes:
            
            subquery1 = "'{url}'".format(url=url)
            subquery2 = "'{sim_node}'".format(sim_node=similar_node)
            if url != similar_node:
                query = "MERGE (n {url:" + subquery1 + "}) MERGE (m {url:" + subquery2 + "})" + \
                        "MERGE (n)-[r:SIMILAR_TO]-(m)"
                memgraph.execute(query)
                
    # embeddings
    query = """CALL node2vec.set_embeddings(False, 2.0, 0.5, 4, 5, 2) YIELD *;"""
    memgraph.execute(query)
                 
# exports "embedding" property from all nodes in Memgraph db    
def get_embeddings_as_properties():
    embeddings: Dict[str, List[float]] = {}
    
    results = list (
        Match() 
        .node(variable="node") 
        .return_() 
        .execute())

    for result in results:
        node: Node = result["node"]
        if not "embedding" in node._properties:
            continue
        embeddings[node._properties["name"]] = node._properties["embedding"]
    
    return results, embeddings

# calculates matrix based on embedding values and cosine similarity
def calculate_adjacency_matrix(embeddings: Dict[str, List[float]], threshold=0.0) -> Dict[Tuple[str, str], float]:
    
    def get_edge_weight(i, j) -> float:
        return np.dot(embeddings[i], embeddings[j])

    nodes = list(embeddings.keys())
    nodes = sorted(nodes)
    adj_mtx_r = {}
    cnt = 0
    for pair in itertools.combinations(nodes, 2):
    
        if cnt % 1000000 == 0:
            adj_mtx_r = {k: v for k, v in sorted(adj_mtx_r.items(), key=lambda item: -1 * item[1])}
            adj_mtx_r = {k: adj_mtx_r[k] for k in list(adj_mtx_r)[:3*PRECISION_AT_K_CONST]}
            gc.collect()

        """if cnt % 10000 == 0:
            print(cnt)"""

        weight = get_edge_weight(pair[0], pair[1])
        if weight <= threshold:
            continue
        cnt += 1
        adj_mtx_r[(pair[0], pair[1])] = get_edge_weight(pair[0], pair[1])

    return adj_mtx_r

# we need to sort predicted edges so that ones that are most likely to appear are first in list
def predict(embeddings):
    adj_matrix = calculate_adjacency_matrix(embeddings=embeddings, threshold=0.0)
    
    predicted_edge_list = adj_matrix
    sorted_predicted_edges = {k: v for k, v in sorted(predicted_edge_list.items(), key=lambda item: -1 * item[1])}
    
    return sorted_predicted_edges
        
