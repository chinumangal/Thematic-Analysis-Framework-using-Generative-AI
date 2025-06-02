import pandas as pd
import matplotlib.pyplot as plt
import os, time
import google.generativeai as genai
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
import configparser


import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if "GEMINI" in config and "api_key" in config["GEMINI"]:
    api_key = config["GEMINI"]["api_key"]
else:
    api_key = None

genai.configure(api_key=api_key)

# Configure Gemini API
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.2,
    "top_p": 0.5,
    "top_k": 4,
    "max_output_tokens": 4000,
    "response_mime_type": "text/plain",
}

# --- File Setup ---
local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
course_data = os.path.join(local_dir, "Course_output_data.xlsx")
df = pd.read_excel(course_data)


domains = df['Cluster']
learners = df['2.1 Learners and Their Interaction with AI']
domain_list = ['Engineering & Technology', 'Computer Science & Data', 'Natural Sciences', 'Medical & Health Sciences', 'Business & Economics', 'Social Sciences & Humanities', 'Design & Creative Arts', 'Applied Sciences & Vocational Fields']


# --- Function to Extract Learners data ---
def get_learners():
    prompt = f"""
    You are an experienced data analyst and AI expert. You work is to analyse data about domains {domains} and, Learners and their interaction with AI {learners} in that domain.
    Provide percentage of the learners in different levels that are “Consumers,the General Public and Policymakers”, “Co-Workers and Users of AI Products”, “Collaborators and AI Implementers” and “Creators of AI”
    across different domains. The total for each doamin should sum up to 100.
    
    Example:
    Engineering & Technology|21.5|24.5|26.9|27.1
    
    Provide output for all the unique domains. Do not include any explanations and Strictly provide output in below format only. Don't miss any values.
    Domain1|Consumers,the General Public and Policymakers|Co-Workers and Users of AI Products|Collaborators and AI Implementers|Creators of AI
    Domain2|Consumers,the General Public and Policymakers|Co-Workers and Users of AI Products|Collaborators and AI Implementers|Creators of AI 
    
    Make sure all the domains from {domain_list} are included in the output. Don't include extra text or characters.
    ...
        
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    learners_cluster = response.text  
    #print(learners_cluster)
    return learners_cluster


# --- Main Execution ---
if __name__ == "__main__":
    learners_text = get_learners()
      

    # Process domain implications
    domain_rows = [line.strip().split('|') for line in learners_text.strip().split('\n')]
    df_learners = pd.DataFrame(domain_rows, columns=[
        "Domain",
        "Consumers,the General Public and Policymaker",
        "Co-Workers and Users of AI Product",
        "Collaborators and AI Implementers",
        "Creators of AI"
    ]) 
    
    # Write to Excel with different sheets
    output_file = os.path.join(local_dir, "view_learners.xlsx")
    try:
        # Try to open the existing file and append
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay') as writer:
            df_learners.to_excel(writer, sheet_name="Learners of AI", index=False)
        print(f"Data appended to sheet 'Learners of AI' in '{output_file}'")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with pd.ExcelWriter(output_file, mode='w') as writer:
            df_learners.to_excel(writer, sheet_name="Learners of AI", index=False)
        print(f"Data saved to new file '{output_file}' with sheet 'Learners of AI'")
        
