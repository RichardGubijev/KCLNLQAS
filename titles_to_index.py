from documents_retriever import load_data_as_dataframe

df = load_data_as_dataframe("prepared_data.json")
titles = df["title"]
texts = df["text"]

titles = [
"Housing and homelessness advice when university services are closed"
,"What financial support is there to help me through the cost of living crisis?"
,"Where can I find charity and not-for-profit accommodation?"
,"I am homeless or at risk of homelessness what should I do?"
,"What topics can Housing Advice support me with?"
,"What student support services are available at King's?"
    ]

index_list = []
for t in titles:
    index_value = df[df['title'] == t].index
    index_list.append(index_value[0])

print(f"{index_list}")