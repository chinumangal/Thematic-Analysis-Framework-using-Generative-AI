import os
import time
import pandas as pd
import numpy as np
import configparser
import google.generativeai as genai


config = configparser.ConfigParser()
config.read("config.ini")
api_key = config.get("GEMINI", "api_key", fallback=None)
genai.configure(api_key=api_key)

local_dir = os.path.abspath(os.path.join(__file__, "../../data/"))
keywords_data = os.path.join(local_dir, "keywords_output_data.csv")
embedding_data = os.path.join(local_dir, "output_embeddings.csv")
raw_data_path = os.path.join(local_dir, "Course_output_data.xlsx")

EMBED_MODEL = "models/text-embedding-004"

def generate_embedding(text):
    """Generate embedding from Gemini API for a given text."""
    result = genai.embed_content(model=EMBED_MODEL, content=text)
    return result["embedding"]

def load_data(input_data_path, output_data_path):
    df = pd.read_csv(input_data_path, sep=";")
    df_filtered = df[df["embeddings_processed"].str.strip().str.lower() == "no"].copy()
    if os.path.exists(output_data_path):
        try:
            df_existing = pd.read_csv(output_data_path, sep=";", encoding="utf-8")
        except UnicodeDecodeError:
            df_existing = pd.read_csv(output_data_path, sep=";", encoding="ISO-8859-1")
    else:
        df_existing = pd.DataFrame()
    return df, df_filtered, df_existing

def process_embeddings(df_filtered):
    fieldnames = [
        '1.1 Domain', '1.2 Potential AI Use Cases', '1.3 Data in the Domain',
        '1.4 Implications of Using AI', '1.5 Additional Learning Resources',
        '2.1 Learners and Their Interaction with AI', '2.2 Instructors', 
        '2.3 Internal Support', '3.1 Learning Outcomes', 
        '3.2 Assessment', '3.3 Learning Activities'
    ]

    df_embeddings = df_filtered[[
        'Serial number', 'Course name', 'Author', 'Date', 'Version'
        ]].copy()

    for field in fieldnames:
        col = f"Keywords_{field}"
        print(f"Processing embeddings for column: {col}")
        embeddings = []

        for text in df_filtered[col].fillna("").tolist():
            try:
                embedding = generate_embedding(text)
                embeddings.append(embedding)
                print(f"→ Embedded text: {text[:60]}...")  
            except Exception as e:
                print(f"❌ Error generating embedding: {e}")
                embeddings.append([None]*768)  
            time.sleep(5)

        df_embeddings[col] = df_filtered[col]
        df_embeddings[f"embeddings_{col}"] = embeddings
        time.sleep(6)

    return df_embeddings

def save_outputs(input_data, output_data, raw_data_path):
    df, df_filtered, df_existing = load_data(input_data, output_data)
    df_raw = pd.read_excel(raw_data_path)
    if df_filtered.empty:
        print("✅ All rows already processed for embeddings.")
        return

    print(f"🟡 Processing {len(df_filtered)} new rows for embeddings.")
    df_embeddings = process_embeddings(df_filtered)

    combined = pd.concat([df_existing, df_embeddings])
    combined.to_csv(output_data, sep=";", index=False)

    df.loc[df['Serial number'].isin(df_filtered['Serial number']), 'embeddings_processed'] = 'Yes'
    df.to_csv(keywords_data, index=False, sep=';')
    
    df_raw.loc[df_raw['Serial number'].isin(df_filtered['Serial number']), 'embeddings_processed'] = 'Yes'
    df_raw.to_excel(raw_data_path, index=False)
    
    print("✅ Embeddings and metadata saved.")
    

if __name__ == "__main__":
    save_outputs(keywords_data, embedding_data, raw_data_path)
