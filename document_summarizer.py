import re
from transformers import pipeline
    
# CODE ADAPTED FROM: https://huggingface.co/facebook/bart-large-cnn
# MODEL FROM: https://huggingface.co/facebook/bart-large-cnn

class document_summarizer:
    def __init__(self, reranker) -> None:
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.reranker = reranker

    def summarize(self, doc):
        return self.summarizer(doc, max_length=int(len(doc)/4), min_length=30, do_sample=False)

    def summarize_best_paragraph(self, query, passage):
        questions = self.divide_passage_into_questions(passage)
        ranked_passages = self.reranker.rerank(query, passage)
        return self.summarize(ranked_passages[0][0])

    def divide_passage_into_questions(self, text: str):
        questions = []
        window = ""
        sentences = re.split("(?<=[.!?])\s+", text)
        for s in sentences:
            if len(s) != 0:
                if s[-1] == "?":
                    if window != "":
                        window = window[1:]
                        questions.append(window)
                        window = ""
            window += " "+ s
        return questions
    

