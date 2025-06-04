import pandas as pd
import os
from save_embeddings import generate_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast


local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
embeddings_path = os.path.join(local_dir,"output_embeddings.csv")
course_output_data_path = os.path.join(local_dir, "Course_output_data.xlsx")

def safe_literal_eval(val):
    if pd.isna(val):
        return None
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return None
    
def find_nearest_neighbors(field_name, query_theme, top_n=10, threshold=0.0):
    query_embedding = generate_embedding(query_theme)
    
    df = pd.read_csv(embeddings_path, encoding='utf-8-sig', sep=';')
    output_df = pd.read_excel(course_output_data_path)
    
    field_embeddings = f"embeddings_Keywords_{field_name}"
    keywords_field = f"Keywords_{field_name}"

    embeddings_list = (
        df[field_embeddings]
        .apply(safe_literal_eval) 
        .dropna()                 
        .tolist()
    )
    
    embeddings_matrix = np.array(embeddings_list)

    cosine_similarities = cosine_similarity([query_embedding], embeddings_matrix).flatten()

    sorted_indices = np.argsort(cosine_similarities)[::-1]

    results = []
    for idx in sorted_indices[:5]:  
        similarity = cosine_similarities[idx]
        serial_number = output_df.iloc[idx][df.columns[0]] 
        course_name = output_df.iloc[idx][df.columns[1]]
        keywords = output_df.iloc[idx][field_name]
        results.append({"Serial Number": serial_number, "Course name": course_name, "field": keywords, "Similarity": similarity})
    
    results_df = pd.DataFrame(results)
    return results_df      


if __name__ == '__main__':
    field = input("Enter the field: ")
    query_theme = input("Enter a query theme: ")  
    nearest_neighbors = find_nearest_neighbors(field, query_theme)
    
    print(nearest_neighbors)
    