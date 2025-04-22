import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter
from search_embedding import find_nearest_neighbors

st.title("Implications of Using AI ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")
impl_data = os.path.join(local_dir,"AI_Implications_Domains.csv")


if impl_data is not None:
    df = pd.read_csv(impl_data, sep=";", encoding="ISO-8859-1")
    tab1, tab2, tab3 = st.tabs(["Implications and affected Domains","Types", "Impact of AI  in domains" ])
    # print(df.head)
    with tab1:
        st.subheader("Implications and affected Domains")
        st.dataframe(df)
    with tab2:
        st.subheader("Types of Implications")
    with tab3:
        st.subheader("Impact of AI ")