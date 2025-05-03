import pandas as pd
import google.generativeai as genai
import streamlit as st
import altair as alt
import os, csv
from io import StringIO

# Your original DataFrame (as defined in the previous turn)
local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data10.xlsx")
df_original = pd.read_excel(course_data, engine="openpyxl")
fieldname = '2.1 Learners and Their Interaction with AI'

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if "GEMINI" in config and "api_key" in config["GEMINI"]:
    api_key = config["GEMINI"]["api_key"]
else:
    api_key = None

genai.configure(api_key=api_key)
# Create the model
generation_config = {
   "temperature": 0.4,
    "top_p": 0.3,
    "top_k": 10,
    "max_output_tokens": 192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

# Define your stakeholder groups
stakeholder_groups = [
    "Consumers, the General Public and Policymakers",
    "Co-Workers and Users of AI Products",
    "Collaborators and AI Implementers",
    "Creators of AI"
]

def classify_with_gemini(expected_role_text, stakeholder_groups):
    prompt = f"""Please classify the following "Expected Role After Completion" into the given stakeholder groups. For each stakeholder group, indicate the level of involvement (e.g., High, Medium, Low, or None).

    Expected Role: {expected_role_text}

    Stakeholder Groups:
    - {stakeholder_groups[0]}
    - {stakeholder_groups[1]}
    - {stakeholder_groups[2]}
    - {stakeholder_groups[3]}

    Provide your classification as a dictionary where the keys are the stakeholder groups and the values are the level of involvement."""

    try:
        response = model.generate_content(prompt)
        if response.parts and hasattr(response.parts[0], 'text'):
            classification_text = response.parts[0].text.strip()
            # Attempt to parse the CSV response
            reader = csv.reader(StringIO(classification_text))
            for row in reader:
                if len(row) == len(stakeholder_groups):
                    return dict(zip(stakeholder_groups, row))
                else:
                    print(f"Error: Unexpected number of values in CSV response: {classification_text}")
                    return {group: "Error" for group in stakeholder_groups}
            return {group: "Error" for group in stakeholder_groups}
        else:
            return {group: "Error" for group in stakeholder_groups}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {group: "Error" for group in stakeholder_groups}

# Apply Gemini classification to each course
gemini_classifications = []
for index, row in df_original.iterrows():
    if "Expected Role After Completion:" in row[fieldname]:
        expected_role = row[fieldname].split("Expected Role After Completion:")[1].strip()
        classification = classify_with_gemini(expected_role, stakeholder_groups)
        gemini_classifications.append(classification)
    else:
        gemini_classifications.append({group: "Not Applicable" for group in stakeholder_groups})

df_gemini = pd.DataFrame(gemini_classifications)

# Combine with domain information (similar to before)
df_final_gemini = pd.concat([df_original['Domain'].str.split('; ', expand=True).stack().reset_index(drop=True).rename('Domain'),
                             df_original[['Course']]], axis=1)

# Repeat Gemini classifications for each domain listed for a course
df_final_gemini = pd.merge(df_final_gemini, df_gemini.loc[df_final_gemini.index // (df_gemini.shape[0] // df_original['Domain'].str.split('; ').str.len().sum())].reset_index(drop=True), left_index=True, right_index=True)

# For simplicity, let's map the 'level of involvement' to a numerical value for the chart
level_mapping = {"High": 3, "Medium": 2, "Low": 1, "None": 0, "Unknown": 0, "Error": 0, "Not Applicable": 0}
for group in stakeholder_groups:
    df_final_gemini[group + " Score"] = df_final_gemini[group].map(level_mapping)

# Group by Domain and sum the scores
df_grouped_gemini = df_final_gemini.groupby('Domain')[[group + " Score" for group in stakeholder_groups]].sum().reset_index()

# Melt for Altair
df_melted_gemini = df_grouped_gemini.melt(id_vars='Domain', var_name='Stakeholder Group', value_name='Implied Involvement Score')

# Create the stacked bar chart
chart_gemini = alt.Chart(df_melted_gemini).mark_bar().encode(
    x=alt.X('Domain', title='Domain'),
    y=alt.Y('Implied Involvement Score', title='Implied Level of Involvement'),
    color='Stakeholder Group',
    tooltip=['Domain', 'Stakeholder Group', 'Implied Involvement Score']
).properties(
    title='Implied Level of Involvement of Stakeholder Groups by Domain (Classified by Gemini)'
)

# # Display in Streamlit
# st.title("Implied Level of Involvement of Stakeholder Groups by Domain (Gemini Classification)")
# st.altair_chart(chart_gemini, use_container_width=True)

# st.subheader("Gemini Classification Output")
# st.dataframe(df_final_gemini)