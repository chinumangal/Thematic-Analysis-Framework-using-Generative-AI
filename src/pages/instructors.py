import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os, re
from collections import Counter
from search_embedding import find_nearest_neighbors

st.title("Instructors ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")



data = {
    'Domain': [
        'Engineering & Technology', 'Natural Sciences', 'Computer Science & Data',
        'Applied Sciences & Vocational Fields', 'Business & Economics',
        'Social Sciences & Humanities', 'Medical & Health Sciences',
        'Design & Creative Arts'
    ],
    'Consumers, the General Public and Policymakers': [21.5, 13.9, 16.8, 17.6, 17.4, 20.2, 16.9, 18.2],
    'Co-Workers and Users of AI Products': [24.5, 17.2, 21.4, 23.9, 23.9, 25.1, 23.9, 24.8],
    'Collaborators and AI Implementers': [26.9, 23.5, 26.6, 26.4, 27.2, 27.5, 27.6, 27.5],
    'Creators of AI': [27.1, 45.4, 35.2, 32.1, 31.5, 27.2, 31.6, 29.5]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Melt the DataFrame for Altair
df_melted = df.melt(id_vars='Domain', var_name='Stakeholder Group', value_name='Percentage')

# Create the stacked bar chart using Altair
chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X('Domain', title='Domain'),
    y=alt.Y('Percentage', title='Percentage'),
    color='Stakeholder Group',
    tooltip=['Domain', 'Stakeholder Group', 'Percentage']
).properties(
    title='Percentage Distribution by Domain and Stakeholder Group'
)

# Display the chart in Streamlit
# st.title("Stacked Bar Chart of Percentage Distribution")
st.altair_chart(chart, use_container_width=True)

# Optionally, display the raw DataFrame as well
st.subheader("Raw Data")
st.dataframe(df)
