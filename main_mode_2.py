import string
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

docs = load_data_as_dataframe("prepared_data.json")
titles = docs["title"]
texts = docs["text"]
reranker = docuemenet_reranker(docs)
summarizer = document_summarizer(reranker=reranker)
qa = answer_extractor(docs)

# QUESTIONS = [
#     "I have been spiked, what should I do?", 
#     "How can I register with a doctor?", 
#     "I am homeless, what support can I get?", 
#     "When do graduation ceremonies take place?",
#     "What is the sunflower disability lanyard scheme?",
#     "Can I travel abroad with a student visa?",
#     "Who can help me with long term mental health conditions?",
#     "When is the second exam period?",
#     "By when do I need to apply for mitigating circumstances?",
#     "When are transcripts released?"
#     ]

QUESTIONS = [
    "I have been a victim of a crime, what should I do?",
    "I am disabled student what support is there for me?"]

log_index = 0
for q in QUESTIONS:
    log = process_question(q)
    write_to_log(log, f"{log_index}.txt")
    log_index += 1
