# from transformers import pipeline
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from accelerate import init_empty_weights, infer_auto_device_map
import torch
import pandas as pd
from loader import load_csv, save_csv
import os, time
from os import walk


print("hello")
local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../"))
raw_data_path = os.path.abspath(os.path.join(local_dir,"data/raw_data.csv"))
model_path = os.path.join(local_dir , "mistral")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Load the tokenizer and model from the local path
tokenizer = AutoTokenizer.from_pretrained(model_path)
# Initialize model with empty weights to reduce memory usage
with init_empty_weights():
    model = AutoModelForCausalLM.from_pretrained(model_path)

# Infer a device map and offload to disk
device_map = infer_auto_device_map(model, max_memory={"cpu": "8GB"}, no_split_module_classes=["BloomBlock"])
model = model.from_pretrained(model_path, device_map=device_map, offload_folder="./offload")
# Set up the pipeline
theme_extractor = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Test the model
text = "Practical use cases are already cropping up across all stages of the TV and film production process. These include story development, storyboarding/animatics, pre-visualization (or “previs”), B-roll, editing, visual effects (VFX) and localization services."

# Extract themes
response = theme_extractor(
    f"Extract and list the main themes from the following text. Please format the response as bullet points:\n\n{text}",
    max_length=200,
    truncation=True
)

# Print the response
print("Response: ", response[0]['generated_text'])


# theme_extractor = pipeline("text-generation", model="bigscience/bloom-560m")
# text = "Practical use cases are already cropping up across all stages of the TV and film production process. These include story development, storyboarding/animatics, pre-visualization (or “previs”), B-roll, editing, visual effects (VFX) and localization services."
# response = theme_extractor(f"Extract the key themes from the following text and present them as bullet points:\n\n{text}\n\n- ", max_length=100, truncation=True)


# print("Response: ", response)

# try:
#     print("Attempting to load Mistral model...")
#     theme_extractor = pipeline("text-generation", model="mistralai/Mistral-7B-v0.1", use_auth_token="abc")
#     print('Mistral 7B connected')
# except Exception as e:
#     print(f"Error with Mistral: {e}")
#     print("Switching to Bloom...")
#     theme_extractor = pipeline("text-generation", model="bigscience/bloom-560m")
#     print('Bloom connected')

# # Check if the pipeline is loaded
# print("Pipeline loaded. Testing the model...")

# text = "The project focuses on AI advancements in healthcare."
# start_time = time.time()
# response = theme_extractor(f"Extract themes from the following text: {text}", max_length=100)

# # Track how long the inference takes
# print(f"Model inference took {time.time() - start_time:.2f} seconds")

# # Ensure that you are receiving a response
# if response:
#     print(response[0]['generated_text'])
# else:
#     print("No response received.")


# # Load the CSV
# local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../data/"))
# raw_data_path = os.path.join(local_dir,"raw_data.csv")
# output_data_path = os.path.join(local_dir, "output.csv")

# df = load_csv(raw_data_path)

# data_columns = ['Domain', 'Potential use cases']

# for col in data_columns:
#     themes = []
#     for text in df[col].fillna(''):  # Handle missing values
#             if text.strip():  # Skip empty rows
#                 response = theme_extractor(f"Extract themes from the following text: {text}", max_length=100)
#                 themes.append(response[0]['generated_text'])
#                 print(themes[0])
#             else:
#                 themes.append('')
        
#         # Add the themes as a new column
#     df[f'{col}_themes'] = themes

# # Save the updated CSV
# save_csv(df, 'data/output.csv')

# print("Themes extracted and saved to output.csv")
