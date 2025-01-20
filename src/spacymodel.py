import pandas as pd
import os, re
import spacy
from sklearn.neighbors import NearestNeighbors

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
raw_data_path = os.path.join(local_dir,"raw_data.csv")
output_data_path = os.path.join(local_dir, "output_data.csv")

df= pd.read_csv(raw_data_path, encoding='ISO-8859-1', sep=';')


domain = df['Domain'].tolist()
use_case = df['Potential use cases'].tolist()

nlp = spacy.load("en_core_web_sm")

keywords = []
embeddings = []

for text in use_case:
    keyword = []
    clean_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    doc = nlp(clean_text)
    # print(doc)
    for token in doc:
        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            keyword.append(token.text)

            # print(token.text, token.pos_, token.dep_)
    embeddings.extend( [nlp(key).vector for key in keyword])
    
    keywords.append(keyword)
    
    
df['use_case_keywords'] = keywords


df.to_csv(output_data_path, index=False, sep=";")


# knn = NearestNeighbors(n_neighbors=5, metric='cosine')

# # Fit the model with embeddings
# knn.fit(embeddings)

# # Example query theme
# query_theme = "Medical"

# # Convert the query theme to an embedding
# query_embedding = nlp(query_theme).vector.reshape(1, -1)

# # Find the 5 nearest neighbors
# distances, indices = knn.kneighbors(query_embedding)

# # Print the query theme and nearest neighbors
# print("Query Theme:", query_theme)
# print("\nNearest Themes:")

# print(len(keywords), len(embeddings))

# print(indices[0])
# for index in indices[0]:
#     print(keywords[index])


