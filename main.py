import os
import string
from documents_retriever import load_data_as_dataframe
from answer_extraction import answer_extractor
from docuement_collector import _scrape_website
from data_preperation import prepare_data
from documents_retriever import filter_documents
from docuemenet_reranker import docuemenet_reranker
from document_summarizer import document_summarizer

# Summarizer, needs the articiles broken down into chunks
# Just steal the one from QA
# save results to a log file

def download_data():
    if os.path.exists("prepared_data.json"):
        dc = input("Do you want to (re)download the data? (Y/N):  ")
        if dc.lower() == "y":
            _scrape_website()
            prepare_data
            print("downloading...")
        elif dc.lower() != "n":
            raise Exception(f"Incorrect input: {dc}\n")
    else: 
        print("downloading...")
        _scrape_website()
        prepare_data

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
    tfidf_set, embed_set = filter_documents(question, 10)
    whole_set = tfidf_set.union(embed_set)
    whole_set = tfidf_set
    sorted_docs = reranker.rerank_indicies(question, whole_set)
    sorted_docs.sort(key = lambda x: x[1], reverse = True)
    doc_index = 0
    answers = qa.extract_answer(question, sorted_docs[doc_index][0])
    while len(answers) == 0: 
        doc_index += 1
        answers = qa.extract_answer(question, sorted_docs[doc_index][0])
    doc_index = sorted_docs[doc_index][0]

    log = print_log(log, "---- Answer Processing:\n")
    log = print_log(log, f"**** Used '{titles[doc_index]}' for Answer Processing")

    log = print_log(log, "---- Answer Extraction: \n")
    for ans in answers:
        log = print_log(log, f"{ans}" + "\n")

    log = print_log(log, "---- Summarizer: \n")
    best_doc = texts[sorted_docs[0][0]]
    log = print_log(log, f"{summarizer.summarize_best_chunk(question, best_doc)[0]['summary_text']} \n")

    log = print_log(log, "---- Document Processing:\n") 
    log = print_log(log, "---- Ranked Documenets:\n")
    for doc in sorted_docs:
        log = print_log(log, f"{titles[doc[0]]}" + f" {doc[1]}" +"\n")

    log = print_log(log, "---- TF-IDF:\n")
    for index in tfidf_set:
        log = print_log(log, titles[index] + "\n")
 
    log = print_log(log, "----Doc2Vec:\n")
    for index in embed_set:
        log = print_log(log, titles[index] + "\n")

    return log


# download_data()
docs = load_data_as_dataframe("prepared_data.json")
titles = docs["title"]
texts = docs["text"]
reranker = docuemenet_reranker(docs)
summarizer = document_summarizer(reranker=reranker)
qa = answer_extractor(docs)

log_index = 0

while True:
    print("\n\n")
    question = input("Enter your question: ")
    log = process_question(question)
    write_to_log(log, f"{log_index}.txt")
