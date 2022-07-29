import numpy as np
from gqlalchemy import Memgraph

memgraph = Memgraph(host="127.0.0.1", port=7687)

lista = []
a = {"apple", "banana", "cherry"}
b = {"google", "microsoft", "apple"}
#lista je kao nasa lista setova kljucnih rijeci
for i in range(5):
    lista.append(a)
    lista.append(b)
print("Lista setova:\n", lista)
#10 je imaginarna duljina all_urls
A = np.empty((10, 10))
#ovo su nam all_urls i oni moraju odgovarati duljini liste
urls= ["prvi", "drugi", "treci", "cetvrti", "peti", "sesti", "sedmi", "osmi", "deveti", "deseti"]
for i in range(len(lista)):
    for j in range(len(lista)):
        if i == j:
            A[i][j] = 0
        else:
            z = lista[i].intersection(lista[j])
            x = len(z)
            A[i][j] = x
    #A[i] = sorted(A[i], reverse=True)
B = A.astype(int)
print("Matrica:\n", B)
print("Max u matrici:\n", max(map(max, B)))
c = np.where(B==3)
print("Di se prvi put nalazi taj max:\n", c[0][0], c[1][0])


def populate_db(urls, similarity_matrix):
    for url in urls:
        query = """CREATE (n:WebPage) SET n.url = '{url}';""".format(url=url)
        memgraph.execute(query)

    for i in range(len(urls)):
        url = urls[i]
        row = similarity_matrix[i]
        row_as_array = np.array(row)
        n = 5
        similar_nodes_indices = np.argpartition(row_as_array, -n)[-n:]
        print("similar_nodes_indices", similar_nodes_indices)
        similar_nodes = [urls[index] for index in similar_nodes_indices]
        print("similar_nodes", similar_nodes)

        for similar_node in similar_nodes:
            subquery1 = "'{url}'".format(url=url)
            subquery2 = "'{sim_node}'".format(sim_node=similar_node)
            query = "MERGE (n {url:" + subquery1 + "}) MERGE (m {url:" + subquery2 + "})" + \
                    "MERGE (n)-[r:SIMILAR_TO]-(m)"
            memgraph.execute(query)

populate_db(urls, B)
