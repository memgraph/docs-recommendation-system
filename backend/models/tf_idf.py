import heapq
from typing import Any, Dict, List, Set, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# get most frequent words from each document
def tf_idf_keywords(corpus: List[str]) -> List[Set[str]]:
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()
    
    new_doc = []
    for doc in corpus:
        tf_idf_vector = vectorizer.transform([doc])
        
        # sort the tf-idf vectors by descending order of scores
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        
        # extract only the top 30
        keywords = extract_topn_from_vector(feature_names, sorted_items, 30)
        new_doc.append(set(keywords))
             
    return new_doc

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

# get the feature names and tf-idf score of top n items
def extract_topn_from_vector(feature_names, sorted_items, topn=30):
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
        
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def tf_idf(corpus: List[str]) -> Tuple[Any, Dict[Any, tuple]]:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    dense_list = dense.tolist()
    df = pd.DataFrame(dense_list, columns=feature_names)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # get the column name of max values in every row
    most_important_words = list(df.idxmax(axis=1))

    word_frequencies = {}
    for word in most_important_words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    top_ten_freqs = heapq.nlargest(10, word_frequencies, key=word_frequencies.get)
    top_keywords = {key: (word_frequencies[key], round(word_frequencies[key]*100/len(corpus), 1)) 
                    for key in top_ten_freqs}
    
    return cosine_sim, top_keywords

# get recommendations based on tf-idf algorithm
def get_recommendations(corpus: List[str]) -> Tuple[np.ndarray, List[float], Dict[Any, tuple]]:
    similarity_matrix, top_keywords = tf_idf(corpus)
    url_order_num = 0
    similarities = similarity_matrix[url_order_num]
    similarities = np.around(similarities, decimals=3)

    # exclude current document
    index = np.where(similarities == 1.)
    similarities[index] = -1.

    top_n = 5
    sim_arr = np.array(similarities)
    top_recommendations = np.argsort(sim_arr)[-top_n:]
    similarities = list(sim_arr[top_recommendations])
    similarities.reverse()

    return np.flip(top_recommendations), similarities, top_keywords
