 # Thematic Analysis using Generative AI

As the adoption of Artificial Intelligence (AI) across various domains accelerates , it is important that AI education is thoughtfully structured and standardized. This tool is developed to analyze the AI Course Design Planning Frameworks[1] dataset. This framework provides structure for the development of domain-speciﬁc AI courses at the university level. In this tool we use Generative AI (Gemini) to automate thematic analysis. It extracts meaningful keywords, clusters data by domain, and visualizes thematic insights to support AI curriculum design and filtering.

## 📑 Table of Contents
1. Introduction
2. Problem statement and research questions
3. Methodology
4. Architecture
5. Setup Instructions
6. Usage (Web + Local)
7. Sample Results
8. Limitations & Future Work
9. Technologies Used
10. References

 
## 📢 Introduction 

### What is Thematic Analysis?

Qualitative data obtained during research cannot be analyzed in a mathematical way. Qualitative data can take many forms, including text, audio, video, and images. One could obtain this data from interviews, survey responses, group discussions, etc. This type of data goes beyond numbers conveying context, emotions and subtleties behind human behaviour, interactions and experiences. 

**Thematic analysis** is a method used to identifying recurring ideas, topics, or categories  in non-numerical data. This is a fundamental methods in Qualitative Data Analysis that can be employed in broad range of approaches (e.g., theoretical, conceptual, epistemological) effectively. 

Traditionally, thematic analysis can be performed manually for small volumes of data. However, for large volumes of data, approaches like machine learning techniques, including topic modeling, clustering, and deep learning are more effective. In this project we will take a look at how we can use **Generative AI models for Thematic analysis**.  

### AI Course Design Planning Framework

The AI Course Design Planning Framework, is a course planning framework to structure the development of domain-speciﬁc AI courses at the university level [1]. The framework has series of questions focusing application of AI in the domain, learning environment, course implementation and outcome. This framework bridges the gap between AI capabilities and domain-specific demands, enabling impactful and practical AI education. While answering these questions, it could be helpful for educators if they could view all the related frameworks with a simple search query. Also, use cases from one domain could spark new ideas for a different domain. 

Our project is inspired by the research work that highlights the need for customized AI courses across different domains. Each domain has it's unique learning goals, datasets, challenges and regulatory constraints. Designing AI courses using **domain-specific insights** ensures they’re more relevant and effective. 

To do this, we need to analyze the theme in each framework and extract keywords to be used for filtering through the data. With this project, we aim to streamline the thematic analysis process by integrating Generative AI, further enabling the automatic identification of key themes, generation of relevant keywords, and efficient filtering of data. The proposed framework addresses the challenges of managing large datasets and extracting actionable insights for educators, researchers, and stakeholders.


## 🎯 Problem Statement and Research questions

_**Perform thematic analysis to generate insights from qualitative data (AI Course Design planning framework) using Generative AI (GenAI)**_

This involves both understanding how to extract themes and how to make them actionable—by enabling interactive exploration or filtering. So we framed our investigation around three key research questions:

* How can Generative AI be applied to extract meaningful themes and keywords from a course design framework?
* How effectively can these keywords be used to support filtering and querying?
* How can AI-driven visualizations like spider charts and pie charts enhance interpretability?


## ⚙️ Methodology

Input: AI Course Design Planning Framework or Course criteria

Intermediate steps:
- Simulate and preprocess course frameworks with Gemini
- Perform thematic analysis to extract keywords
- Generate embeddings and set up filtering framework
- Group themes and visualize them in the form pie chart, stacked charts, etc.

Output: Streamlit app 

