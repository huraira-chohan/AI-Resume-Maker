# config.py
import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import time
import random

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    
    # THIS MODEL WORKS RIGHT NOW (Dec 2025)
    MODEL = genai.GenerativeModel("gemini-1.5-flash")

    # Add automatic retry for 429 quota errors
    original_generate = MODEL.generate_content

    def generate_with_retry(*args, **kwargs):
        for attempt in range(4):  # 4 attempts total
            try:
                return original_generate(*args, **kwargs)
            except ResourceExhausted:
                if attempt == 3:
                    raise
                wait = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait)
        return original_generate(*args, **kwargs)

    MODEL.generate_content = generate_with_retry

except Exception as e:
    st.error("Check your GEMINI_KEY in Secrets → https://aistudio.google.com/app/apikey")
    st.stop()
