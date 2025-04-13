import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter

st.title("📊 Domain Distribution (Pie Chart)")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
data_types = os.path.join(local_dir,"view_data_types.csv")

if data_types is not None:
    df = pd.read_csv(data_types, sep=";")
    # print(df.head)
    if "Cluster_data_types" in df.columns:
        # Clean and split domain entries
        all_domains = []
        # st.write(df.head)
        for entry in df["Cluster_data_types"].dropna():
            # Remove brackets and split by semicolon
            cleaned = re.sub(r"[\[\]]", "", entry)  # remove [ and ]
            domains = [d.strip() for d in cleaned.split(";") if d.strip()]
            all_domains.extend(domains)

        # Count domain frequencies
        domain_counts = pd.DataFrame(Counter(all_domains).items(), columns=["Cluster_data_types", "Count"])
        domain_counts = domain_counts.sort_values(by="Count", ascending=False)
        print(domain_counts)
        # Pie Chart
        st.subheader("📊 Pie Chart of Cluster_data_types")
        fig = px.pie(domain_counts, values="Count", names="Cluster_data_types", title="Cluster Data type Distribution", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔢 Data type Frequency")
        st.dataframe(domain_counts)
    else:
        print("error")        
        st.error("❌ 'cluster' column not found in the uploaded file.")