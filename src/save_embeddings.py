import google.generativeai as genai
import os, time
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

# client = genai.Client(api_key="GEMINI_API_KEY")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def save_embeddings_to_csv(embeddings, mappings, file_path):
    """
    Save embeddings and their mappings to a CSV file.

    Args:
        embeddings (list): List of embeddings (vectors).
        mappings (list): List of dictionaries with mappings (e.g., serial numbers, domains).
        file_path (str): File path to save the data.
    """
    data = []
    for idx, embedding in enumerate(embeddings):
        data.append({
            "Serial Number": mappings[idx]["Serial Number"],
            # "Domain": mappings[idx]["Domain"],
            "Embedding": ','.join(map(str, embedding))  # Convert embedding to a string
        })
        
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, sep=";")
    print(f"Embeddings saved to {file_path}")


def generate_embedding(text):
    """
    Use Gemini to generate a contextualized text representation.
    """
    result = genai.embed_content(
            model="models/text-embedding-004",
            content=text)

    # print(result["embedding"])
    return result["embedding"]


if __name__ == "__main__":
    # Mock example embeddings and mappings (replace these with your actual data)
    local_dir = os.path.abspath(os.path.join(__file__, "../../data/"))
    keywords_data = os.path.join(local_dir, "keywords_output_data.csv")
    output_data_path = os.path.join(local_dir, "output_embeddings.csv")
    input_data = pd.read_csv(keywords_data, delimiter=";")
    
    df = pd.DataFrame(input_data)
    # print(df.head())
    df_output = pd.DataFrame()
    df_output['Serial number'] = df['Serial number']
    # Ensure the Excel file has the necessary columns (adjust column names if needed)
    
    mappings = []
    fieldnames = ['1.1 Domain', '1.2 Potential AI Use Cases','1.3 Data in the Domain',
                        '1.4 Implications of Using AI', '1.5 Additional Learning Resources',
                        '2.1 Learners and Their Interaction with AI','2.2 Instructors', 
                        '2.3 Internal Support', '3.1 Learning Outcomes', 
                        '3.2 Assessment','3.3 Learning Activities'] 

        
    for fieldname in fieldnames:
        columnname = f"Keywords_{fieldname}"
        print(f"column is {columnname}")
        embeddings = []
        # for index, row in input_data.iterrows():
        for text in df[columnname].tolist():
            # text = row[{columnname}]  # Keywords_1.1 Domain Adjust according to your Excel column
            # print(text)
            embedding = generate_embedding(text)
            # print(embedding)
            embeddings.append(embedding)
            mappings.append({
                "Serial Number": df["Serial number"],
                # {fieldname}: row[columnname]
            })
            time.sleep(5)
        
        df_output[columnname] = df[columnname]
        df_output[f"embeddings_{columnname}"] = embeddings
        time.sleep(300)
    
    df_output.to_csv(output_data_path, index= False, sep=";" )
    
    # save_embeddings_to_csv(embeddings, mappings, "domain_embeddings.csv")
    
    print("done")
    

