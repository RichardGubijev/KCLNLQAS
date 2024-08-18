from documents_retriever import load_data_as_dataframe
from answer_extraction import answer_extractor
from document_summarizer import document_summarizer
from docuemenet_reranker import docuemenet_reranker

df = load_data_as_dataframe("prepared_data.json")
titles = df["title"]
texts = df["text"]

reranker = docuemenet_reranker(df)
qa = answer_extractor(df)
summarizer = document_summarizer(reranker)


QUESTIONS = [
    "I have been a victim of a crime, what should I do?", 
    "How can I register with a doctor?", 
    "I am homeless, what support can I get?", 
    "When do graduation ceremonies take place?",
    "I am disabled student what support is there for me?",
    "Can I travel abroad with a student visa?",
    "Who can help me with long term mental health conditions?",
    "When is the second exam period?",
    "By when do I need to apply for mitigating circumstances?",
    "When are transcripts released?"
    ]


# question = "When is the second exam period?"
# doc_indexes = [144, 12, 50]
# question = "Can I travel abroad with a student visa?"
# doc_indexes = [433, 430]
# question = "When do graduation ceremonies take place?"
# doc_indexes = [338, 337, 331]
# question = "By when do I need to apply for mitigating circumstances?"
# doc_indexes = [164, 165, 162, 129]
question = "I am homeless, what support can I get?"
doc_indexes = [391, 284, 6, 412, 407, 17]

for index in doc_indexes:
    print(f"Article: '{index} - {titles[index]}\n'")
    # answers = qa.extract_answer(question, index)
    # print( "Answer Extraction: \n")
    # for ans in answers:
    #     print( f"{ans[0]}" + "\n")
    # print( "\n")
    print( "Summarizer: \n")
    print( f"{summarizer.summarize_best_chunk(question, texts[index])[0]['summary_text']} \n")
    print( "\n")