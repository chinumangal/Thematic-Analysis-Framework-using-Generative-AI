import pandas as pd
import os
from save_embeddings import generate_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast


local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
embeddings_path = os.path.join(local_dir,"output_embeddings.csv")
course_output_data_path = os.path.join(local_dir, "Course_output_data.xlsx")

def find_nearest_neighbors(field_name, query_theme, top_n=10, threshold=0.0):
    # print(query_theme)
    query_embedding = generate_embedding(query_theme)
    
    df = pd.read_csv(embeddings_path, encoding='ISO-8859-1', sep=';')
    output_df = pd.read_excel(course_output_data_path, 'Sheet1')
    
    field_embeddings = f"embeddings_Keywords_{field_name}"
    keywords_field = f"Keywords_{field_name}"
    
    # Extract the embeddings for the selected field
    embeddings_list = df[field_embeddings].apply(ast.literal_eval).tolist()
    
    # Convert the embeddings list into a numpy array
    embeddings_matrix = np.array(embeddings_list)
    
    # Calculate cosine similarity between the query embedding and all the embeddings
    cosine_similarities = cosine_similarity([query_embedding], embeddings_matrix).flatten()
    
    # Get indices of the sorted similarities in descending order
    sorted_indices = np.argsort(cosine_similarities)[::-1]
 
    # Collect top N results or those above the threshold
    results = []
    for idx in sorted_indices[:5]:  # Get top 5 indices
        similarity = cosine_similarities[idx]
        serial_number = output_df.iloc[idx][df.columns[0]]  # Assuming 'Serial number' is the first column
        course_name = output_df.iloc[idx][df.columns[1]]
        keywords = output_df.iloc[idx][field_name]
        results.append({"Serial Number": serial_number, "Course name": course_name, "field": keywords, "Similarity": similarity})
    
    # Convert results to a DataFrame for a tabular format
    results_df = pd.DataFrame(results)
    return results_df      


if __name__ == '__main__':
    field = input("Enter the field: ")
    query_theme = input("Enter a query theme: ")  # Prompt the user for a query
    nearest_neighbors = find_nearest_neighbors(field, query_theme)
    
    print(nearest_neighbors)
    