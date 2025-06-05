## User Guide - Thematic Analysis using Generative AI

This document is designed to help you navigate the Thematic Analysis using  Generative AI (GenAI), a Streamlit Web App develped to visualize the insights from AI Couse Design Planning Frameworks
dataset.  

This tool is available at 🔗 - https://aithematicanalysis.streamlit.app/, 

or you can run it locally by following [README.md](https://github.com/darshina2/AI_Thematic_analysis/blob/master/README.md) 

### 1. Homepage Overview

When you open this tool, you will land on Homepage. On the left navigation bar, you will see the different sections of this tool. The main area displays the selected content. 

----------
![image](https://github.com/user-attachments/assets/3272c99e-e67c-4fad-8a69-9913a889a501)

----------

To access certain functionalities of this tool, you will need to have [Gemini API key](https://aistudio.google.com/apikey). Enter your Gemini API key to save it for future use.

Let's go through all pages in detail:

### 2. Load data

This page is designed so that user can upload new frameworks to the existing data. Here, the user can upload a zip file containing all his frameworks in a .txt format in a single go. These 
frameworks once uploaded will be temporarly saved at "data/uploads/unzipped_files". We can use buttons under "Save and Process data" for next steps.

----------
![image](https://github.com/user-attachments/assets/a7f7f70d-607a-4387-be80-0eb18b0d7399)
 
----------

- Save Data to Excel: Loads all files and preprocess them to save in excel file
- Get Keywords: Generate keywords and append to the existing data
- Generate embeddings: Add emebeddings for new data


### 3. Domain     

This page gives us the overview of domain distribution of the courses. With the help of Gemini, we have tried to figure out the domain that the course belongs. Looking at the multidisciplinary 
structure of some courses, a course can be classified into 2 domains at the maximum. We can visualize this in the form of pie-chart. 

----------
![image](https://github.com/user-attachments/assets/1c03b596-4fe0-4649-a35d-6a2512cc0614)

----------
We can also view the detailed information of the courses in a particular domain in a table format. 

----------
![image](https://github.com/user-attachments/assets/87e8b3b1-ff4f-46b4-94ce-58b9bcbea477)

----------

### 4. Use cases

This page explores the impact of AI technology on various domains, identifying current use cases and predicting future potential applications for AI in problem-solving domain-specific issues.

Here, you can view similar frameworks based on the use case:

----------
![image](https://github.com/user-attachments/assets/e00914dc-8b49-41d6-906f-9b1fa1a38db1)

----------
Or view all the courses based on the use cases. For example, I can view all the course frameworks where Quality control can be used:

----------
![image](https://github.com/user-attachments/assets/00cb5085-b07d-49ed-913f-7dae90ac415c)

----------
In the third tab, relevance in domains, the domains are ranked in descending order of relevance for each AI use case. 

----------
![image](https://github.com/user-attachments/assets/fbc83e08-b0b4-4969-83c9-2b46858283ad)

----------

### 5. Types of data

AI use cases are based on the most relevant data type in a domain, allowing for targeted use of AI techniques. Understanding typical data in a domain, such as time-series data, texts, images, 
and abundant or scarce data, significantly impacts the effectiveness of AI techniques.

In this page, the user can see the distribution of data types present. 

----------
![image](https://github.com/user-attachments/assets/18d74587-7777-444b-b5f7-443f1dd441cd)

----------
In the second tab, we will see the distribution across different domains. It gives us an idea, what type of data is most present to facilitate the use of AI. 

----------
![image](https://github.com/user-attachments/assets/ad4837ae-ebbd-4879-89b0-0eddc9f40466)

----------

### 6. Implications

There are potential implications that could arise when using AI in the respective field. This mostly concerns ethical, legal and social implications across different domains and courses.
We first see the domains most affected by each implication. 

----------
![image](https://github.com/user-attachments/assets/4abf4f45-7b95-49e5-bf4d-39b97de63827)

----------
Then in the second tab, we see the types of implications and their impact on each domain. 

----------
![image](https://github.com/user-attachments/assets/495d7030-d963-4b01-a56a-d83f0dbcad24)

----------
We can also this at individual course level on the third tab here. 


### 7. Learners

Three considerations are important for domain-specific AI courses for learners. First is to understand which AI skills and related competencies. Second, it is important to clarify the role 
of the group of learners regarding their interaction with AI to choose relevant demonstrations of AI-applications and an appropriate level of difficulty. Third, the existing competencies and 
the future role are influenced by the curricular integration of the course in an overall program.

In this page, we can see the stacked chart showing the distribution of type of learners in each domain. 

----------
![image](https://github.com/user-attachments/assets/4598ee5d-06fd-499e-a184-11427860c711)

----------

### 8. Instructors

Domain-specific AI teaching requires a mix of sufficient AI knowledge, domain expertise and pedagogical skills to teach an interdisciplinary course as well as the motivation and time from an
instructor’s perspective.

In this page, we can see the stacked chart showing the distribution of type of instructors in each domain. 

----------
![image](https://github.com/user-attachments/assets/f284ccce-6955-4b90-9785-304a3fb85c87)

----------

### 9. Internal support

Internal support, including budget, personnel restraints, course duration, data, software, and hardware, can be seen as resources or limitations in AI teaching. Instructor support, institutional barriers, and student support also impact course design. In this page, we visualize it in the form of spider chart. For each domain, we obtain rating on categories like budget, personnel, data availability, etc. on the scale of 1-5. 

----------
![image](https://github.com/user-attachments/assets/5598991f-d335-4a0c-be2e-60f37dc47ae4)

----------

### 10. Assessment

The Constructive Alignment approach emphasizes the importance of evaluating learning objectives in interdisciplinary courses. This includes balancing the experiences of different groups 
and the targeted outcomes. Traditional assessment methods, project- or problem-based assessments, and reflection can help bridge disciplinary silos. Using different assessment components 
can be beneficial and fair.

Here, similar to Internal support, we rate all domains on categories like Quizzes, Group activities, Individual assignments, etc. 

----------
![image](https://github.com/user-attachments/assets/67b9e440-0697-48b2-9ac4-2354ac5a6df0)

----------

### 11. Learning Activities

The final step involves implementing learning activities to achieve desired objectives, focusing on pedagogical implementation of course design. Merrill principles of learning are considered, 
and domain-specific AI courses often use a combination of teaching methods. This overview forms the basis for detailed planning, including AI-based activities.

Here, similar to Internal support, we rate all domains on categories like activation, problem centered, teaching activities, etc. 

----------
![image](https://github.com/user-attachments/assets/9bdbc2f1-9672-4294-9821-556da3d9c30a)

----------


You are now ready to explore Thematic Analysis tool using GenAI. We hope this tool helps you while designing new curriculia or exploring thematic insights in course framework data. 
Happy exploring!
