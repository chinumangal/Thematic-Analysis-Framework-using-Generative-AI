import streamlit as st
import pandas as pd
import numpy as np
import os
from search_embedding import find_nearest_neighbors

st.title('Data analysis on Educational data')

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")
# @st.cache_data
def load_data(file_path, nrows):
    data = pd.read_excel(file_path, nrows=nrows)
    return data

def print_data(text):
    st.text( text)

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(course_data, 10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Loading Done!")

fieldname = st.selectbox(
                'Select the field name',
                    ('1.1 Domain', '1.2 Potential AI Use Cases','1.3 Data in the Domain',
                        '1.4 Implications of Using AI', '1.5 Additional Learning Resources',
                        '2.1 Learners and Their Interaction with AI','2.2 Instructors', 
                        '2.3 Internal Support', '3.1 Learning Outcomes', 
                        '3.2 Assessment','3.3 Learning Activities'))

query_text = st.text_input(label="Enter your text here")

# Corrected code using a lambda function
if st.button(label="Search similar frameworks"):
    output_data = find_nearest_neighbors(fieldname, query_text)
    st.subheader('AI Course design framework')
    st.write(output_data)


