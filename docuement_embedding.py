import numpy as np
import pandas as pd
import gensim
import os
from data_preperation import load_json

# GENSIM DOES NOT WORK WITH RECENT RELEASES OF SCIPY BECAUSE OF DEPRECATIONS
# https://stackoverflow.com/questions/78279136/importerror-cannot-import-name-triu-from-scipy-linalg-when-importing-gens
# pip install scipy==1.10.1

# Code Adapted from: https://radimrehurek.com/gensim/auto_examples/tutorials/run_doc2vec_lee.html#sphx-glr-auto-examples-tutorials-run-doc2vec-lee-py
# USING THE GENSIM LIBRARY https://radimrehurek.com/gensim/

def load_data_as_dataframe(filename):
    json_data = load_json(filename)
    dataframe = pd.DataFrame.from_dict(json_data, orient="index")
    dataframe = dataframe.reset_index(drop = True)
    return dataframe

class docuement_embedding:
    def __init__(self, filename = None, vector_size = 50, min_count = 2, epochs = 40) -> None:
        if isinstance(filename, str):
            self.load_model(filename)
        else:
            self.model = gensim.models.doc2vec.Doc2Vec(vector_size = vector_size, min_count = min_count, epochs = epochs)
        
    def enable_logging(self):         
        # Adapted from: https://radimrehurek.com/gensim/auto_examples/tutorials/run_doc2vec_lee.html#sphx-glr-auto-examples-tutorials-run-doc2vec-lee-py
        import logging
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    def train(self, documents):
        training_set = self.tokenize_docuements(documents)
        self.model.build_vocab(training_set)
        self.model.train(training_set, total_examples = self.model.corpus_count, epochs = self.model.epochs)

    def tokenize_docuements(self, documents, tokens_only = False):
        return_docuements = []
        for i, doc in enumerate(documents):
            tokens = gensim.utils.simple_preprocess(doc)
            if tokens_only:
                return_docuements.append(tokens)
            else:
                return_docuements.append(gensim.models.doc2vec.TaggedDocument(tokens, [i]))
        return return_docuements

    def save_model(self, filename): 
        self.model.save(filename)

    def load_model(self, filename):
        if os.path.exists(filename):
            self.model = gensim.models.doc2vec.Doc2Vec.load(filename)
        else:
            raise FileNotFoundError(f"File {filename} does not exist")

    def find_closest(self, search, k):
        tokens = gensim.utils.simple_preprocess(search)
        search_vector = self.model.infer_vector(tokens)
        return self.model.dv.similar_by_vector(search_vector, topn = k)


if __name__ == "__main__":
    docs = load_data_as_dataframe("prepared_data.json")
    titles = docs["title"]
    embed = docuement_embedding(vector_size = 50, min_count = 2, epochs = 40)
    embed.train(list(docs["text"]))
    embed.save_model("doc2vec_embed.model")
    # embed.save_model("test_embed")
    # closet_doc = embed.find_closest(search = "What is a stage two misconduct?", k = 10)
    # for i in closet_doc:
    #     index = i[0]
    #     print(titles[index])