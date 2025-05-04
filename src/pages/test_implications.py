import pandas as pd
import matplotlib.pyplot as plt
import os, time
import google.generativeai as genai
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
import configparser


# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY_2"])

generation_config = {
    "temperature": 0.2,
    "top_p": 0.5,
    "top_k": 4,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# --- File Setup ---
local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
course_data = os.path.join(local_dir, "Course_output_data.xlsx")
df_original = pd.read_excel(course_data)

courses = df_original['Course_name']
implications = df_original['1.4 Implications of Using AI']
implications_cluster = []

def get_course_implications():
    prompt = f"""
        You are an experienced data analyst and AI expert. You work is to analyse data about courses {courses} and implications of using AI {implications} in that courses.
    Provide the most common ethical implications, legal implications, social implications, positive examples and negative examples in that course limiting to minimum 1 value and maximum 3 values for each of them.
    
    Example:
    Radiology|Data Privacy, Algorithmic Bias, Transparency|Regulatory Compliance, Liability, Data Usage|Changes in Radiologist Roles, Accessibility, Patient Trust|Earlier & Accurate Diagnosis, Reduced Radiation|Job Displacement, Over-Reliance, Misdiagnosis
    
	Do not include any explanations and Striclty provide output in below format only:
    Course1|Ethical Implications|Legal Implications|Social Implications|Positive Examples|Negative Examples
    Course2|Ethical Implications|Legal Implications|Social Implications|Positive Examples|Negative Examples
    ...
    
    Don't miss any course.
    
     
	"""
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    implications_cluster = response.text
    print(implications_cluster)
    return implications_cluster

    
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
    

        
    merged_df = pd.merge(
        df_original[['Serial number', 'Course_name', 'Author',  'Date', 'Version', 'Cluster']],
        df_course,
        on='Course_name',
        how='left'  # Include all courses from df_original DataFrame
    )

    # Replace NaN with None (optional, if None is required)
    merged_df = merged_df.where(merged_df.notna(), None)
    
    # Write to Excel with different sheets
    output_file = os.path.join(local_dir, "view_implications.xlsx")
    with pd.ExcelWriter(output_file) as writer:
        df_course.to_excel(writer, sheet_name="Course Implications", index=False)
    print("Implications data Saved")

    try:
        # Try to open the existing file and append
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay') as writer:
            merged_df.to_excel(writer, sheet_name="Course Implications", index=False)
        print(f"Data appended to sheet 'Course Implications' in '{output_file}'")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with pd.ExcelWriter(output_file, mode='w') as writer:
            merged_df.to_excel(writer, sheet_name="Course Implications", index=False)
        print(f"Data saved to new file '{output_file}' with sheet 'Course Implications'")