from typing import Dict, List, Set

import numpy as np

# jaccard's measure between two sets of keywords
def jaccard_measure(set1: Set[str], set2: Set[str]) -> float:
    intersection = len(list(set(set1).intersection(set2)))
    union = (len(set1) + len(set2)) - intersection

    return 0 if union == 0 else float(intersection) / union

# creates url matrix based on jaccard's measure 
def create_matrix(key_sets: List[Set[str]]): 
    
    length = len(key_sets)
    A = np.empty((length, length))
    
    for i in range(length):
        for j in range(length):
            A[i][j] = 0 if i == j else jaccard_measure(key_sets[i], key_sets[j])
    return A

# find num-th occurrence of character in string
def find_next(string: str, ch: str, num: int) -> int:
    s = string[::-1]
    occur = 0
 
    for i in range(len(s)) :
        if s[i] == ch: occur += 1
        if occur == num: return len(s)-i-1
    
    return -1

# get unique tail of certain URL
def get_name(names: Dict[str, str] , string: str) -> str:
    index = string.rfind('/')
    name = string[index+1:]
    flag, num = True, 1
    
    while flag:
        flag = False
        for key in names:
            if names[key] == name:
                flag = True
                num += 1 
                index = find_next(string, '/', num)
                name = string[index+1:]
    return name
