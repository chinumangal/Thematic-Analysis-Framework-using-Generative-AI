import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os, time
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

generation_config = {
   "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 192,
    "response_mime_type": "text/plain",
}

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")

df = pd.read_excel(course_data)

fieldname = '1.1 Domain'
columnname = "Course_name"
domain_list = ['Engineering & Technology', 'Computer Science & Data', 'Natural Sciences', 'Medical & Health Sciences', 'Business & Economics', 'Social Sciences & Humanities', 'Design & Creative Arts', 'Applied Sciences & Vocational Fields']

domain_name = []
def get_gemini_cluster():
    for course in df[columnname].tolist():
        
        prompt = f"""
        I want you to classify the given course name in a domain list provided. 
        A course can be classified into 2 domains at maximum. Do not classify a course into more than 2 domains.  
        In the output please mention only domain from the domain_list, separated by comma, no other text is required.
        Example:
            Input: Radiology
            Domain list =[Medical & Health Sciences, Natural Sciences]
            
        Your turn:
        Based on  following course description: {course}, classify the course into a the {domain_list}. Only use the clusters from the {domain_list}, do not use any other titles. 
        """
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        response_clean = (response.text).replace("\n", " ").replace("[]", " ").strip()
        domain_array = response_clean.split(',')
        print(domain_array)
        domain_name.append('; '.join(map(str.strip, domain_array)))
        time.sleep(5)

    df['Cluster'] =  domain_name

clusters = get_gemini_cluster()

output_data_path = os.path.join(local_dir, "views", "view_domain_clusters.csv")

df.to_csv(output_data_path,  index= False, sep=";")

