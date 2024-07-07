from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from data_preperation import load_json

class tfidf:
    def __init__(self, documents):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
    
    def search(self, look_up_docuement): 
        sparse_matrix_x = self.vectorizer.transform([look_up_docuement])
        cosine_similarities = cosine_similarity(sparse_matrix_x, self.tfidf_matrix).flatten()
        return cosine_similarities
