import numpy as np
import pandas as pd
from data_preperation import load_json
import tfidf_search

def load_data_as_dataframe(filename):
    json_data = load_json(filename)
    dataframe = pd.DataFrame.from_dict(json_data, orient="index")
    dataframe = dataframe.reset_index(drop = True)
    return dataframe

def find_k_largest_indicies(array, k):
    indexed_array = []
    for i in range(0, len(array)):
        indexed_array.append([i, float(array[i])])
    indexed_array.sort(key = lambda x : x[1], reverse= True)
    return indexed_array[:k]

search_question = "How do I get finnacial help?"

dataframe = load_data_as_dataframe("prepared_data.json")
documents = dataframe["text"]
titles = dataframe["title"]

tfidf = tfidf_search.tfidf(documents = documents)
similarities = tfidf.search(search_question)

largest_indicies = find_k_largest_indicies(similarities, 5)
for i in largest_indicies:
    print(titles[i[0]])

