import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter

st.title("📊 AI in the Domain ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
cluster_data = os.path.join(local_dir,"view_domain_clusters.csv")

st.write('''
Describing the use of AI in the domain is the starting point of any endeavor to create a
domain-speciﬁc AI course, as it determines what content will be taught in the corresponding
courses.
''')
st.markdown("**Source file:** view_domain_clusters.csv ")
st.markdown("**Disclaimer:** A course can be classified in maximum 2 domains. ")

if cluster_data is not None:
    df = pd.read_csv(cluster_data, delimiter=';')
    
    if "Cluster" in df.columns:
        # Clean and split domain entries
        all_domains = []
        tab1, tab2 = st.tabs(["Overview", "Details" ])
        
        with tab1:
            for entry in df["Cluster"].dropna():
                # Remove brackets and split by semicolon
                cleaned = re.sub(r"[\[\]]", "", entry)  # remove [ and ]
                domains = [d.strip() for d in cleaned.split(";") if d.strip()]
                all_domains.extend(domains)

            # Count domain frequencies
            domain_counts = pd.DataFrame(Counter(all_domains).items(), columns=["Domain", "Count"])
            domain_counts = domain_counts.sort_values(by="Count", ascending=False)

            # Pie Chart
            fig = px.pie(domain_counts, values="Count", names="Domain", title="Cluster Domain Distribution", hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("🔢 Domain Frequency")
            st.dataframe(domain_counts)

            
        with tab2:
         # Interactive Domain Filter
            selected_domain = st.selectbox("Select a domain to view details:",  domain_counts["Domain"].tolist())

            if selected_domain:
                st.subheader(f" Details for: {selected_domain}")
                filtered_df = df[df["Cluster"].str.contains(selected_domain, na=False)]
                st.dataframe(filtered_df)
    else:
        st.error("❌ 'cluster' column not found in the uploaded file.")
