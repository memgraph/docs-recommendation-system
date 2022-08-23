import time
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_tf_idf(corpus):
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    dense = tfidf_matrix.todense()
    dense_list = dense.tolist()
    df = pd.DataFrame(dense_list, columns=feature_names)
    print(df)

    start = time.time()

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix) # TODO: vidjet jel algoritam za simetričnu matricu računa sve vrijednosti ili samo pola matrice
    print("cosine_sim:", cosine_sim)
    print("Time taken: %s seconds" % (time.time() - start))
    return cosine_sim

def get_recommendations(corpus):
    similarity_matrix = find_tf_idf(corpus)
    url_order_num = 0
    similarities = similarity_matrix[url_order_num]
    similarities = np.around(similarities, decimals=3)
    print("similarities:", similarities, "type:", type(similarities))
    print("data type:", type(similarities[0]), "value:", similarities[0])

    # exclude current document
    index = np.where(similarities == 1.)
    similarities[index] = -1.
    print("similarities:", similarities, "len:", len(similarities))

    n = 5
    sim_arr = np.array(similarities)
    top_recommendations = np.argsort(sim_arr)[-n:]
    print("top_recommendations", top_recommendations)
    print("top_similarities:", sim_arr[top_recommendations])

    return top_recommendations
