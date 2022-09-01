import time
from typing import Any, Dict, List, Tuple

from database import memgraph
from gqlalchemy import Match, Node
from sklearn.model_selection import train_test_split

from .node2vec import calculate_adjacency_matrix, get_embeddings_as_properties

def get_all_edges() -> List[Tuple[Node, Node]]:
    results = Match() \
        .node(labels="WebPage", variable="node_a") \
        .to(relationship_type="SIMILAR_TO", variable="edge") \
        .node(labels="WebPage", variable="node_b") \
        .return_() \
        .execute()
        
    return [(result["node_a"], result["node_b"]) for result in results]

# split edges in train, test group
def split_edges_train_test(edges: List[Tuple[Node, Node]], test_size: float = 0.2) -> (
        Tuple[List[Tuple[Node, Node]], List[Tuple[Node, Node]]]):
    edges_train, edges_test = train_test_split(edges, test_size=test_size, random_state=int(time.time()))

    return edges_train, edges_test

def remove_edges(edges: List[Tuple[Node, Node]]) -> None:
    for edge in edges:
        query = Match() \
                .node(labels="WebPage", name = edge[0].name) \
                .to(relationship_type="SIMILAR_TO", variable="f") \
                .node(labels="WebPage", name = edge[1].name) \
                .delete("f") \
                .execute() 
    
def link_prediction() -> Tuple[List[Dict[str, Any]], Dict[Tuple[str, str], float]]:
    edges = get_all_edges()
   
    edges_train, edges_test = split_edges_train_test(edges=edges, test_size=0.2)
    remove_edges(edges_test)

    train_edges_dict = {(node_from.name, node_to.name): 1 for node_from, node_to in edges_train}
    test_edges_dict = {(node_from.name, node_to.name): 1 for node_from, node_to in edges_test}
    
    # calculate and get node embeddings
    query = """CALL node2vec.set_embeddings(False, 2.0, 0.5, 4, 5, 2) YIELD *;"""
    memgraph.execute(query)
   
    nodes, node_embeddings = get_embeddings_as_properties()
   
    # calculate adjacency matrix from embeddings
    adj_matrix = calculate_adjacency_matrix(embeddings=node_embeddings, threshold=0.0)
    predicted_edge_list = adj_matrix

    # we need to sort predicted edges so that ones that are most likely to appear are first in list
    sorted_predicted_edges = {k: v for k, v in sorted(predicted_edge_list.items(), key=lambda item: -1 * item[1])}
    
    return nodes, sorted_predicted_edges