The process is visualized as seen here. 
![image](https://github.com/user-attachments/assets/c01a59b8-9bfb-4c29-8379-f70e75334d34)


## 🗂️ Architecture
The structure of the project can be explained as below:
```
├──  data/
|    ├── Course_output_data.xlsx   # Course Framework data in a single .xlsx file
|    ├── keywords_output_data.xlsx # Keywords file
|    ├── output_embeddings.xlsx    # Embeddings file
|    ├── course_files/             #  AI Course Design Planning Framework files in .txt format
|       ├── Aerospace.txt
|       ├── Agriculture.txt
|       ├── ...
|    ├── views/                   # Tables for views in Streamlit App 
|       ├── view_domain_clusters.py
|       ├── view_use_cases.py
|       ├── ...
|    ├── uploads/                 # Uploaded files will be saved here till being processed
|       ├── unzipped_files/
├──  src/
|    ├── pages/                    # Clustering + UI pages
|       ├── 1_1_domain.py           
|       ├── clustering_domain.py
|       ├── ...
|    ├── datagen.py                # Course simulation using Gemini
|    ├── dataloader.py             # Preprocess and save simulated data
|    ├── keyword_extraction.py     # Chain-of-thought keyword extraction
|    ├── save_embedding.py         # Embedding generation using Gemini Embed model
|    ├── search_embedding.py       # Search nearest neighbour with emebeding matching
|    ├── page_manager.py           # Streamlit entry point
|    └── config.ini                # Gemini API Key config
├──  README.md                     # Overview of the project
├──  User_guide.md                 # How to use the streamlit app 
└──  requirements.txt
```


## 🖥️ Setup Instructions

1. Clone the Repository
```
git clone https://github.com/darshina2/AI_Thematic_analysis.git
cd AI_Thematic_analysis
```
2. Create a Virtual Environment
```
python -m venv env
env\Scripts\activate      # or source env/bin/activate for Linux
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


## 📖 Usage

### Web Version:

Visit the live app: https://aithematicanalysis.streamlit.app/

The complete user-guide is available [here](https://github.com/darshina2/AI_Thematic_analysis/blob/master/User_guide.md). 

### Developer Version
In Developer mode, you can perform various tasks from simulation of course frameworks to visualizing this data on a streamlit app. 

1. Simulizing the data using Gemini
   ```
   python src/datagen.py
   ```
   **Output**: For eg., Aerospace.txt

   Generated a AI course design planning framework for AI in Aerospace simulated using Gemini AI, including fields such as Domain, Use Cases, Learners, Instructors, Learning Outcomes, etc.
    
2. Loading and preprocessing the data
   ```
   python src/dataloader.py
   ```
   **Output**: Course_output_data.xlsx.

   Saved all the frameworks in an excel file ready for Thematic Analysis.

3. Extract keywords from course content
   ```
   python src/keyword_extraction.py
   ```
   **Output**: keyword_output_data.csv.

   Extracted thematic keywords for each field in the course framework using chain-of-thought prompting.
   
4. Save embeddings for the extracted keywords 
   ```
   python src/save_embeddings.py
   ```
   **Output**: output_embeddings.csv.

   A serialized file containing vector embeddings for each keyword, used to perform similarity-based filtering.

5. Search similar frameworks
   ```
   python src/search_embedding.py
   ```
   **Output**: Table containing 

   A serialized file containing vector embeddings for each keyword, used to perform similarity-based filtering.
   
6.  Create clusters for the analysis of subtopics of main pillar for AI Teaching
      
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

        This process is repeated for all fields in the course frameworks.
        
 7.  Edit or launch different pages of Streamlit web app
      - **Domain**:
        ```
        streamlit run src/pages/1_1_domain.py
        ```
        
      - **Use Cases**:
         ```
        streamlit run src/pages/1_2_use_cases.py
         ```

         We created pages for all the remaining fields in the framework. 
        
8. Launch the Streamlit web app ((runs at http://localhost:8501/))
   ```
   streamlit run src/page_manager.py
   ```


## 📊 Sample Results

This tool was able to cluster the frameworks according to the domain, and further extract valuable insights related to use cases, learners, instructors and learning outcomes. For example, 
user can see that use case like Predictive maintenance is more relevant in Engineering and Technology domain than Design and creative arts. User can further know about positive and negative
implications of using AI in Medical domain. Semantic search, enabled with embeddings, helps user to search similar frameworks for reference or while creating new frameworks. Additionally, 
the user can compare different domains and how they could benefit from each other when it comes to applying AI. 

For example, 

![newplot](https://github.com/user-attachments/assets/f95f648a-65e2-42e5-adea-3985fb17a4a7)


## 🔴🟡🟢 Limitations and Future work
### Limitations
- In absence of real data, working with simulated data limited the scale of our analysis.
- Like any Gen AI tool, Gemini also is not immune to hallucinations.
- Also when data did not align naturally, it overgeneralize.

### Future Work
- Integration with Learning Management systems for curriculum design
- Enhanced human - AI interaction with instant feedback
- Multilingual and Cross-Cultural Thematic Analysis


## 🛠️ Technologies Used

- Gemini API (Generative AI)
- Streamlit (Web Interface)
- Python (Core scripts)
- Pandas, Regex (Data Processing)
- Gemini EMBED_MODEL = "models/text-embedding-004" (Embeddings)
- Gemini,Numpy, Plotly (Clustering and dimensionality reduction)


## 📜 References:
1. Schleiss, J.; Laupichler, M.C.; Raupach, T.; Stober, S. AI Course Design Planning Framework: Developing Domain-Specific AI Education Courses. Educ. Sci. 2023, 13, 954.
   https://doi.org/10.3390/educsci13090954
2. Katz, Andrew & Fleming, Gabriella & Main, Joyce. (2024). Thematic Analysis with Open-Source Generative AI and Machine Learning: A New Method for Inductive Qualitative Codebook Development. 10.48550/arXiv.2410.03721

3. Gamieldien, Yasir & Case, Jennifer & Katz, Andrew. (2023). Advancing Qualitative Analysis: An Exploration of the Potential of Generative AI and NLP in Thematic Coding. SSRN Electronic     Journal. 10.2139/ssrn.4487768

4. Gemini API documentation - https://ai.google.dev/gemini-api/docs
5. Streamlit documentation - https://docs.streamlit.io/

