import streamlit as st
from config import MODEL
from prompts import get_resume_prompt
from templates import get_styled_html
from utils import generate_pdf

st.set_page_config(page_title="PakResume AI", page_icon="Resume", layout="centered")
st.title("PakResume AI — Professional & Styled")
st.markdown("**Best resume tailorer for Pakistani freshers. Free. Beautiful. Actually works.**")

jd = st.text_area("Paste Job Description", height=140)

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Name", "Ahmed Khan")
    phone = st.text_input("Phone", "+92 300 1234567")
    email = st.text_input("Email", "ahmed@example.com")
with c2:
    location = st.text_input("City", "Lahore")
    linkedin = st.text_input("LinkedIn (optional)", "")
    education = st.text_input("Education", "BS CS – FAST-NU | CGPA 3.7")

skills = st.text_area("Your Skills", "Flutter, Dart, Firebase, REST API, Git, Provider")
bullets = st.text_area("Your Raw Bullets (one per line)", "Built mobile app\nDid internship\nFinal Year Project")

if st.button("Generate Professional Resume", type="primary") and jd:
    with st.spinner("Creating your perfect resume..."):
        prompt = get_resume_prompt(jd, bullets, skills)
        response = MODEL.generate_content(prompt)
        new_bullets = response.text.strip()

        html = get_styled_html(name, phone, email, linkedin, location, education, skills, new_bullets)
        pdf_buffer = generate_pdf(html)

        st.success("Done! Here's your beautiful resume")
        st.download_button(
            "Download Styled PDF",
            data=pdf_buffer.getvalue(),
            file_name=f"{name.replace(' ', '_')}_Resume.pdf",
            mime="application/pdf"
        )
        st.balloons()

st.caption("Free • Professional design • ATS-safe • Made for Pakistani job market")
