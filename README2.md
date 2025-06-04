 # Thematic Analysis with Generative AI

This tool helps design new AI courses within a given domain by leveraging thematic insights from previously designed courses across different domains. It performs thematic analysis to 
extract keywords from AI course design planning frameworks and enables flexible filtering using Generative AI.
 
## Introduction 

### What is Thematic Analysis?
During a research, we need to analyze either quantitative or qualitative data. Quantitative data, i.e., numerical data can be analyzed by various mathematical ways. Qualitative data can 
take many forms, including text, audio, video, and images. One could obtain this data from interviews, survey responses, group discussions, etc. This type of data goes beyond numbers conveying 
context, emotions and subtleties behind human behaviour, interactions and experiences. 

**Thematic analysis** is a method used to identifying recurring ideas, topics, or categories  in non-numerical data. It is a fundamental methods in QDA can be employed in broad range of 
approaches (e.g., theoretical, conceptual, epistemological) effectively. 

Traditionally, thematic analysis can be performed manually for small volumes of data. However, for large volumes of data, approaches like machine learning techniques, including topic modeling, 
clustering, and deep learning are more effective. In this project we will take a look at how we can use Generative AI models for Thematic analysis.  

### AI Course Design Planning Framework
The AI Course Design Planning Framework, is a course planning framework to structure the development of domain-speciﬁc AI courses at the university level [1]. The framework has series of 
questions focusing application of AI in the domain, learning environment, course implementation and outcome. This framework bridges the gap between AI capabilities and domain-specific demands,
enabling impactful and practical AI education. While answering these questions, it could be helpful for educators if they could view all the related frameworks with a simple search query. Also,
use cases from one domain could spark new ideas for a different domain. 

Our project is inspired by the research work that highlights the need for **customized AI courses across different domains**. Each domain has it's unique learning goals, datasets, challenges 
and regulatory constraints. Designing AI courses using **domain-specific insights** ensures they’re more relevant and effective. 

To do this, we need to analyze the theme in each answer and extract keywords to be used for filtering through the data. With this project, we aim to streamline the thematic analysis process
by integrating Generative AI, further enabling the automatic identification of key themes, generation of relevant keywords, and efficient filtering of data. The proposed framework addresses 
the challenges of managing large datasets and extracting actionable insights for educators, researchers, and stakeholders.

## Problem Statement and Research questions

_**Perform thematic analysis to generate insights from qualitative data (AI Course Design planning framework) using Generative AI (GenAI)**_

This involves both understanding how to extract themes and how to make them actionable—by enabling interactive exploration or filtering. So we framed our investigation around three key 
research questions:

* How can Generative AI be applied to extract meaningful themes and keywords from a course design framework?
* How effectively can these keywords be used to support filtering and querying?
* How can AI-driven visualizations like spider charts and pie charts enhance interpretability?

## Methodology

Input: AI Course Design Planning Framework or Course criteria

Intermediate steps:
- Simulate and preprocess course frameworks with Gemini
- Perform thematic analysis to extract keywords
- Generate embeddings and set up filtering framework
- Group themes and visualize them in the form pie chart, stacked charts, etc.

Outut: Streamlit app 

The process is visualized as seen here. 
![image](https://github.com/user-attachments/assets/c01a59b8-9bfb-4c29-8379-f70e75334d34)

## Architecture
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
src/
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
```

## Setup Instructions

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
5. Launch the Streamlit web app ((runs at http://localhost:8501/))
   ```
   streamlit run src/page_manager.py
   ```

## Usage

Web Version:

Visit the live app: https://aithematicanalysis.streamlit.app/

The complete user-guide is available here. 

## Sample Results

This tool 

## References:
1. Schleiss, J.; Laupichler, M.C.; Raupach, T.; Stober, S. AI Course Design Planning Framework: Developing Domain-Specific AI Education Courses. Educ. Sci. 2023, 13, 954.
2. https://doi.org/10.3390/educsci13090954

