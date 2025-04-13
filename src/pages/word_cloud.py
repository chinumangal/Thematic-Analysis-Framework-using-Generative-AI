import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
course_data = os.path.join(local_dir,"Course_output_data.xlsx")
keyword_data = os.path.join(local_dir,"keywords_output_data.csv")
# Load data into DataFrame
df = pd.read_csv(keyword_data, sep=";", encoding="ISO--8859-1")


filtered_df = df[df['Cluster'].str.contains('Medical')]
st.title('Thematic Analysis and Filtering Framework Using Generative AI')
st.write("How does the data look like in medical domain?")
# fieldname = '1.1 Domain'
def make_word_cloud(fieldname):
    # Extract keywords
    columnname = f"Keywords_{fieldname}"
    keywords_text = " ".join(filtered_df[columnname].tolist()).replace(";", " ")

    # Generate Word Cloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color="white", 
        colormap="viridis", 
        max_words=100
    ).generate(keywords_text)

    # Streamlit UI
    # st.title("Word Cloud of Keywords")
    st.write(f"This word cloud represents the most frequent keywords for {fieldname} across medical domain.")

    # Display Word Cloud in Streamlit
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")  # Hide axis

    st.pyplot(fig)

# st.write(columnname)

fieldname = st.selectbox(
                'Select the field name',
                    ('1.1 Domain', '1.2 Potential AI Use Cases','1.3 Data in the Domain',
                        '1.4 Implications of Using AI', '1.5 Additional Learning Resources',
                        '2.1 Learners and Their Interaction with AI','2.2 Instructors', 
                        '2.3 Internal Support', '3.1 Learning Outcomes', 
                        '3.2 Assessment','3.3 Learning Activities'))

# query_text = st.text_input(label="Enter your text here")

# Corrected code using a lambda function
if st.button(label="Generate"):
    output = make_word_cloud(fieldname)
    

