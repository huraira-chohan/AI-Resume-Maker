# config.py — FINAL WORKING VERSION (Dec 2025)
import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])

    # THIS IS THE ONLY MODEL THAT STILL WORKS ON FREE KEYS RIGHT NOW
    MODEL = genai.GenerativeModel("gemini-pro")

except Exception as e:
    st.error("Check your GEMINI_KEY in Secrets → https://aistudio.google.com/app/apikey")
    st.stop()
