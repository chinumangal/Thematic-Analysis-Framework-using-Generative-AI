import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter

# Set page title and layout
st.set_page_config(page_title="Implications of Using AI", layout="wide")

st.title("📊 Implications of Using AI ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
implications_file = os.path.join(local_dir,"view_implications.xlsx")

df_common = pd.read_excel(implications_file, sheet_name="Common Implications")
df_domain = pd.read_excel(implications_file, sheet_name="Domain Implications")
df_course = pd.read_excel(implications_file, sheet_name="Course Implications")


tab1, tab2, tab3 = st.tabs(["Common Implications", "Domain wise","Course wise  "])

with tab1:
    st.subheader("Commom Implications across Domains")
    st.dataframe(df_common[["Common Implications", "Domains Most Affected"]], use_container_width=True)
    
with tab2:
    st.subheader("Different types of Implications")
    st.dataframe(df_domain[["Domain", "Ethical Implications", "Legal Implications", "Social Implications"]], use_container_width=True)
    
    st.subheader("Examples")
    st.dataframe(df_domain[["Domain", "Positive Examples", "Negative Examples"]], use_container_width=True)

with tab3:
    st.subheader("🎓 Course-wise Implications")
    course_options = df_course["Course_name"].unique().tolist()
    default_courses = course_options[:2]  # Pre-select first 2

    selected_courses = st.multiselect(
        "Search implications of using AI in a course",
        options=course_options,
        default=default_courses
    )

    filtered_df_course = df_course[df_course["Course_name"].isin(selected_courses)]
    
    st.subheader("Different types of Implications")
    st.dataframe(filtered_df_course[["Course_name", "Ethical Implications", "Legal Implications", "Social Implications"]], use_container_width=True)
    
    st.subheader("Examples")
    st.dataframe(filtered_df_course[["Course_name", "Positive Examples", "Negative Examples"]], use_container_width=True)


    