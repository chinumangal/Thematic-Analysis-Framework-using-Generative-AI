import pandas as pd
import os, time, re
import google.generativeai as genai
import json
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if "GEMINI" in config and "api_key" in config["GEMINI"]:
    api_key = config["GEMINI"]["api_key"]
else:
    api_key = None

genai.configure(api_key=api_key)
# Create the model
generation_config = {
   "temperature": 0.4,
    "top_p": 0.3,
    "top_k": 10,
    "max_output_tokens": 192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )


local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")

df = pd.read_excel(course_data)
fieldname = '3.2 Assessment'
columnname = f'Keywords_{fieldname}'     #"Course_name"

categories = {"Individual Assignments", "Group Projects", "Quizzes", "Midterm Exam", "Final Exam/Presentation/Portfolio", "Class Participation"}

def rate_support(text):
    
    text = str(text).lower()
    
    prompt = f"""
        You are evaluating assessment descriptions for university courses.
        Please rate the following categories on a scale from 1 (very poor) to 5 (excellent),
        based only on the information provided below.
        

        Categories:
        - Individual Assignments
        - Group Projects
        - Quizzes
        - Midterm Exam
        - Final Exam/Presentation/Portfolio
        - Class Participation

        Return the result as a valid JSON object with category names as keys and integer scores as values. Do not include any explanation or additional text.

        Text:
        \"\"\"{text}\"\"\"
        """
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        response_text = response.text.strip()
        print(f"Raw Gemini response:\n{response_text}")
        time.sleep(5)
        # Clean up backticks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        # Try parsing as JSON
        ratings = json.loads(response_text)
        return ratings
    except Exception as e:
        print(f"Error processing Gemini response: {e}")
        return {cat: None for cat in categories}
    



# Store scores for each course
course_scores = []
for idx, row in df.iterrows():
    clusters = [c.strip() for c in row["Cluster"].split(";")]
    scores = rate_support(row[fieldname])
    for cluster in clusters:
        course_scores.append({
            "Cluster": cluster,
            **scores
        })

# Create DataFrame and aggregate by cluster
score_df = pd.DataFrame(course_scores)
cluster_avg = score_df.groupby("Cluster").mean().round(2)

# Display final result
print(cluster_avg)

cluster_avg = cluster_avg.reset_index()
output_data_path = os.path.join(local_dir, "view_assessment.csv")

cluster_avg.to_csv(output_data_path,  index= False, sep=";")
# Save to CSV
# cluster_avg.to_csv("cluster_internal_support_scores.csv", index=False)

# Optionally print to confirm
# print(cluster_avg.head())
