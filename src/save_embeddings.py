import google.generativeai as genai
import os, time
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if "GEMINI" in config and "api_key" in config["GEMINI"]:
    api_key = config["GEMINI"]["api_key"]
else:
    api_key = None

genai.configure(api_key=api_key)
print(api_key)

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

def save_embeddings(input_data_path, output_data_path):
    
    df = pd.DataFrame(input_data_path)
    # print(df.head())
    df_output = pd.DataFrame()
    df_output['Serial number'] = df['Serial number']
    df_output['Course name'] = df['Course name']
    df_output['Author'] = df['Author']
    df_output['Date'] = df['Date']
    df_output['Version'] = df['Version']
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
            print(f"text is {text}")
            embedding = generate_embedding(text)
            # print(embedding)
            embeddings.append(embedding)
            mappings.append({
                "Serial Number": df["Serial number"],
                'Course name' : df['Course name'],
                'Author' : df['Author'],
                'Date' : df['Date'],
                'Version': df['Version']
                # {fieldname}: row[columnname]
            })
            time.sleep(5)
        
        df_output[columnname] = df[columnname]
        df_output[f"embeddings_{columnname}"] = embeddings
        print(f"embeddings created for {columnname}")
        time.sleep(300)
    
    df_output.to_csv(output_data_path, index= False, sep=";" )
    
    # save_embeddings_to_csv(embeddings, mappings, "domain_embeddings.csv")
    
    print("done")
    



if __name__ == "__main__":
    # Mock example embeddings and mappings (replace these with your actual data)
    local_dir = os.path.abspath(os.path.join(__file__, "../../data/"))
    keywords_data = os.path.join(local_dir, "keywords_output_data.csv")
    output_data_path = os.path.join(local_dir, "output_embeddings.csv")
    input_data = pd.read_csv(keywords_data, delimiter=";", encoding="ISO-8859-1")
    
    save_embeddings(input_data, output_data_path)