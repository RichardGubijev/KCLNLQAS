from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch.nn.functional as F
import torch
import re

# DISABLE SYMLINKS WARNING MESSAGE IN CONSOLE 
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# CODE ADAPTED FROM: https://huggingface.co/docs/transformers/main/en/model_doc/roberta#transformers.RobertaForQuestionAnswering
# MODEL FROM: https://huggingface.co/deepset/roberta-base-squad2

class answer_extractor:
    def __init__(self, dataset,  model_name = "deepset/roberta-base-squad2") -> None:
        self.dataset = dataset["text"]
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    def _answer(self, question, text):
        inputs = self.tokenizer(question, text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)

        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()
        predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
        
        start_probs = F.softmax(outputs.start_logits, dim=-1)
        end_probs = F.softmax(outputs.end_logits, dim=-1)

        # Compute the confidence score
        start_prob = start_probs[0, answer_start_index].item()
        end_prob = end_probs[0, answer_end_index].item()
        confidence_score = start_prob * end_prob
        
        return (str(self.tokenizer.decode(predict_answer_tokens, skip_special_tokens=True)).replace(question, ""), confidence_score)

    def extract_answer(self, question, passage_id):
        divided_passages = self.divide_passage_into_questions(self.dataset[passage_id])
        answers = []
        for p in divided_passages:
            if len(p) > 250:
                for i in range(0,len(p) - 250 + 1, 100):
                    window = p[i:i+250]
                    answer = self._answer(question, window)
                    # if answer[0] != "" and answer[0] != " " and answer[0] != "\t" and answer[0] != "\n" and answer[0] != "\s" and len(answer[0]) != 0:
                    if answer[0].strip() != "":
                        answers.append(answer)

            else:
                answer = self._answer(question, p)
                if answer[0].strip() != "":
                    answers.append(answer)

        answers.sort(key= lambda x : x[1], reverse= True)

        return answers

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