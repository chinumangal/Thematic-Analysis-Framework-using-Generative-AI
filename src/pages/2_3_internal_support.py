import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
output_data_path = os.path.join(local_dir, "view_internal_support.csv")
df = pd.read_csv(output_data_path, delimiter=';')

domains = df['Cluster'].tolist()
factors = list(df)

data = {}
data["Domain"] = df['Cluster']
# Streamlit app
st.title("📊 Internal Support")

st.write('''Internal support, including budget, personnel restraints, course duration, data, software, and hardware, can be seen as resources or limitations in AI teaching. Instructor support, institutional barriers, and student support also impact course design.''')
st.markdown("**Source file:** view_internal_support.csv ")

# Allow user to select domains to display
# selected_domains = st.multiselect("Select Domains to Display:", domains, default=domains)
factors = [col for col in df.columns if col != 'Cluster']
selected_domains = st.multiselect("Select Clusters to Display:", df['Cluster'].tolist(), default=df['Cluster'].tolist())


if selected_domains:
    filtered_df = df[df['Cluster'].isin(selected_domains)].copy()

    fig = go.Figure()

    for _, row in filtered_df.iterrows():
        theta = factors + [factors[0]]
        r = row[factors].tolist() + [row[factors].tolist()[0]]
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            name=row['Cluster']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=False)
    # st.dataframe(filtered_df)
else:
    st.warning("Please select at least one cluster.")