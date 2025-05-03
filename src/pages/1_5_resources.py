import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter
from search_embedding import find_nearest_neighbors

st.title("Additional Learning Resources ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")
# impl_data = os.path.join(local_dir,"AI_Implications_Domains.csv")
resources_data = os.path.join(local_dir, "view_resources.csv")
fieldname = '1.5 Additional Learning Resources'

if resources_data is not None:
    df = pd.read_csv(resources_data, sep=";", encoding="ISO-8859-1")
    tab1, tab2 = st.tabs(["Distribution of resources across Domains", "Most suggested resources" ])
    # print(df.head)
    with tab1:
        st.subheader("Distribution of resources across Domains")
        st.dataframe(df)
    with tab2:
        all_resources = []
        for entry in df["Cluster_resources"].dropna():
                # Remove brackets and split by semicolon
                cleaned = re.sub(r"[\[\]]", "", entry)  # remove [ and ]
                domains = [d.strip() for d in cleaned.split(";") if d.strip()]
                all_resources.extend(domains)

            # Count domain frequencies
        use_case_counts = pd.DataFrame(Counter(all_resources).items(), columns=["Cluster_resources", "Count"])
        use_case_counts = use_case_counts.sort_values(by="Count", ascending=False)

        selected_use_case = st.selectbox("Select a use case to view detailed information:",  use_case_counts["Cluster_resources"].tolist(), key= "selectbox_details")

        if selected_use_case:
            st.subheader(f" Selected use case: {selected_use_case}")
            filtered_df = df[df["Cluster_resources"].str.contains(selected_use_case, na=False)]
            filtered_df = filtered_df[['Serial number', 'Course name',fieldname]]
            st.dataframe(filtered_df)