import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os, re
from collections import Counter
import matplotlib.pyplot as plt

# Set page title and layout
st.set_page_config(page_title="Learners and Their Interaction with AI", layout="wide")

st.title("2.1 Learners and Their Interaction with AI ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
learners_file = os.path.join(local_dir,"view_learners.xlsx")

df_learners = pd.read_excel(learners_file, sheet_name="Learners of AI")

# Set the 'Domain' column as index for plotting
df_learners.set_index("Domain", inplace=True)

# Plot the stacked bar chart
st.subheader("Distribution of Learners at different levels")
fig, ax = plt.subplots(figsize=(10, 4))
df_learners.plot(kind="bar", stacked=True, ax=ax)

# Formatting
ax.set_ylabel("Percentage")
ax.set_xlabel("Domains")
ax.set_title("AI Learners by Domain")
plt.xticks(rotation=45, ha='right')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title="Levels of AI Learners", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Display the chart in Streamlit
st.pyplot(fig)


# Optional: expand rows to show each implication in detail
with st.expander("🔍 View Learners data in tabular format"):
    st.subheader("Learners Data")
    st.dataframe(df_learners)