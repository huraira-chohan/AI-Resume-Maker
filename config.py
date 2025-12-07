import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import time
import random

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    MODEL = genai.GenerativeModel("gemini-2.0-flash")  # Stable model
except Exception as e:
    st.error(f"Setup error: {e}. Check key at aistudio.google.com/app/apikey")
    st.stop()

# Add retry decorator for generate_content
def with_retry(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except ResourceExhausted:
                if attempt < max_retries - 1:
                    wait = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
                    time.sleep(wait)
                    continue
                raise
    return wrapper

MODEL.generate_content = with_retry(MODEL.generate_content)
