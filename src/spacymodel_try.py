import pandas as pd
import numpy as np
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
embedding_to_keyword_map = []

for i, text in enumerate(use_case):
    keyword = []
    clean_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    doc = nlp(clean_text)
    # print(doc)
    for token in doc:
        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            keyword.append(token.text)
            embeddings.append(nlp(token.text).vector)  # Append embeddings for each keyword
            embedding_to_keyword_map.append(i)
    
    keywords.append(keyword)
    
    
df['use_case_keywords'] = keywords


df.to_csv(output_data_path, index=False, sep=";")

# Convert embeddings to a NumPy array for KNN
embeddings_array = np.array(embeddings)

knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(embeddings_array)

# Generalized query functionality
def find_nearest_neighbors(query_theme):
    """
    Find the nearest neighbors for a given query theme.
    
    Args:
        query_theme (str): The theme or keyword to query.
        
    Returns:
        list: The nearest themes (keywords).
    """
    # Convert the query theme to an embedding
    query_embedding = nlp(query_theme).vector.reshape(1, -1)

    # Find the 5 nearest neighbors
    distances, indices = knn.kneighbors(query_embedding)

    # Map indices back to keywords
    nearest_neighbors = []
    for index in indices[0]:
        use_case_index = embedding_to_keyword_map[index]  # Find the corresponding use case
        nearest_neighbors.append(keywords[use_case_index])  # Retrieve the use case keywords

    return nearest_neighbors

if __name__ == "__main__":
    query_theme = input("Enter a query theme: ")  # Prompt the user for a query
    nearest_neighbors = find_nearest_neighbors(query_theme)
    
    print(f"\nQuery Theme: {query_theme}")
    print("\nNearest Themes:")
    for neighbor in nearest_neighbors:
        print(neighbor)

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


