import string
import time
from documents_retriever import load_data_as_dataframe
from answer_extraction import answer_extractor
from documents_retriever import filter_documents
from docuemenet_reranker import docuemenet_reranker
from document_summarizer import document_summarizer

def write_to_log(text, filename):
    with open(filename, "w+", encoding= "utf-8") as log_file:
        log_file.write(text)

def print_log(log, text):
    log += text
    print(text)
    return log

def process_question(question): 
    question = question.lower()
    question = question.translate(str.maketrans('', '', string.punctuation))
    log = f"Question: '{question}'\n"
    log = print_log(log, "\n")
    tfidf_set, embed_set = filter_documents(question, 10)
    whole_set = tfidf_set.union(embed_set)
    sorted_docs = reranker.rerank_indicies(question, whole_set)
    sorted_docs.sort(key = lambda x: x[1], reverse = True)
    log = print_log(log, "---- Answer Processing:\n")
    for sorted_doc_index in range(0,5):
        doc_index = sorted_docs[sorted_doc_index][0]
        log = print_log(log, f"****'{sorted_doc_index} - {titles[doc_index]}\n'")

        log = print_log(log, "---- Answer Extraction: \n")
        answers = qa.extract_answer(question, doc_index)
        for ans in answers:
            log = print_log(log, f"{ans[0]}" + "\n")
        log = print_log(log, "\n")
        log = print_log(log, "---- Summarizer: \n")
        log = print_log(log, f"{summarizer.summarize_best_chunk(question, texts[doc_index])[0]['summary_text']} \n")
        log = print_log(log, "\n")
    log = print_log(log, "\n-----------------------\n")
    log = print_log(log, "---- Document Processing:\n") 
    log = print_log(log, "---- Ranked Documenets:\n")
    for sorted_doc_index in sorted_docs:
        log = print_log(log, f"{titles[sorted_doc_index[0]]}" + f" {sorted_doc_index[1]}" +"\n")
    log = print_log(log, "\n")
    log = print_log(log, "---- TF-IDF:\n")
    for index in tfidf_set:
        log = print_log(log, titles[index] + "\n")
    log = print_log(log, "\n")
    log = print_log(log, "----Doc2Vec:\n")
    for index in embed_set:
        log = print_log(log, titles[index] + "\n")

    return log

df = load_data_as_dataframe("prepared_data.json")
titles = df["title"]
texts = df["text"]
reranker = docuemenet_reranker(df)
summarizer = document_summarizer(reranker=reranker)
qa = answer_extractor(df)

QUESTIONS = []

log_index = 0
for q in QUESTIONS:
    start_time = time.time()
    log = process_question(q)
    write_to_log(log, f"{log_index}.txt")
    log_index += 1
    print(f"Took: f{time.time() - start_time}")
