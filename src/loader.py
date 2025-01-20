# src/loader.py
import pandas as pd

# Load the CSV file
def load_csv(file_path):
    return pd.read_csv(file_path, encoding='ISO-8859-1', sep=';')

# Save themes back to CSV
def save_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)
