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
    if not os.path.isfile(output_data_path):
        with pd.ExcelWriter(output_data_path, engine='openpyxl') as writer:
            pd.DataFrame().to_excel(writer, sheet_name="Init", index=False)

    
    with pd.ExcelWriter(output_data_path, engine='openpyxl') as writer:
        
        fieldnames = ['3.3 Learning Activities'] 
# '1.1 Domain', '1.2 Potential AI Use Cases','1.3 Data in the Domain', 
#                                 '1.4 Implications of Using AI', '1.5 Additional Learning Resources', 
# '2.1 Learners and Their Interaction with AI', 
#                                 '2.2 Instructors', '2.3 Internal Support', '3.1 Learning Outcomes', 
#                                 '3.2 Assessment', 
        

        for columnname in fieldnames:
            df_keywords = pd.DataFrame()    
            column_data = df[columnname].tolist()
            print(f"columnname is {columnname}")
            keywords = []

            for text in column_data:
            # Chain-of-Thought Prompt
                prompt = f"""
                    **Prompt:**  I  want you to act as a qualitative data analyzer. You should be able to summarize concepts with minimum words. 
                    **Example:**

                    **Prompt:** Summarize this text and create only 3 keywords: "This technology enables real-time, personalized recommendations for products and services based on individual user preferences and behavior." 

                    **Chain-of-Thought:**

                    1. **Understand the text:** The text describes a technology that provides customized recommendations to users. 
                    2. **Identify key themes:** Key themes include personalization, real-time analysis, and user preferences.
                    3. **Select minimum essential keywords:** 

                    **Answer:** Personalized Recommendations, Real-time Analysis, User Preferences

                    **Your Turn:**
                    **Prompt:** Summarize this text and create minimum absolute no. of keywords: {text}. I don't want anything else.

                    **Chain-of-Thought:**
                    1. **Understand the text:** Read the text carefully and identify the main topic and key concepts.
                    2. **Identify key themes:** Determine the most important and relevant themes discussed in the text.
                    3. **Select minimum number of keywords:** Choose words or short phrases that best represent the key themes and provide a concise summary of the text.
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
                
                keywords_array = (response_clean).split(',')
                print(keywords_array)
                keywords.append(keywords_array)
                time.sleep(5)
            
            
            # df_keywords[columnname] = keywords
            df_keywords['Serial number'] = df['Serial number']
            df_keywords[columnname] = ['; '.join(map(str, kw)).strip() for kw in keywords]
            df_keywords[columnname] = df_keywords[columnname].str.replace(r'\[|\]', '', regex=True)
            sheet_name = f"keywords_{columnname}".replace(':', '_')[:31]

            df_keywords.to_excel(writer, sheet_name=sheet_name, index=False)
                
            
if __name__ == '__main__':
    local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
    raw_data_path = os.path.join(local_dir,"output_course_data.xlsx")
    output_data_path = os.path.join(local_dir, "output_data_keywords.xlsx")
    print(f"Output data path: {output_data_path}")
    # print(os.path.exists(output_data_path))

    df= pd.read_excel(raw_data_path)
    
    output_keywords_df = get_keywords(df, output_data_path)
