from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class tfidf:
    def __init__(self, documents):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
    
    def search(self, look_up_docuement): 
        sparse_matrix_x = self.vectorizer.transform([look_up_docuement])
        cosine_similarities = cosine_similarity(sparse_matrix_x, self.tfidf_matrix).flatten()
        return cosine_similarities

    def find_closest(self, search_question, k):
        similarities = self.search(search_question)
        indexed_array = []
        for i in range(0, len(similarities)):
            indexed_array.append([i, float(similarities[i])])
        indexed_array.sort(key = lambda x : x[1], reverse= True)
        return indexed_array[:k]