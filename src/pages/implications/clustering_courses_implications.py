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
    "max_output_tokens": 3000,
    "response_mime_type": "text/plain",
}

# --- File Setup ---
local_dir = os.path.abspath(os.path.join(__file__, "../../../../data/"))
course_data = os.path.join(local_dir, "Course_output_data.xlsx")
df_original = pd.read_excel(course_data)

courses = df_original['Course_name']
implications = df_original['1.4 Implications of Using AI']
implications_cluster = []

def chunk_dataframe(df_original, chunk_size):
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i + chunk_size]
        
def get_course_implications(chunk_size=10):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    all_responses = []

    for start in range(0, len(courses), chunk_size):
        end = start + chunk_size
        course_chunk = courses[start:end]
        implication_chunk = implications[start:end]

        prompt = f"""
        You are an experienced data analyst and AI expert. Your job is to analyse data about courses {list(course_chunk)} and implications of using AI {list(implication_chunk)} in those courses.
        Provide the most common ethical implications, legal implications, social implications, positive examples and negative examples in that course limiting to minimum 1 value and maximum 3 values for each of them.

        Example:
        Radiology|Data Privacy, Algorithmic Bias, Transparency|Regulatory Compliance, Liability, Data Usage|Changes in Radiologist Roles, Accessibility, Patient Trust|Earlier & Accurate Diagnosis, Reduced Radiation|Job Displacement, Over-Reliance, Misdiagnosis

        Do not include any explanations and strictly provide output in below format only:
        Course1|Ethical Implications|Legal Implications|Social Implications|Positive Examples|Negative Examples
        Course2|Ethical Implications|Legal Implications|Social Implications|Positive Examples|Negative Examples
        ...
        Don't miss any course.
        """

        try:
            response = chat_session.send_message(prompt)
            all_responses.append(response.text.strip())
            time.sleep(15)  # Avoid rate limiting
        except Exception as e:
            print(f"Error processing chunk {start}-{end}: {e}")

    full_response = "\n".join(all_responses)
    return full_response


    

    
# --- Main Execution ---
if __name__ == "__main__":
    
    implications_cluster = get_course_implications()
        
    # Process course implications
    course_rows = [line.strip().split('|') for line in implications_cluster.strip().split('\n')]
    df_course = pd.DataFrame(course_rows, columns=[
        "Course_name",
        "Ethical Implications",
        "Legal Implications",
        "Social Implications",
        "Positive Examples",
        "Negative Examples"
    ])
    
    print(df_course)
    
    # Write to Excel with different sheets
    output_file = os.path.join(local_dir, "view_implications.xlsx")
    try:
        # Try to open the existing file and append
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay') as writer:
            df_course.to_excel(writer, sheet_name="Course Implications", index=False)
        print(f"Data appended to sheet 'Course Implications' in '{output_file}'")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with pd.ExcelWriter(output_file, mode='w') as writer:
            df_course.to_excel(writer, sheet_name="Course Implications", index=False)
        print(f"Data saved to new file '{output_file}' with sheet 'Course Implications'")