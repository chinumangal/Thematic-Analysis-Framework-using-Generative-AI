import pandas as pd
import os
import re
import spacy
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# File path to the Excel file
excel_file_path = "E:/OVGU/AI_Thematic_analysis/data/new_output_data.xlsx"

# Load data from the single sheet named "Sheet 1"
df = pd.read_excel(excel_file_path, sheet_name="Sheet 1")

# Verify column names
print("Column names in the dataset:", df.columns)

# Define column names
serial_number_column = "Serial number"
domain_column = "1.1 Domain"
use_case_column = "1.2 Potential AI Use Cases"


# Initialize storage for embeddings and mappings
embeddings = []
serial_number_mapping = []
domain_mapping = []
use_case_mapping = []

# Process the domain and potential use case fields
for i, row in df.iterrows():
    domain_text = str(row[domain_column])
    use_case_text = str(row[use_case_column])

    # Clean and combine domain and use case text
    combined_text = re.sub(r"[^a-zA-Z0-9\s.,!?]", "", domain_text + " " + use_case_text)
    doc = nlp(combined_text)

    # Generate embedding for the combined text
    embeddings.append(doc.vector)

    # Store mappings for later use
    serial_number_mapping.append(row[serial_number_column])
    domain_mapping.append(domain_text)
    use_case_mapping.append(use_case_text)

# Convert embeddings to a NumPy array for KNN
embeddings_array = np.array(embeddings)

# Initialize and fit the KNN model
knn = NearestNeighbors(n_neighbors=5, metric="cosine")
knn.fit(embeddings_array)

# Function to find nearest serial numbers, domains, and use cases
def find_nearest_info(query_theme, threshold=0.5):
    """
    Find the nearest serial numbers, domains, and use cases for a given query theme using embeddings and KNN.

    Args:
        query_theme (str): The theme or keyword to query.
        threshold (float): Maximum allowed distance for considering a result relevant (default 0.5).

    Returns:
        list: A list of dictionaries containing the nearest serial numbers, domains, and use cases.
    """
    # Convert the query theme to an embedding
    query_embedding = nlp(query_theme).vector.reshape(1, -1)

    # Find the 5 nearest neighbors
    distances, indices = knn.kneighbors(query_embedding)

    # Collect the results
    results = []
    for idx, distance in zip(indices[0], distances[0]):
        if distance <= threshold:  # Include only results within the threshold distance
            results.append(
                {
                    "Serial Number": serial_number_mapping[idx],
                    "Domain": domain_mapping[idx],
                    "Use Case": use_case_mapping[idx],
                    "Distance": distance,  # Include distance for debugging
                }
            )

    return results

# Main program: Query for a theme and display results
if __name__ == "__main__":
    query_theme = input("Enter a query theme: ")  
    nearest_info = find_nearest_info(query_theme, threshold=1.0) 

    print(f"\nQuery Theme: {query_theme}")
    print("\nNearest Matches:")
    if nearest_info:
        for info in nearest_info:
            print(
                f"Serial Number: {info['Serial Number']}, Domain: {info['Domain']}, Use Case: {info['Use Case']}, Distance: {info['Distance']:.4f}"
            )
    else:
        print("No relevant matches found.")