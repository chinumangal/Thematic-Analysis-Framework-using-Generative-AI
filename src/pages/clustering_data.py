import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os, time, re
import google.generativeai as genai
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Create the model
generation_config = {
   "temperature": 1,
    "top_p": 0.3,
    "top_k": 40,
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
fieldname = '1.3 Data in the Domain'
columnname = 'Keywords_1.3 Data in the Domain'     #"Course_name"

def get_cluster_list():
    list = df[fieldname].tolist()
    
    prompt = f"""Go through the list of keywords for this column {list}. And make a list of repeting 8 data types present in this column. 
        Let the data-types be most generalized. 
        
        For eg. Image/Visual Data, Sensor/Time-Series Data 
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
    print(cluster_array)


cluster_list =  get_cluster_list() #['Image/Visual Data', 'Sensor/Time-Series Data', 'Structured/Tabular Data', 'Audio Data', 'Text/Document Data', 'Biological/Molecular Data', 'Market/Economic Data', 'Geospatial Data', '3D Model Data']    #['Engineering & Technology', 'Computer Science & Data', 'Natural Sciences', 'Medical & Health Sciences', 'Business & Economics', 'Social Sciences & Humanities', 'Design & Creative Arts', 'Applied Sciences & Vocational Fields']
# cluster_list = ', '.join(cluster_list)
clusters = []
def get_gemini_cluster(keywords):

        prompt = f"""
        You are a Classifier. Given domain keywords, classify them into one or more of the following clusters:
        {cluster_list}
        
        Only use these clusters in your response, separated by commas. Do not add any other text.

        Example:
        Input:    Types of Data:    Medical Images: X-rays, CT scans, MRIs, PET scans, ultrasounds (both 2D and 3D).    
                            Structured Data: Patient demographics, medical history, lab results, radiology reports, and clinical notes (often stored in PACS - Picture Archiving and Communication Systems).    
                            Image Metadata: Information associated with medical images, such as acquisition parameters, patient positioning, and imaging modality.    
                            Annotation Data: Radiologist's annotations on medical images, indicating areas of interest (e.g., tumor locations, fractures).    
                            Significance for AI Applications:    Medical images are the primary input for many AI algorithms used in radiology, allowing for the training of image recognition and analysis models.    
                            Structured data is essential for contextualizing medical images and building more robust diagnostic models.    
                            Image metadata ensures that AI models are trained on data with the correct parameters and can be generalized to different settings.    
                            Annotation data is critical for training supervised learning models, enabling AI to accurately identify and segment regions of interest in images.    
                            Understanding Data: Understanding the nuances of medical imaging modalities and data formats is crucial for selecting appropriate AI techniques and building effective models for radiological applications. 
        Output: Image/Visual Data, Structured/Tabular Data, Annotation Data	

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

df = df[['Serial number', 'Course name', 'Author',  'Date', 'Version', '1.3 Data in the Domain', 'Cluster_data_types'  ]]

output_data_path = os.path.join(local_dir, "view_data_types.csv")

df.to_csv(output_data_path,  index= False, sep=";")

