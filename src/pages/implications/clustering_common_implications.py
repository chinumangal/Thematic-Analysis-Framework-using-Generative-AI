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

def get_common_implications():
    prompt = f"""
    You are an experienced data analyst and AI expert. You work is to analyse data about domains {domains} and implications of using AI {implications} in that domain
    Your task is to find top 10 common implications of using AI and the three domains it affects the most.
    
    Example:
    Alogorithm Bias|Medical & Health Sciences, Business & Economics, Social Sciences & Humanities
    
    Provide output in below format only. 
    Common Implications1|Domains Most Affected
    Common Implications2|Domains Most Affected
    
    Don't include any other text.
     ...
        
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    common_immplications = response.text  
    #print(cluster_array)
    return common_immplications



# --- Main Execution ---
if __name__ == "__main__":
    common_implications_text = get_common_implications()
    
# Process common implications
    common_rows = [line.strip().split('|') for line in common_implications_text.strip().split('\n')]
    df_domain = pd.DataFrame(common_rows, columns=[
        "Common Implications",
        "Domains Most Affected"
    ]) 
    
    # Write to Excel with different sheets
    output_file = os.path.join(local_dir, "view_implications.xlsx")
    try:
        # Try to open the existing file and append
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay') as writer:
            df_domain.to_excel(writer, sheet_name="Common Implications", index=False)
        print(f"Data appended to sheet 'Common Implications' in '{output_file}'")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with pd.ExcelWriter(output_file, mode='w') as writer:
            df_domain.to_excel(writer, sheet_name="Common Implications", index=False)
        print(f"Data saved to new file '{output_file}' with sheet 'Common Implications'")