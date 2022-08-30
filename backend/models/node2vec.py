import gc
import itertools
from typing import Any, Dict, List, Tuple

import numpy as np
from gqlalchemy import Match

PRECISION_AT_K_CONST = 2 ** 8

# exports "embedding" property from all nodes in Memgraph db    
def get_embeddings_as_properties() -> Tuple[List[Dict[str, Any]], Dict[str, List[float]]]:
    embeddings: Dict[str, List[float]] = {}
 
    results = list (
        Match() 
        .node("WebPage", variable="node") 
        .return_(
            {"node.name" : "n_name", "node.url" : "n_url", "node.embedding" : "n_embedding"}) 
        .execute()
    )

    for result in results:
        embeddings[result["n_name"]] = result["n_embedding"]
    
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

        weight = get_edge_weight(pair[0], pair[1])
        if weight <= threshold:
            continue
        cnt += 1
        adj_mtx_r[(pair[0], pair[1])] = get_edge_weight(pair[0], pair[1])

    return adj_mtx_r

# we need to sort predicted edges so that ones that are most likely to appear are first in list
def predict(embeddings: Dict[str, List[float]]) -> Dict[Tuple[str, str], float]:
    adj_matrix = calculate_adjacency_matrix(embeddings=embeddings, threshold=0.0)
    
    predicted_edge_list = adj_matrix
    sorted_predicted_edges = {k: v for k, v in sorted(predicted_edge_list.items(), key=lambda item: -1 * item[1])}
    
    return sorted_predicted_edges
