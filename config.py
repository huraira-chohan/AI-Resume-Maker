import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # FIXED: Force v1 API + stable model (avoids v1beta 404)
    client = genai.Client(api_version="v1")
    MODEL = genai.GenerativeModel("gemini-1.5-flash-002", client=client)
except Exception as e:
    st.error("Add GEMINI_KEY in Streamlit Secrets → aistudio.google.com/app/apikey")
    st.stop()
