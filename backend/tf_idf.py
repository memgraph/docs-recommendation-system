import heapq
import time
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tf_idf(corpus: List[str]):
    #start = time.time()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    dense_list = dense.tolist()
    df = pd.DataFrame(dense_list, columns=feature_names)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    #-----------------------------------------------------------------------

    # get the column name of max values in every row
    most_important_words = list(df.idxmax(axis=1))

    word_frequencies = {}
    for word in most_important_words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    top_ten_freqs = heapq.nlargest(10, word_frequencies, key=word_frequencies.get)
    top_keywords = {key: (word_frequencies[key], round(word_frequencies[key]*100/len(corpus), 1)) 
                    for key in top_ten_freqs}

    print("top_keywords:", top_keywords, "\n")

    # print("Time taken: %s seconds" % (time.time() - start))
    
    return cosine_sim, top_keywords

def get_recommendations(corpus: List[str]):
    similarity_matrix, top_keywords = tf_idf(corpus)
    url_order_num = 0
    similarities = similarity_matrix[url_order_num]
    similarities = np.around(similarities, decimals=3)

    # exclude current document
    index = np.where(similarities == 1.)
    similarities[index] = -1.

    n = 5
    sim_arr = np.array(similarities)
    top_recommendations = np.argsort(sim_arr)[-n:]
    similarities = list(sim_arr[top_recommendations])
    similarities.reverse()

    return np.flip(top_recommendations), similarities, top_keywords
