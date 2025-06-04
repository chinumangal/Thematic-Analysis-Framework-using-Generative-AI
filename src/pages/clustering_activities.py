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
fieldname = '3.3 Learning Activities'
# columnname = f'Keywords_{fieldname}'     #"Course_name"

categories = {"Problem-Centered", "Activation", "Demonstration", "Application", "Integration", "Teaching Methods"}

def rate_support(text):
    
    text = str(text).lower()
    
    prompt = f"""
        You are evaluating learning activities descriptions for university courses.
        Please rate the following categories on a scale from 1 (very poor) to 5 (excellent),
        based only on the information provided below.
        

        Categories:
        - Problem-Centered
        - Activation
        - Demonstration
        - Application
        - Integration
        - Teaching Methods

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

        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()


        ratings = json.loads(response_text)
        return ratings
    except Exception as e:
        print(f"Error processing Gemini response: {e}")
        return {cat: None for cat in categories}
    

course_scores = []
for idx, row in df.iterrows():
    clusters = [c.strip() for c in row["Cluster"].split(";")]
    scores = rate_support(row[fieldname])
    for cluster in clusters:
        course_scores.append({
            "Cluster": cluster,
            **scores
        })


score_df = pd.DataFrame(course_scores)
cluster_avg = score_df.groupby("Cluster").mean().round(2)


print(cluster_avg)

cluster_avg = cluster_avg.reset_index()
raw_output_data = os.path.join(local_dir, "cluster_activities.csv")
score_df.to_csv(raw_output_data,  index= False, sep=";")

output_data_path = os.path.join(local_dir, "views", "view_activities.csv")

cluster_avg.to_csv(output_data_path,  index= False, sep=";")

