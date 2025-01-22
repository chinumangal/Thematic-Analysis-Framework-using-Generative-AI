import os
import pandas as pd
import google.generativeai as genai
import time

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 192,
  "response_mime_type": "text/plain",
}

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
raw_data_path = os.path.join(local_dir,"raw_data.csv")
output_data_path = os.path.join(local_dir, "output_data.csv")

df= pd.read_csv(raw_data_path, encoding='ISO-8859-1', sep=';')

domain = df['Domain'].tolist()
use_case = df['Potential use cases'].tolist()

keywords = []

for text in use_case:
   # Chain-of-Thought Prompt
  prompt = f"""
    **Prompt:**  I  want you to act as a qualitative data analyzer. You should be able to summarize concepts with minimum words. 
    **Example:**

    **Prompt:** Summarize this text and create only 3 keywords: "This technology enables real-time, personalized recommendations for products and services based on individual user preferences and behavior." 

    **Chain-of-Thought:**

    1. **Understand the text:** The text describes a technology that provides customized recommendations to users. 
    2. **Identify key themes:** Key themes include personalization, real-time analysis, and user preferences.
    3. **Select 3 keywords:** 

    **Answer:** Personalized Recommendations, Real-time Analysis, User Preferences

    **Your Turn:**
    **Prompt:** Summarize this text and create only 3 keywords: {text}. I don't want anything else.

    **Chain-of-Thought:**
    1. **Understand the text:** Read the text carefully and identify the main topic and key concepts.
    2. **Identify key themes:** Determine the most important and relevant themes discussed in the text.
    3. **Select 3 keywords:** Choose three words or short phrases that best represent the key themes and provide a concise summary of the text.

    
    **Answer:** 
    """

  # print(text)
  model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  response = chat_session.send_message(prompt)

  keywords_array = (response.text).split(',')
  print(keywords_array)
  keywords.append(keywords_array)
  time.sleep(10)

df['use_case_keywords'] = keywords
# print(len(keywords))

df.to_csv(output_data_path, index=False, sep=";")