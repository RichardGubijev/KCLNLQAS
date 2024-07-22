import argparse
from web_scraper import scrape_website
from data_preperation import prepare_data
from documents_retriever import filter_documents
from documents_retriever import load_data_as_dataframe
from answer_extraction import answer_extractor
from docuemenet_reranker import docuemenet_reranker
from document_summarizer import document_summarizer

def main():
    parser = argparse.ArgumentParser(description="A NLQAS CLI tool for KCL Services")
    parser.add_argument("-q", "--query", dest="query", help="Your query to answer")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-d", "--download", dest="download", action="store_true", help="Download/parse the dataset from self-service.kcl.ac.uk")
    args = parser.parse_args()  

    if args.download == True:
        print("Scraping website...")
        scrape_website()
        print("Preparing Data...")
        prepare_data()
        print("Done...")

    if args.query:
        docs = load_data_as_dataframe("prepared_data.json")
        filtered_docs = filter_documents(args.query, 10)
        sorted_docs = sort_docuements(args.query, filtered_docs)
        print(f"Query: {args.query}")
        
        if args.verbose:
            for i in range(len(sorted_docs)):
                doc_index = sorted_docs[i][0]
                doc_sim = sorted_docs[i][1]
                print(f"Title")
                print(f"Title")



if __name__ == "__main__":
    QUESTION = "When can I retake my exams?"
    docs = load_data_as_dataframe("prepared_data.json")
    titles = docs["title"]
    texts = docs["text"]
    filtered_docs_ind = filter_documents(QUESTION, 10)
    reranker = docuemenet_reranker(docs)
    summarizer = document_summarizer(reranker=reranker)
    sorted_docs = reranker.rerank_indicies(QUESTION, filtered_docs_ind)
    qa = answer_extractor(docs)
    answers = qa.extract_answer(QUESTION, sorted_docs[0][0])
    print("QUESTION:" , QUESTION, "\n")

    for i in sorted_docs:
        print(titles[i[0]])
        print(i, "\n")

    print("ANSWERS FROM DOC 1 \n")

    for a in answers:
        print(a[0], " - ", a[1])

    # print("\nDOCUEMENT SUMMARIZED\n")
    # index = sorted_docs[0][0]
    # print(summarizer.summarize(texts[index]))
    # print(summarizer.summarize_best_paragraph(QUESTION,texts[sorted_docs[0][0]]))

    # main()
