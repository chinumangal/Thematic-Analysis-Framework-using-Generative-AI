import os, re
import pandas as pd
import google.generativeai as genai
import time
from openpyxl import load_workbook

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 192,
  "response_mime_type": "text/plain",
}

def get_keywords(df, output_data_path):
 
    df_existing = pd.DataFrame() 
    df_existing['Serial number'] = df['Serial number']
    try:
        fieldnames = ['1.1 Domain', '1.2 Potential AI Use Cases', '1.3 Data in the Domain', 
                        '1.4 Implications of Using AI', '1.5 Additional Learning Resources',
                        '2.1 Learners and Their Interaction with AI','2.2 Instructors', 
                        '2.3 Internal Support', '3.1 Learning Outcomes', 
                        '3.2 Assessment','3.3 Learning Activities'] 

        

        for columnname in fieldnames:
            # df_keywords = pd.DataFrame()    
            # column_data = df[columnname].tolist()
            print(f"columnname is {columnname}")
            keywords = []

            for text in df[columnname].tolist():
            # Chain-of-Thought Prompt
                prompt = f"""
                    **Prompt:**  I  want you to act as a qualitative data analyzer. You should be able to summarize concepts with keywords that best explain the theme. Do not include generic words, I want specific keywords to best define the text below. 
                    **Example:**

                    **Prompt:** Summarize this text and create keywords: " Robotics  *   Definition: Robotics is the field of engineering focused on the design, construction, operation, and application of robots. It combines aspects of mechanical engineering, electrical engineering, computer science, and increasingly, artificial intelligence to create intelligent machines capable of performing various tasks, ranging from industrial automation to complex exploration. *   Relevance:  AI is rapidly transforming robotics by enabling robots to perceive their environment, make intelligent decisions, learn from experience, and adapt to new situations. This is pushing the boundaries of what robots can achieve, making them more versatile and autonomous." 

                    **Chain-of-Thought:**

                    1. **Understand the text:** Focus on the field's interdisciplinary nature and specific engineering domains involved.
                    2. **"Select keywords to Highlight AI's transformative impact on perception, decision-making, learning, and adaptability in robotics.**
                    3. **Emphasize the outcomes such as industrial automation and complex exploration.**

                    **Answer:** robotics engineering, intelligent machines, industrial automation, complex exploration, AI-driven adaptability, environmental perception, decision-making algorithms, mechanical-electrical integration, autonomous systems, machine learning in robotics

                    **Your Turn:**
                    **Prompt:** Summarize this text and create minimum absolute no. of keywords: {text}. I don't want anything else.

                    **Chain-of-Thought:**
                    1. **Understand the text:** Read the text carefully and identify the main topic and key concepts.
                    2. **Identify key themes:** Determine the most important and relevant themes discussed in the text.
                    3. **Select keywords:** Choose words or short phrases that best represent the key themes and provide a concise summary of the text.
                    4. **Do not add any additional text for heading or summary like **answer. Just provide keywords required.

                    
                    **Answer:** 
                    """

                # print(text)
                model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash-exp",
                    generation_config=generation_config,
                )

                chat_session = model.start_chat(history=[])
                response = chat_session.send_message(prompt)

                response_clean = (response.text).replace("\r\n", " ").replace("[]", " ").strip()
                # response_clean = re.sub(r"[-()\"#/@;:<>{}-=~|.?,]","",response_clean)
                
                # keywords_array = (response_clean).split(',')
                keywords_array = response_clean.split(',')
                print(keywords_array)
                keywords.append('; '.join(map(str.strip, keywords_array)))
                time.sleep(5)
            
            df_existing[f"Keywords_{columnname}"] = keywords
            # df_existing.head()
            time.sleep(300)
            
        df_existing.to_csv(output_data_path, index=False, sep=";")
                
           
    except Exception as e:
        print(f"failed with an error {e} ")
                
            
if __name__ == '__main__':
    local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
    raw_data_path = os.path.join(local_dir,"Course_output_data.xlsx")
    output_data_path = os.path.join(local_dir, "keywords_output_data.csv")
    print(f"Output data path: {output_data_path}")
    # print(os.path.exists(output_data_path))

    df= pd.read_excel(raw_data_path)
    
    output_keywords_df = get_keywords(df, output_data_path)
