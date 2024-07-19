from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

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

        return self.tokenizer.decode(predict_answer_tokens, skip_special_tokens=True)

    def extract_answer(self, question, passage_id):
        text = self.dataset[passage_id]
        answers = []
        if len(text) > 250:
            for i in range(0,len(text) - 250 + 1, 100):
                window = text[i:i+250]
                answers.append(self._answer(question, window))
        else: 
            answers.append(self._answer(question, text))

        return answers
