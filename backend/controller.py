from typing import List
import numpy as np

from database import populate_db
from extractor import rake
from models.link_prediction import link_prediction
from models.node2vec import get_embeddings_as_properties, predict
from models.tf_idf import get_recommendations


class Controller:    
    def __init__(self):
        self.recs_indices = np.array([])
        self.similarities = []
        self.top_keywords = {}
        self.tf_idf_recs = []
        self.node2vec_recs = []
        self.link_prediction_recs = []

    def tf_idf(self, documents:List[str], all_urls:List[str]) -> bool: 
        if len(documents) > 1:
            self.recs_indices, self.similarities, self.top_keywords = get_recommendations(documents)
            self.tf_idf_recs = [all_urls[i] for i in self.recs_indices]
            return True
        return False

    def node2vec(self, documents:List[str], all_urls:List[str], url_name:str) -> None:
        new_docs = rake(documents)
        populate_db(all_urls, new_docs)
        nodes, node_embeddings = get_embeddings_as_properties()
        predicted_edges = predict(node_embeddings)

        num_of_recs = 0
        top_rec_name = []
        for key in predicted_edges:
            if num_of_recs == 3:
                break
            if key[0] == url_name:
                top_rec_name.append(key[1])
                num_of_recs += 1
            elif key[1] == url_name:
                top_rec_name.append(key[0])
                num_of_recs += 1

        for i in top_rec_name:
            for result in nodes:
                if(result["n_name"] == i):
                        self.node2vec_recs.append(result["n_url"])
                        break

    def link_prediction(self, url_name:str) -> None:
        nodes, precise_edges = link_prediction()

        num_of_recs = 0
        top_link_name = []

        for key in precise_edges:
            if num_of_recs == 3:
                break
            if key[0] == url_name:
                top_link_name.append(key[1])
                num_of_recs += 1
            elif key[1] == url_name:
                top_link_name.append(key[0])
                num_of_recs += 1

        for i in top_link_name:   
            for result in nodes:
                if(result["n_name"] == i):
                    self.link_prediction_recs.append(result["n_url"])
                    break  
