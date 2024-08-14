import numpy as np
import pandas as pd
from data_preperation import load_json
import tfidf_search
from docuement_embedding import docuement_embedding

def load_data_as_dataframe(filename):
    json_data = load_json(filename)
    dataframe = pd.DataFrame.from_dict(json_data, orient="index")
    dataframe = dataframe.reset_index(drop = True)
    return dataframe

def filter_documents(question_query, k = 10):
    dataframe = load_data_as_dataframe("prepared_data.json")
    documents = dataframe["text"]

    tfidf = tfidf_search.tfidf(documents = documents)
    tfidf_closest_indicies = tfidf.find_closest(question_query, k)

    embed = docuement_embedding("doc2vec_embed.model")
    embed_closest_indicies = embed.find_closest(question_query, k)

    tfid_set = set()
    embed_set = set()
    for i in range(0, len(tfidf_closest_indicies)):
        tfid_set.add(tfidf_closest_indicies[i][0])
        embed_set.add(embed_closest_indicies[i][0])
    return tfid_set, embed_set

def debug_print(tfidf, embed):
    dataframe = load_data_as_dataframe("prepared_data.json")
    documents = dataframe["text"]
    titles = dataframe["title"]
    found = []
    clashed = []

    print("TFIDF")
    for i in tfidf:
        print(f"{i[1]} - {titles[i[0]]}")
        found.append(titles[i[0]])

    print("DOC2VEC")
    for i in embed:
        print(f"{i[1]} - {titles[i[0]]}")
        if titles[i[0]] in found:
            clashed.append(titles[i[0]])

    print(f"Clashed: {clashed}")
    print(f"length: {len(clashed)}")


if __name__ == "__main__":
    pass