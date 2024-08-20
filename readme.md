# KCL NLQAS

All source code files contained in main directory, result logs are in aptly named `testingresults` folder. 

All requirmenets listed in requirements.txt

To download requirmenets run `pip install -r requirements.txt`

Might require installing pytorch manually.

To run the code `python main_mode_1.py`

Files and description:
docuement_collector.py - The web scraper
data_preperation.py - Prepares the data collected by the web scraper

tfidf_search.py - TF-IDF search for documenets
docuement_embedding.py - The model code for the doc2vec embedding
documents_retriever.py - The code for stage one of IR
doc2vec_embed.model - Trained model for this project
docuemenet_reranker.py - The model code for the reranker

answer_extraction.py - Contains the code for extractive QA model
document_summarizer.py - Contains the code for the summarizer model

main_mode_1.py - Only extract answer from top 1 docs mode
main_mode_2.py - Extract answers from top 5 docs mode
Summary_QA_Testing.py - Testing file for QA and summarizer in ideal conditions

# Richard Gubijev 
