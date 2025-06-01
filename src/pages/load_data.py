import streamlit as st
import os
import zipfile
import tempfile
import pandas as pd
from dataloader import dataloader
from keyword_extraction import get_keywords
from save_embeddings import save_outputs
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


st.title("🗂️ Upload and Process a ZIP Folder")

# Upload .zip file
uploaded_zip = st.file_uploader("Upload a ZIP file", type="zip")

# Target folder to extract ZIP contents
local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
EXTRACT_FOLDER = os.path.join(local_dir, "uploads/unzipped_files")
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

course_data_file = os.path.join(local_dir, "Course_output_data.xlsx")
keyword_data_file = os.path.join(local_dir, "keywords_output_data.csv")
embeddings_data_file = os.path.join(local_dir, "output_embeddings.csv")


if st.button(label="Save and Process Data", key="save_and_process"):
    try:
        # Step 1: Save raw data to Excel
        st.write("Saving course data...")
        
        df_new = dataloader(EXTRACT_FOLDER, course_data_file)
        st.success("New data saved in Course_output_data.xlsx.")
        # st.dataframe(df_new)

        # Step 2: Extract keywords
        st.write("Extracting keywords...")
        keyword_output = get_keywords(course_data_file, keyword_data_file)
        st.success("Keywords extracted to keywords_output_data.csv.")
        # st.dataframe(keyword_output)

        # Step 3: Generate embeddings
        st.write("Generating embeddings... (this may take a while ⏳)")
        embeddings = save_outputs(keyword_data_file, embeddings_data_file, course_data_file)
        st.success("Embeddings generated and saved in output_embeddings.csv.")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")

# df_new = pd.DataFrame()
# if st.button(label = "Save to Excel file", key="Save_to_Excel"):
#     try:
#         df_new = dataloader(EXTRACT_FOLDER, course_data_file)
        
#     except Exception as e:
#         st.write(e)

# if not df_new.empty:
#     st.dataframe(df_new)

# if "GEMINI" in config and "api_key" in config["GEMINI"]:
#     st.title("Process data ")

# keyword_output = pd.DataFrame()
# if st.button(label = "Get keywords", key="generate_keyword"):
#     try:
#         keyword_output = get_keywords(course_data_file, keyword_data_file)
#     except Exception as e:
#         st.write(e)
# if not keyword_output.empty:
#     st.dataframe(keyword_output)     


# if st.button(label = "Generate embeddings", key="generate_embeddings"):
#     try:
#         embeddings  = save_outputs(keyword_data_file, embeddings_data_file, course_data_file)
#     except Exception as e:
#         st.write(e)

