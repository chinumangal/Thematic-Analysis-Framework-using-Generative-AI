import streamlit as st
import configparser
import google.generativeai as genai
import requests

generation_config = {
   "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 192,
    "response_mime_type": "text/plain",
}

# Streamlit Page Config
st.set_page_config(page_title="Thematic Analysis Tool", page_icon="📊", layout="centered")

# Title & Description
st.title("📊 Thematic Analysis Tool")
st.write("Welcome! This app helps you extract insights from text using AI.")


# Initialize ConfigParser
config = configparser.ConfigParser()

# Streamlit UI
st.title("🔑 API Key Setup")
st.write("Enter your Gemini API key to save it for future use.")

api_key = st.text_input("Enter API Key:", type="password")

def validate_api_key(api_key):
    API_VERSION = 'v1'
    api_url = f'https://generativelanguage.googleapis.com/{API_VERSION}/models?key={api_key}'
    
    response = requests.get(api_url, headers={'Content-Type': 'application/json'})
    
    # Verifica si hubo un error en la respuesta
    if response.status_code != 200:
        error_message = response.json().get('error', {}).get('message', 'Invalid API key')
        # raise Exception(error_message)
        return False
    else:
        return True


if st.button("Save API Key"):
    config["GEMINI"] = {"api_key": api_key}
    
    # Save to config.ini
    with open("config.ini", "w") as configfile:
        config.write(configfile)
        
    x = validate_api_key(api_key)

    if x == True:
        st.success("✅ API Key saved successfully!")
    else:
        st.warning("⚠️ API key is invalid. Please enter a valid Gemini API key.")