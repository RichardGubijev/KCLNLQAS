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

question = ""

doc_indexes = []

for index in doc_indexes:
    print(f"Article: '{index} - {titles[index]}\n'")
    answers = qa.extract_answer(question, index)
    print( "Answer Extraction: \n")
    for ans in answers:
        print( f"{ans[0]}" + "\n")
    print( "\n")
    print( "Summarizer: \n")
    print( f"{summarizer.summarize_best_chunk(question, texts[index])[0]['summary_text']} \n")
    print( "\n")