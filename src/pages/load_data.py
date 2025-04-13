import streamlit as st
import os
import zipfile
import tempfile
import pandas as pd
from dataloader import dataloader
# from ..dataloader import dataloader

st.title("🗂️ Upload and Process a ZIP Folder")

# Upload .zip file
uploaded_zip = st.file_uploader("Upload a ZIP file", type="zip")

# Target folder to extract ZIP contents
# local_dir = os.path.abspath(os.path.join(__file__, "../../data/"))
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

    # Optional: Preview one of the CSV files
    # for file in extracted_files:
    #     if file.endswith(".csv"):
    #         df = pd.read_csv(os.path.join(EXTRACT_FOLDER, file))
    #         st.write(f"📄 Preview: `{file}`")
    #         st.dataframe(df.head())

st.title("Save data in an excel file:")

course_output_file = os.path.join(EXTRACT_FOLDER, "Course_output_data.xlsx")
    

if st.button(label = "Save to Excel file", key="Save_to_Excel"):
    for course_file in os.listdir(EXTRACT_FOLDER):
        output = dataloader(course_file, course_output_file)


import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if "GEMINI" in config and "api_key" in config["GEMINI"]:
    st.title("Process data ")

    