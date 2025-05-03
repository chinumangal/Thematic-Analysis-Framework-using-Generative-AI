import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Define the domains
domains = [
    'Engineering & Technology', 'Natural Sciences', 'Computer Science & Data',
    'Applied Sciences & Vocational Fields', 'Business & Economics',
    'Social Sciences & Humanities', 'Medical & Health Sciences',
    'Design & Creative Arts'
]

# Define the factors for the spider chart
factors = [
    'Budget', 'Course Duration', 'Personnel',
    'Availability of domain-specific data',
    'Access to software and hardware', 'Institutional Support'
]

# Simulate data (replace with your actual data if available)
np.random.seed(42)  # for reproducibility
data = {}
data['Domain'] = domains
for factor in factors:
    data[factor] = np.random.randint(1, 11, size=len(domains)) # Simulate scores from 1 to 10

df = pd.DataFrame(data)

# Streamlit app
st.title(" Internal Support")

# Allow user to select domains to display
selected_domains = st.multiselect("Select Domains to Display:", domains, default=domains)

if selected_domains:
    filtered_df = df[df['Domain'].isin(selected_domains)].copy() # Use .copy() to avoid SettingWithCopyWarning

    # Create the spider chart using Plotly
    fig = go.Figure()

    for index, row in filtered_df.iterrows():
        theta = factors + [factors[0]]  # Close the circle
        r = row[factors].tolist() + [row[factors].tolist()[0]] # Close the circle
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            name=row['Domain']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10] # Adjust range based on your simulated data scale
            )),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered_df)

else:
    st.warning("Please select at least one domain to display the spider chart.")

st.subheader("Simulated Data")
st.dataframe(df)