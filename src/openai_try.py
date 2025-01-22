from openai import OpenAI
import pandas as pd
import os, time

local_dir = os.path.abspath(os.path.join(__file__, "../../data/"))
raw_data_path = os.path.join(local_dir, "raw_data.csv")
output_data_path = os.path.join(local_dir, "output_data.csv")

# Set your OpenAI API key
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY', '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'))

# Load your CSV file
df = pd.read_csv(raw_data_path, encoding='ISO-8859-1', sep=';')

# Check if the column name exists
print("Columns in the CSV:", df.columns)




def extract_themes(text):
    
    if pd.isna(text):
        return "No text provided"
    
    prompt = f"Extract themes and summarize the main points from the following text:\n\n{text}\n\nSummarize as bullet points."

    response = client.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=500,
        n=1,
        temperature=0.5,
    )
    
    return response['choices'][0]['message']['content'].strip()
    
# Adjust your batch processing logic
batch_size = 10  # Customize as needed

# Create batches and process each batch
def process_batch(batch):
    return extract_themes("\n\n".join(batch))

df['Themes'] = df.groupby(df.index // batch_size)['Potential use cases'].transform(process_batch)


def extract_themes_with_retry(text, retries=5):
    for i in range(retries):
        try:
            return extract_themes(text)
        except client.error.RateLimitError:
            wait_time = 2 ** i  # Exponential backoff
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    return "API request failed after retries."

for i, chunk in enumerate(pd.read_csv('your_file.csv', chunksize=100)):
    chunk['Themes'] = chunk['Potential use cases'].apply(extract_themes_with_retry)
    chunk.to_csv(f'output_chunk_{i}.csv', index=False)
    print("Themes extracted and saved to CSV!")


# Save the updated CSV
# df.to_csv(output_data_path, index=False)

# print("Themes extracted and saved to CSV!")

# # Function to extract themes from a text
# def extract_themes(text):
#     if pd.isna(text):
#         return "No text provided"
    
#     prompt = f"Extract themes and summarize the main points from the following text:\n\n{text}\n\nSummarize as bullet points."
    
#     response = client.completions.create(
#         model="gpt-3.5-turbo",
#         prompt=prompt,
#         max_tokens=500,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
    
#     return response.choices[0].text.strip()