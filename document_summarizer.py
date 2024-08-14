import re
from transformers import pipeline
    
# CODE ADAPTED FROM: https://huggingface.co/facebook/bart-large-cnn
# MODEL FROM: https://huggingface.co/facebook/bart-large-cnn

class document_summarizer:
    def __init__(self, reranker) -> None:
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.reranker = reranker

    def sum(self, doc):
        return self.summarizer(doc, max_length=int(len(doc)/5), min_length=30, do_sample=False)
            

    def summarize_best_chunk(self, query, passage):
        chunks = self.chunk(passage)
        ranked_passages = self.reranker.rerank(query, chunks)
        ranked_passages.sort(key = lambda x: x[1], reverse = True)
        return self.sum(ranked_passages[1][0])


    def chunk(self, text: str):
        chunks = []
        window = ""
        sentences = re.split("(?<=[.!?])\s+", text)
        for s in sentences:
            if len(s) != 0:
                if len(window) > 3600:
                    if window != "":
                        window = window[1:]
                        chunks.append(window)
                        window = ""
            window += " "+ s
        if window.strip():
            chunks.append(window.strip())
        return chunks
    