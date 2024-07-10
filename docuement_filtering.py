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

if __name__ == "__main__":
    search_question = "I am having mental health issues, what help is there?"
    k = 10

    dataframe = load_data_as_dataframe("prepared_data.json")
    documents = dataframe["text"]
    titles = dataframe["title"]

    tfidf = tfidf_search.tfidf(documents = documents)
    largest_indicies = tfidf.find_closest(search_question, k)

    embed = docuement_embedding("doc2vec_embed.model")
    closet_doc = embed.find_closest(search_question, k)

    print("TFIDF")
    for i in largest_indicies:
        print(f"{i[1]} - {titles[i[0]]}")

    print("DOC2VEC")
    for i in closet_doc:
        print(f"{i[1]} - {titles[i[0]]}")

