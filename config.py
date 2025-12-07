import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # FIXED: Force v1 API to avoid v1beta deprecation 404s
    client = genai.Client(api_version="v1")
    # Use stable model supported in v1
    MODEL = genai.GenerativeModel("gemini-1.5-flash", client=client)
except Exception as e:
    st.error("Setup error: {e}. Check key at aistudio.google.com/app/apikey")
    st.stop()
