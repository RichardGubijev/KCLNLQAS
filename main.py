import argparse
from web_scraper import scrape_website
from data_preperation import prepare_data
from documents_retriever import filter_documents, sort_docuements
from documents_retriever import load_data_as_dataframe
from answer_extraction import answer_extractor

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
    QUESTION = "When are exam resutls for period 3 released?"
    PASSAGE_ID = 11
    docs = load_data_as_dataframe("prepared_data.json")
    qa = answer_extractor(docs)
    answers = qa.extract_answer(QUESTION, PASSAGE_ID)

    for a in answers:
        print(f"{a[1]} - {a[0]}\n")

    # main()
