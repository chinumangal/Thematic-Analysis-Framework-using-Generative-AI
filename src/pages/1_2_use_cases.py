import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter
from search_embedding import find_nearest_neighbors

st.title("📊 Potential AI Use Cases ")
st.write('''
    This subtopic explores the impact of AI technology on various domains, identifying current use cases and predicting future potential applications for AI in problem-solving domain-specific issues.
''')
st.markdown("**Source file:** view_use_cases.csv ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")
use_cases = os.path.join(local_dir, "views", "view_use_cases.csv")

fieldname = '1.2 Potential AI Use Cases'

if use_cases is not None:
    df = pd.read_csv(use_cases, sep=";", encoding="ISO-8859-1")
    tab1, tab2, tab3 = st.tabs(["Search Use cases","Details", "Relevance in domains" ])
    # print(df.head)
    with tab1:
        query_text = st.text_input(label="Enter your use case here")


        if st.button(label="Search similar frameworks"):
            output_data = find_nearest_neighbors(fieldname, query_text)
            st.subheader('AI Course design framework')
            st.write(output_data)
            print(output_data)

    with tab2: 
        st.subheader("Details")
        all_use_cases = []
        for entry in df["Cluster_use_cases"].dropna():

                cleaned = re.sub(r"[\[\]]", "", entry)  
                domains = [d.strip() for d in cleaned.split(";") if d.strip()]
                all_use_cases.extend(domains)


        use_case_counts = pd.DataFrame(Counter(all_use_cases).items(), columns=["Cluster_use_cases", "Count"])
        use_case_counts = use_case_counts.sort_values(by="Count", ascending=False)

        selected_use_case = st.selectbox("Select a use case to view detailed information:",  use_case_counts["Cluster_use_cases"].tolist(), key= "selectbox_details")

        if selected_use_case:
            st.subheader(f" Selected use case: {selected_use_case}")
            filtered_df = df[df["Cluster_use_cases"].str.contains(selected_use_case, na=False)]
            filtered_df = filtered_df[['Serial number', 'Course name',fieldname]]
            st.dataframe(filtered_df)
            
    with tab3:
        st.subheader("Relevance in Domains")
        selected_use_case = st.selectbox("Select a use case to view relevance in different domains:",  use_case_counts["Cluster_use_cases"].tolist(), key= "selectbox_relevance")
        all_domains = []
        
        if selected_use_case:
            filtered_df = df[df["Cluster_use_cases"].str.contains(selected_use_case, na=False)]
            filtered_df = filtered_df[['Serial number', 'Course name', 'Cluster', fieldname]]
            for entry in filtered_df["Cluster"].dropna():

                cleaned = re.sub(r"[\[\]]", "", entry)  
                domains = [d.strip() for d in cleaned.split(";") if d.strip()]
                all_domains.extend(domains)
                
            domain_counts = pd.DataFrame(Counter(all_domains).items(), columns=["Domain", "Count"])
            domain_counts = domain_counts.sort_values(by="Count", ascending=False)
            

            total_count = domain_counts["Count"].sum()
            domain_counts["Percentage"] = (domain_counts["Count"] / total_count) * 100
            domain_counts["Percentage"] = domain_counts["Percentage"].round(2).astype(str) + " %"
            use_case_relevance_df = domain_counts[['Domain', 'Percentage']]
            st.dataframe(use_case_relevance_df)
