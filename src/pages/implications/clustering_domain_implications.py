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
local_dir = os.path.abspath(os.path.join(__file__, "../../../../data/"))
course_data = os.path.join(local_dir, "Course_output_data.xlsx")
df = pd.read_excel(course_data)


domains = df['Cluster']
implications = df['1.4 Implications of Using AI']
domain_list = ['Engineering & Technology', 'Computer Science & Data', 'Natural Sciences', 'Medical & Health Sciences', 'Business & Economics', 'Social Sciences & Humanities', 'Design & Creative Arts', 'Applied Sciences & Vocational Fields']


# --- Function to Extract Structured Implications ---
def get_domain_implications():
    prompt = f"""
    You are an experienced data analyst and AI expert. You work is to analyse data about domains {domains} and implications of using AI {implications} in that domain.
    Provide the most common ethical implications, legal implications, social implications, positive examples and negative examples across the domains limiting to minimum 1 and maximum 3 values for each of them. Strictly follow this.
    
    
    Example:
    Engineering & Technology|Algorithmic Bias, Data Privacy, Transparency, Autonomy, Safety|Liability, Regulations, Data Protection, Intellectual Property, Standards|Job Displacement, Retraining, Efficiency, System Reliability, Human-Robot Interaction|Improved Efficiency, Safety, Design, Automation|Job Losses, System Failures, Misuse, Biased Decisions
    
    Provide output for all the unique domains. Do not include any explanations and Striclty provide output in below format only. Don't miss any values.
    Domain|Ethical Implications|Legal Implications|Social Implications|Positive Examples|Negative Examples
    Domain2|Ethical Implications|Legal Implications|Social Implications|Positive Examples|Negative Examples 
    
    Make sure all the domains from {domain_list} are included in the output. 
    ...
        
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    cluster_array = response.text  
    #print(cluster_array)
    return cluster_array


# --- Main Execution ---
if __name__ == "__main__":
    domain_implications_text = get_domain_implications()
      

    # Process domain implications
    domain_rows = [line.strip().split('|') for line in domain_implications_text.strip().split('\n')]
    df_domain = pd.DataFrame(domain_rows, columns=[
        "Domain",
        "Ethical Implications",
        "Legal Implications",
        "Social Implications",
        "Positive Examples",
        "Negative Examples"
    ]) 
    
    # Write to Excel with different sheets
    output_file = os.path.join(local_dir, "view_implications.xlsx")
    try:
        # Try to open the existing file and append
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay') as writer:
            df_domain.to_excel(writer, sheet_name="Domain Implications", index=False)
        print(f"Data appended to sheet 'Domain Implications' in '{output_file}'")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with pd.ExcelWriter(output_file, mode='w') as writer:
            df_domain.to_excel(writer, sheet_name="Domain Implications", index=False)
        print(f"Data saved to new file '{output_file}' with sheet 'Domain Implications'")
        
