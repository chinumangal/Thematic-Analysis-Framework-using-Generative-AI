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
4. Add API Key
   Edit or create a file named config.ini with the following content:
```
GEMINI_API_KEY=your_key_here
```
4. Run the Script
   
   a. Generate sample course frameworks
   ```
   python src/dataloader.py
   ```
   **Output**: Course_output_data.xlsx
   Contains structured course design data simulated using Gemini AI, including fields such as Domain, Use Cases, Learners, Instructors, and Learning Outcomes.

   b. Extract keywords from course content
   ```
   python src/keyword_extraction.py
   ```
   **Output**: keyword_output_data.csv
   Extracted thematic keywords for each field in the course framework using chain-of-thought prompting.

   c. Save embeddings for the extracted keywords 
   ```
   python src/search_embedding.py
   ```
   **Output**: output_embeddings.csv 
   A serialized file containing vector embeddings for each keyword, used to perform similarity-based filtering.

   d. Create clusters for the analysis
      
      - **Domain**:
        ```
        python src/clustering_domain.py
        ```
      - **Use Cases**:
         ```
        python src/clustering_use_cases.py
         ```
      - **Data Type**:
        ```
        python src/clustering_data.py
        ```
      - **Implications**:
        ```
              python src/implications/clustering_common_implications.py
              python src/implications/clustering_domain_implications.py
              python src/implications/clustering_courses_implications.py
        ```
      - **Learners**:
         ```
        python src/clustering_learners.py
         ```
      - **Instructors**:
        ```
        python src/clustering_instructors.py
        ```
      - **Internal Support**:
        ```
      - python src/clustering_internal_support.py
        ```
      - **Assessment**:
        ```
        python src/clustering_assessment.py
        ```
      - **Learning Activity**:
        ```
        python src/clustering_activities.py
        ```
   
   d. Launch the Streamlit web app ((runs at http://localhost:8501/))
   ```
   python src/page_manager.py
   ```
   e. Create clusters 
