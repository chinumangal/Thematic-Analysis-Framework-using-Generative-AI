# Thematic Analysis and Filtering Framework Using Generative AI 

This tool helps you to design new AI course in a domain based on the previous courses in different domains. This can be used to perform thematic analysis to extract keywords from the course design framework to facilitate filtering using Generative AI.

1. Clone the Repository
```
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
4. Add API Key(in config.ini)
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
    python src/gemini.py
    ```
