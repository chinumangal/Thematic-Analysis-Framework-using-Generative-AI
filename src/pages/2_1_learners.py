import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os, re
from collections import Counter
import matplotlib.pyplot as plt


st.set_page_config(page_title="Learners and Their Interaction with AI", layout="wide")

st.title("📊 Learners and Their Interaction with AI ")
st.write('''
Three considerations are important for domain-specific AI courses for learners. First is to understand which AI skills and related competencies. Second, it is important to clarify the role of the group of learners regarding their interaction with AI to choose relevant demonstrations of AI-applications and an appropriate level of difficulty. Third, the existing competencies and the future role are influenced by the curricular integration of the course in an overall program. 
''')
st.markdown("**Source file:** view_learners.csv ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
learners_file = os.path.join(local_dir, "views", "view_learners.xlsx")

df_learners = pd.read_excel(learners_file, sheet_name="Learners of AI")


df_learners.set_index("Domain", inplace=True)


st.subheader("Distribution of Learners at different levels")
fig, ax = plt.subplots(figsize=(10, 4))
df_learners.plot(kind="bar", stacked=True, ax=ax)


ax.set_ylabel("Percentage")
ax.set_xlabel("Domains")
ax.set_title("AI Learners by Domain")
plt.xticks(rotation=45, ha='right')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title="Levels of AI Learners", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

st.pyplot(fig)



with st.expander("🔍 View Learners data in tabular format"):
    st.subheader("Learners Data")
    st.dataframe(df_learners)