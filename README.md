# Thematic Analysis and Filtering Framework Using Generative AI 

This tool helps design new AI courses within a given domain by leveraging thematic insights from previously designed courses across different domains. It performs thematic analysis to extract keywords from course design frameworks and enables flexible filtering using Generative AI.



**Web Version:**

1. Visit the live app: https://aithematicanalysis.streamlit.app/
   
2. To add new data:
   - First, provide your **Gemini API Key** and save it for future sessions.

3. Choose the **'Load Data'** option:
   -  Upload new data as a ZIP folder containing structured `.txt` files.
   -  Select **'Save to Excel file'** to convert the uploaded text files into Excel format.

4. Explore different sections of the AI Course Framework through the app interface.
---

**Developer Version(Local Setup):**

1. Clone the Repository
```bash
git clone https://github.com/darshina2/AI_Thematic_analysis.git
cd AI_Thematic_analysis
```
2. Create a Virtual Environment
```
python -m venv env
```
  Replace env with your preferred virtual environment name if needed. 

3. Install Dependencies
```
pip install -r requirements.txt
```
4. Add API Key:
   Edit or create a file named config.ini with the following content:
```
GEMINI_API_KEY=your_key_here
```
4. Run the Script
   
   a. Generate sample course frameworks
   ```
   python src/dataloader.py
   ```
   **Output**: Course_output_data.xlsx.
   Contains structured course design data simulated using Gemini AI, including fields such as Domain, Use Cases, Learners, Instructors, Learning Outcomes, etc.

   b. Extract keywords from course content
   ```
   python src/keyword_extraction.py
   ```
   **Output**: keyword_output_data.csv.
   Extracted thematic keywords for each field in the course framework using chain-of-thought prompting.

   c. Save embeddings for the extracted keywords 
   ```
   python src/search_embedding.py
   ```
   **Output**: output_embeddings.csv.
   A serialized file containing vector embeddings for each keyword, used to perform similarity-based filtering.

   d. Create clusters for the analysis of subtopics of main pillar for AI Teaching
      
      - **Domain**:
        ```
        python src/pages/clustering_domain.py
        ```
        **Output**: view_domain_clusters.csv
      - **Use Cases**:
         ```
        python src/pages/clustering_use_cases.py
         ```
         **Output**: view_use_cases.csv
      - **Data Type**:
        ```
        python src/pages/clustering_data.py
        ```
        **Output**: view_data_types.csv
      - **Implications**:
        ```
              python src/pages/implications/clustering_common_implications.py
              python src/pages/implications/clustering_domain_implications.py
              python src/pages/implications/clustering_courses_implications.py
        ```
        **Output**: view_implications.xlsx
      - **Learners**:
         ```
        python src/pages/clustering_learners.py
         ```
         **Output**: view_learners.xlsx
      - **Instructors**:
        ```
        python src/pages/clustering_instructors.py
        ```
        **Output**: view_instructors.xlsx
      - **Internal Support**:
        ```
        python src/pages/clustering_internal_support.py
        ```
        **Output**: view_internal_support.csv
      - **Assessment**:
        ```
        python src/pages/clustering_assessment.py
        ```
        **Output**: view_assessment.csv
      - **Learning Activity**:
        ```
        python src/pages/clustering_activities.py
        ```
        **Output**: view_activities.csv
   e. Edit or launch different pages of Streamlit web app
      - **Domain**:
        ```
        python src/pages/1_1_domain.py
        ```
      - **Use Cases**:
         ```
        python src/pages/1_2_use_cases.py
         ```
      - **Data Type**:
        ```
        python src/pages/1_3_data_types.py
        ```
      - **Implications**:
        ```
        python src/pages/implications/1_4_implications.py
        ```
      - **Learners**:
         ```
        python src/pages/2_1_learners.py
         ```
      - **Instructors**:
        ```
        python src/pages/2_2_instructorss.py
        ```
      - **Internal Support**:
        ```
        python src/pages/2_3_internal_support.py
        ```
      - **Assessment**:
        ```
        python src/pages/3_2_assessment.py
        ```
      - **Learning Activity**:
        ```
        python src/pages/3_3_activities.py
        ```
   
   f. Launch the Streamlit web app ((runs at http://localhost:8501/))
   ```
   python src/page_manager.py
   ```
   
