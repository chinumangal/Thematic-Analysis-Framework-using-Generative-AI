import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter

st.title("📊 Data in the Domain")

st.write('''
AI use cases are based on the most relevant data type in a domain, allowing for targeted use of AI techniques. Understanding typical data in a domain, such as time-series data, texts, images, and abundant or scarce data, significantly impacts the effectiveness of AI techniques.
''')

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
data_types = os.path.join(local_dir,"view_data_types.csv")

if data_types is not None:
    df = pd.read_csv(data_types, sep=";", encoding="ISO-8859-1")
    tab1, tab2 = st.tabs(["Data types", "Distribution across domains"])
    # print(df.head)
    with tab1:
        if "Cluster_data_types" in df.columns:
            # Clean and split domain entries
            all_data_types = []
            # st.write(df.head)
            for entry in df["Cluster_data_types"].dropna():
                # Remove brackets and split by semicolon
                cleaned = re.sub(r"[\[\]]", "", entry)  # remove [ and ]
                data_types = [d.strip() for d in cleaned.split(";") if d.strip()]
                all_data_types.extend(data_types)

            # Count domain frequencies
            data_type_counts = pd.DataFrame(Counter(all_data_types).items(), columns=["Cluster_data_types", "Count"])
            data_type_counts = data_type_counts.sort_values(by="Count", ascending=False)
            # print(data_type_counts)
            # Pie Chart
            st.subheader("📊 Pie Chart of Cluster_data_types")
            fig = px.pie(data_type_counts, values="Count", names="Cluster_data_types", title="Cluster Data type Distribution", hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("🔢 Data type Frequency")
            st.dataframe(data_type_counts)
            
        else:     
            st.error("❌ 'cluster' column not found in the uploaded file.")
        
    with tab2:
        df['Cluster'] = df['Cluster'].str.split('; ')
        df_exploded = df.explode('Cluster')
        
        df_exploded['Cluster_data_types'] = df_exploded['Cluster_data_types'].str.split('; ')
        df_exploded_new = df_exploded.explode('Cluster_data_types')

        pivot_df = pd.pivot_table(
            df_exploded_new,
            index='Cluster',
            columns='Cluster_data_types',
            values='Course name',
            aggfunc='count',
            fill_value=0,
            sort= False
        )
        pivot_percent = (pivot_df.div(pivot_df.sum(axis=0), axis=1) * 100)
        st.subheader("🔢 Data type across domains")
        st.dataframe(pivot_percent.round(1).astype(str) + '%' )
        
