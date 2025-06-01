# Thematic Analysis and Filtering Framework Using Generative AI 

This tool helps design new AI courses within a given domain by leveraging thematic insights from previously designed courses across different domains. It performs thematic analysis to extract keywords from course design frameworks and enables flexible filtering using Generative AI.



**Web Version:**

1. Visit the live app: https://aithematicanalysis.streamlit.app/
   
2. To add new data:
   - First, provide your **Gemini API Key** and save it for future sessions.

3. Choose the **'Load Data'** option:
   - **a.** Upload new data as a ZIP folder containing structured `.txt` files.
   - **b.** Select **'Save to Excel file'** to convert the uploaded text files into Excel format.

4. Explore different sections of the AI Course Framework through the app interface.
---

**Developer Version(Local Setup):**

1. Clone the Repository
```bash
git clone https://github.com/darshina2/AI_Thematic_analysis.git
cd AI_Thematic_analysis
```
2. Create a Virtual Environment
Create a virtual environment using Python:
```
python -m venv env
```
   Replace env with your preferred virtual environment name if needed. 

3. Install Dependencies
```
pip install -r requirements.txt
```
4. Add API Key in config.ini file
```
GEMINI_API_KEY=your_key_here
```
4. Run the Script
   
   a. To generate new example of the course framework
   ```
   python src/datagen.py
   ```
   b. To evaluate the course content to generate keywords
   ```
   python src/keyword_extraction.py
   ```
   c. To generate embeddings 
   ```
   python src/search_embedding.py
   ```
   d. To run the streamlit app
   ```
   python src/page_manager.py
   ```
