from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity

# CODE ADAPTED FROM: https://huggingface.co/sentence-transformers/all-mpnet-base-v2
# MODEL FROM: https://huggingface.co/sentence-transformers/all-mpnet-base-v2

class docuemenet_reranker:
    def __init__(self, dataset) -> None:
        self.dataset = dataset["text"]
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')

    def rerank(self, search_query, paragraphs, df) ->  list:
        sentences = [search_query] + paragraphs
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        similarity_scores = cosine_similarity(sentence_embeddings)
        scores = similarity_scores[0][:]
        scores_paragraphs = list(zip(scores, sentences))
        return scores_paragraphs

    def rerank_indicies(self, search_query, indicies, df) ->  list:
        paragraphs = []
        for i in indicies:
            paragraphs.append(self.dataset[i])
        sentences = [search_query] + paragraphs
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        similarity_scores = cosine_similarity(sentence_embeddings)
        scores = similarity_scores[0][:]
        scores_paragraphs = list(zip(scores, indicies))
        return scores_paragraphs

    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)