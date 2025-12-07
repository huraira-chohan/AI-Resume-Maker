import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    MODEL = genai.GenerativeModel("models/gemini-1.5-flash-latest")
except Exception:
    st.error("Add GEMINI_KEY in Streamlit Secrets → aistudio.google.com/app/apikey")
    st.stop()
