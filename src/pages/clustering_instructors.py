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
instructors = df['2.2 Instructors']
domain_list = ['Engineering & Technology', 'Computer Science & Data', 'Natural Sciences', 'Medical & Health Sciences', 'Business & Economics', 'Social Sciences & Humanities', 'Design & Creative Arts', 'Applied Sciences & Vocational Fields']


# --- Function to Extract Learners data ---
def get_instructors():
    prompt = f"""
    You are an experienced data analyst and AI expert. You work is to analyse data about domains {domains} and, Instructors {instructors} in that domain.
     instructors play an important role in the learning process [53].
    Domain-specific AI teaching requires a mix of sufficient AI knowledge, domain expertise and pedagogical skills to teach an 
    interdisciplinary course as well as the motivation and time from an instructor’s perspective. The AI knowledge of faculty 
    and instructors tends to be quite heterogeneous, ranging from no previous AI experience to decades of AI research experience. 
    Thus, provide percentage of the instructors at different levels that are "Emerging AI Instructor","Competent Interdisciplinary 
    Instructo","Experienced AI Instructor","Expert AI-Domain Educator" across different domains.  The distribution should be such 
    that it helps the learner to understand, apply the course.
    
    Example:
    Cybersecurity|10|20|40|30

    
    Provide output for all the unique domains. Do not include any explanations and Strictly provide output in below format only. Don't miss any values.
    Domain1|Emerging AI Instructor|Competent Interdisciplinary Instructor|Experienced AI Instructor|Expert AI-Domain Educator
    Domain2|Emerging AI Instructor|Competent Interdisciplinary Instructor|Experienced AI Instructor|Expert AI-Domain Educator
    
    Make sure all the domains from {domain_list} are included in the output. Don't include extra text or characters.
    
        
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    instructors_cluster = response.text  
    #print(instructors_cluster)
    return instructors_cluster


# --- Main Execution ---
if __name__ == "__main__":
    instructors_text = get_instructors()
      

    # Process domain implications
    domain_rows = [line.strip().split('|') for line in instructors_text.strip().split('\n')]
    df_learners = pd.DataFrame(domain_rows, columns=[
        "Domain",
        "Emerging AI Instructor",
        "Competent Interdisciplinary Instructor",
        "Experienced AI Instructor",
        "Expert AI-Domain Educator"
    ]) 
    
    # Write to Excel with different sheets
    output_file = os.path.join(local_dir, "view_instructors.xlsx")
    try:
        # Try to open the existing file and append
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay') as writer:
            df_learners.to_excel(writer, sheet_name="Instructors", index=False)
        print(f"Data appended to sheet 'Instructors' in '{output_file}'")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with pd.ExcelWriter(output_file, mode='w') as writer:
            df_learners.to_excel(writer, sheet_name="Instructors", index=False)
        print(f"Data saved to new file '{output_file}' with sheet 'Learners of AI'")
        
