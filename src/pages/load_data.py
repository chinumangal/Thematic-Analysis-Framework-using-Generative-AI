import streamlit as st
import os
import zipfile
import tempfile
import pandas as pd
from dataloader import dataloader
from keyword_extraction import get_keywords
from save_embeddings import save_embeddings
# from ..dataloader import dataloader

st.title("🗂️ Upload and Process a ZIP Folder")

# Upload .zip file
uploaded_zip = st.file_uploader("Upload a ZIP file", type="zip")

# Target folder to extract ZIP contents
local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
EXTRACT_FOLDER = "../data/uploads/unzipped_files"
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

if uploaded_zip is not None:
    zip_path = os.path.join(EXTRACT_FOLDER, uploaded_zip.name)

    # Save uploaded zip file temporarily
    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.getbuffer())

    # Extract contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)

    st.success("✅ ZIP file extracted successfully!")

    # List files
    extracted_files = [f for f in os.listdir(EXTRACT_FOLDER) if f.endswith((".csv", ".txt", ".json"))]
    st.write("📂 Extracted Files:")
    st.write(extracted_files)

    os.remove(zip_path)


st.title("Save data in an excel file:")

course_data_file = os.path.join(local_dir, "Course_output_data10.xlsx")
keyword_data_file = os.path.join(local_dir, "keywords_output_data10.csv")
embeddings_data_file = os.path.join(local_dir, "output_embeddings10.csv")

if st.button(label = "Save to Excel file", key="Save_to_Excel"):
    try:
        dataloader(EXTRACT_FOLDER, course_data_file)
    except Exception as e:
        st.write(e)

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if "GEMINI" in config and "api_key" in config["GEMINI"]:
    st.title("Process data ")

if st.button(label = "Get keywords", key="generate_keyword"):
    try:
        output = get_keywords(course_data_file, keyword_data_file)
    except Exception as e:
        st.write(e)
        
if st.button(label = "Generate embeddings", key="generate_embeddings"):
    try:
        embeddings  = save_embeddings(keyword_data_file, embeddings_data_file)
    except Exception as e:
        st.write(e)

