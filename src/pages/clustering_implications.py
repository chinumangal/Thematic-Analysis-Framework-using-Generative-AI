import os
import time
import pandas as pd
import google.generativeai as genai

# Load Excel data
local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
input_file = os.path.join(local_dir, "Course_output_data.xlsx")
df = pd.read_excel(input_file)

# Extract lists
domains = df['Cluster'].dropna().unique().tolist()
implications = df['1.4 Implications of Using AI'].dropna().unique().tolist()

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.4,
    "top_p": 0.9,
    "top_k": 20,
    "max_output_tokens": 512,
    "response_mime_type": "text/plain",
}

# Prompt for common Implications across domains
prompt = f"""
You are an expert in Artificial Intelligence impact analysis.

Given the following domains:
{domains}

And the following AI implications:
{implications}

Your tasks:
1. Identify at least 10 common AI implications that affect multiple domains.
2. For each implication, list which domains it affects most — but:
   - Do not repeat the same domain name.
   - Separate domains only using commas.
   - Return output only in this format:

Implication: Domain1, Domain2, Domain3

Example:
Algorithmic Bias: Medical & Health Sciences, Business & Economics, Social Sciences & Humanities

Please strictly follow this format. Avoid semicolons, avoid duplicate domain names.  
"""

# Initialize Gemini Model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Start the chat session
chat_session = model.start_chat(history=[])
response = chat_session.send_message(prompt)
print(response.text)

# Split into lines
lines = response.text.strip().split('\n')

# Create a list of dictionaries
data = []
for line in lines:
    if ':' in line:
        implication, domains_str = line.split(':', 1)
        domains = [d.strip() for d in domains_str.split(',')]
        data.append({'Implication': implication.strip(), 'Domains': ', '.join(domains)})

# Save to DataFrame
output_df = pd.DataFrame(data)

# Or save to Excel
output_file = os.path.join(local_dir, "AI_Implications_Domains.xlsx")

with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
    output_df.to_excel(writer, sheet_name="Common Implications", index=False)
