import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os, time, re
import google.generativeai as genai
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA

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


local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")
keyword_data = os.path.join(local_dir,"keywords_output_data.csv")
# Load data into DataFrame
# df = pd.read_csv(keyword_data, sep=";", encoding="ISO-8859-1")
df = pd.read_excel(course_data)
# df = pd.read_csv(course_data, sep=";")
fieldname = '1.5 Additional Learning Resources'
columnname = f'Keywords_{fieldname}'     #"Course_name"

def get_cluster_list():
    list = df[fieldname].tolist()
    
    prompt = f"""Go through the list of keywords for this column {list}. And make a list of repeting 8 resource types present in this column. 
        Let the data-types be most generalized. 
        
        For eg. Textbook, online courses, etc. 
        Just give me cluster names as a list in the output, I dont want any additional text. 
        """
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    
    response_clean = (response.text).replace("\n", " ").replace("[]", " ").strip()
    # response_cleaned = re.sub(r"[\[\] \"\' \* ]", "", response_clean )
    cluster_array = response_clean.split(',')
    # print(cluster_array)
    return cluster_array


cluster_list =  get_cluster_list() #['Image/Visual Data', 'Sensor/Time-Series Data', 'Structured/Tabular Data', 'Audio Data', 'Text/Document Data', 'Biological/Molecular Data', 'Market/Economic Data', 'Geospatial Data', '3D Model Data']    #['Engineering & Technology', 'Computer Science & Data', 'Natural Sciences', 'Medical & Health Sciences', 'Business & Economics', 'Social Sciences & Humanities', 'Design & Creative Arts', 'Applied Sciences & Vocational Fields']
cluster_list.append("Others")
print(cluster_list)
clusters = []
def get_gemini_cluster(keywords):

        prompt = f"""
        You are a Classifier. Given domain keywords, classify them into one or more of the following clusters:
        {cluster_list}
        
        Only use these clusters in your response, separated by commas. Do not add any other text.

        Example:
        Input:       Online Courses:    Coursera: "AI for Astronomy" (Hypothetical, but similar courses may exist).    edX: "Introduction to Data Science in Python."    Webinars:    Astronomy AI Webinar Series by various institutions (e.g., Space Telescope Science Institute).    Webinars by NASA, ESA, and other space agencies focused on using AI in astronomy.    Open Educational Resources (OER):    The Astropy Project Documentation (Python library for astronomy).    NASA Open Data Portal and Archives.    Data repositories like the Sloan Digital Sky Survey (SDSS).    Textbooks:    "Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control" by Steven L. Brunton and J. Nathan Kutz.    "Astronomy Methods" by Hale Bradt (for astronomical background).    Research Articles:    Papers published in journals like The Astrophysical Journal, Astronomy & Astrophysics, and Monthly Notices of the Royal Astronomical Society.  
        Output: Online courses, webinars, Textbooks, etc. 

        Now classify the following:
        Input: {keywords}
        Output:
        
        """
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )
        try: 
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            response_clean = (response.text).replace("\n", " ").replace("[]", " ").strip()
            cluster_array = response_clean.split(',')
            print(cluster_array)
            return cluster_array
        except Exception as e:
            print(f"Error while getting clusters from Gemini: {e}")
            time.sleep(60)
            return ['None']
    # return clusters
    
    # print(df.head)

def get_gemini_cluster_with_retries(keywords, retries=3):
    for attempt in range(retries):
        cluster_array = get_gemini_cluster(keywords)
        if cluster_array and cluster_array != ['None']:
            return cluster_array
        print(f"Retry {attempt+1}")
        time.sleep(60)  # be kind to the API
    return ["Unclassified"]  # fallback

for keywords in df[fieldname].tolist():
    # print(f"keywords are {keywords} ")
    cluster_array = get_gemini_cluster_with_retries(keywords)
    clusters.append('; '.join(map(str.strip, cluster_array)))
    time.sleep(5)

# Generate labels for each domain
df['Cluster_data_types'] =  clusters

df = df[['Serial number', 'Course name', 'Author',  'Date', 'Version', fieldname, 'Cluster_resources'  ]]

output_data_path = os.path.join(local_dir, "view_resources.csv")

df.to_csv(output_data_path,  index= False, sep=";")

