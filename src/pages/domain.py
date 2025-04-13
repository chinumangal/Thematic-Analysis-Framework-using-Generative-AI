import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter

st.title("📊 Domain Distribution (Pie Chart)")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")


if course_data is not None:
    df = pd.read_excel(course_data)

    if "Cluster" in df.columns:
        # Clean and split domain entries
        all_domains = []

        for entry in df["Cluster"].dropna():
            # Remove brackets and split by semicolon
            cleaned = re.sub(r"[\[\]]", "", entry)  # remove [ and ]
            domains = [d.strip() for d in cleaned.split(";") if d.strip()]
            all_domains.extend(domains)

        # Count domain frequencies
        domain_counts = pd.DataFrame(Counter(all_domains).items(), columns=["Domain", "Count"])
        domain_counts = domain_counts.sort_values(by="Count", ascending=False)

        # Pie Chart
        st.subheader("📊 Pie Chart of Domains")
        fig = px.pie(domain_counts, values="Count", names="Domain", title="Cluster Domain Distribution", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔢 Domain Frequency")
        st.dataframe(domain_counts)
    else:
        st.error("❌ 'cluster' column not found in the uploaded file.")