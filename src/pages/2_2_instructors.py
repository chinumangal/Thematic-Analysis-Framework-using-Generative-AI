import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os, re
from collections import Counter
import matplotlib.pyplot as plt

# Set page title and layout
st.set_page_config(page_title="Instructors", layout="wide")

st.title("📊 Instructors ")
st.write('''
Domain-specific AI teaching requires a mix of sufficient AI knowledge, domain expertise and pedagogical skills to teach an interdisciplinary course as well as the motivation and time from an instructor’s perspective.''')

st.markdown("**Source file:** view_instructors.csv ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
learners_file = os.path.join(local_dir,"view_instructors.xlsx")

df_instructors = pd.read_excel(learners_file, sheet_name="Instructors")

# Set the 'Domain' column as index for plotting
df_instructors.set_index("Domain", inplace=True)

# Plot the stacked bar chart
st.subheader("Distribution of Instructors in Domain")
fig, ax = plt.subplots(figsize=(10, 4))
df_instructors.plot(kind="bar", stacked=True, ax=ax)

# Formatting
ax.set_ylabel("Percentage")
ax.set_xlabel("Domains")
ax.set_title("Hierarchy of Instructors")
plt.xticks(rotation=45, ha='right')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title="Hierarchy of Instructors", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Display the chart in Streamlit
st.pyplot(fig)


# Optional: expand rows to show each implication in detail
with st.expander("🔍 View Instructors data in tabular format"):
    st.subheader("Hierarchy of Instructors")
    st.dataframe(df_instructors)