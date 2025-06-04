import os
import time
import pandas as pd
import google.generativeai as genai

# Path setup
local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
input_file = os.path.join(local_dir, "Course_output_data.xlsx")
df = pd.read_excel(input_file)

# Clean out rows without necessary data
df = df[['Cluster', '1.4 Implications of Using AI']].dropna()

# Get unique domains
domains = df['Cluster'].dropna().unique().tolist()

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.4,
    "top_p": 0.9,
    "top_k": 20,
    "max_output_tokens": 512,
    "response_mime_type": "text/plain",
}

# Create Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)



# Split combined domains and flatten into a clean unique list
domain_set = set()
for entry in df['Cluster'].dropna():
    split_domains = [d.strip() for d in entry.split(';')]
    domain_set.update(split_domains)

domains = sorted(domain_set)

# Store results
structured_data = []

# Loop through each domain
for domain in domains:
    prompt = f"""

For the domain: {domain} 

Based on typical AI usage, provide the following:
1. Ethical Implications
2. Legal Implications
3. Social Implications
4. Positive Examples
5. Negative Examples

Format the output like this:
Domain | Ethical Implications | Legal Implications | Social Implications | Positive Examples | Negative Examples

Example:
{domain} | Ethical1, Ethical2 | Legal1, Legal2 | Social1, Social2 | Positive1, Positive2 | Negative1, Negative2

Make sure to:
- Only output for this domain.
- Use commas `,` to separate points.
- Strictly avoid semicolons and never combine multiple domains.
- keep it clear and concise
"""


chat_session = model.start_chat(history=[])
response = chat_session.send_message(prompt)


lines = response.text.strip().split('\n')


data = []
for line in lines:
    if ':' in line:
        domain, "Ethical Implications", "Legal Implications", "Social Implications", "Positive Examples", "Negative Examples" = line.split('|', 1)
        domains = [d.strip() for d in domains_str.split(',')]
        data.append({'Implication': implication.strip(), 'Domains': ', '.join(domains)})


data = [line.split('|') for line in structured_data if '|' in line]


df = pd.DataFrame(data, columns=[
    "Domain", 
    "Ethical Implications", 
    "Legal Implications", 
    "Social Implications", 
    "Positive Examples", 
    "Negative Examples"
])

local_dir = os.path.abspath(os.path.join(__file__, "../../../../data/"))
output_file = os.path.abspath(os.path.join(local_dir, "views", "Structured_AI_Implications.xlsx"))

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name="AI_Implications")

print(f"Data saved to Excel at:\n{output_file}")
