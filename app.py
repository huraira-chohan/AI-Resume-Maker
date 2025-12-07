import streamlit as st
import google.generativeai as genai
from pypdf2 import PdfReader
from io import BytesIO
import weasyprint
import json
from datetime import date

# === CONFIG ===
genai.configure(api_key=st.secrets.get("GEMINI_KEY", "YOUR_KEY_HERE_IF_NOT_USING_SECRETS"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Free AI Resume Tailorer", page_icon="Resume")
st.title("Free AI Resume Tailorer (Pakistan Edition)")
st.markdown("**Instantly tailor your resume for Rozee.pk, Mustakbil.com, LinkedIn, Bayt & any Pakistani job** — 100% Free, No Limits, No Signup")

# Templates (clean, ATS-friendly, English)
templates = {
    "Tech Fresher (MERN, Flutter, Django, etc.)": """<!DOCTYPE html>
<html><head><style>
    body {font-family: Arial; margin: 2cm; line-height: 1.5; font-size: 11pt; color: #000;}
    h1 {font-size: 26pt; margin:0; color:#1e40af;}
    .contact {font-size:10pt; margin:10px 0; color:#555;}
    h2 {font-size:13pt; border-bottom:2px solid #1e40af; padding-bottom:4px; margin-top:25px;}
    ul {margin:8px 0; padding-left:20px;}
    li {margin-bottom:6px;}
    .highlight {font-weight:bold; color:#1e40af;}
</style></head><body>
    <h1>{{name}}</h1>
    <div class="contact">{{phone}} • {{email}} • {{linkedin}} • {{location}}</div>
    <h2>Technical Skills</h2><p class="highlight">{{skills}}</p>
    <h2>Experience & Projects</h2>{{experience_projects}}
    <h2>Education</h2><p>{{education}} <br> CGPA: {{cgpa}}</p>
</body></html>""",

    "Business / ACCA / Banking": """<!DOCTYPE html>
<html><head><style>
    body {font-family: Arial; margin: 2cm; line-height: 1.5; font-size: 11pt; color: #000;}
    h1 {font-size: 26pt; margin:0; color:#1e40af;}
    .contact {font-size:10pt; margin:10px 0; color:#555;}
    h2 {font-size:13pt; border-bottom:2px solid #1e40af; padding-bottom:4px; margin-top:25px;}
    ul {margin:8px 0; padding-left:20px;}
    li {margin-bottom:6px;}
    .highlight {font-weight:bold; color:#1e40af;}
</style></head><body>
    <h1>{{name}}</h1>
    <div class="contact">{{phone}} • {{email}} • {{linkedin}} • {{location}}</div>
    <h2>Professional Skills</h2><p class="highlight">{{skills}}</p>
    <h2>Experience & Internships</h2>{{experience_projects}}
    <h2>Education & Certifications</h2><p>{{education}}<br>{{certifications}}</p>
</body></html>""",

    "General / Entry-Level": """<!DOCTYPE html>
<html><head><style>
    body {font-family: Arial; margin: 2cm; line-height: 1.5; font-size: 11pt; color: #000;}
    h1 {font-size: 26pt; margin:0; color:#1e40af;}
    .contact {font-size:10pt; margin:10px 0; color:#555;}
    h2 {font-size:13pt; border-bottom:2px solid #1e40af; padding-bottom:4px; margin-top:25px;}
    ul {margin:8px 0; padding-left:20px;}
    li {margin-bottom:6px;}
    .highlight {font-weight:bold; color:#1e40af;}
</style></head><body>
    <h1>{{name}}</h1>
    <div class="contact">{{phone}} • {{email}} • {{linkedin}} • {{location}}</div>
    <h2>Key Skills</h2><p class="highlight">{{skills}}</p>
    <h2>Experience & Projects</h2>{{experience_projects}}
    <h2>Education</h2><p>{{education}} <br> CGPA: {{cgpa}}</p>
</body></html>"""
}

# UI
col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("Paste the full Job Description here", height=180)
with col2:
    resume_file = st.file_uploader("Upload your current resume (PDF)", type="pdf")
    template = st.selectbox("Choose your template", list(templates.keys()))

if st.button("Generate Tailored Resume – 100% FREE") and jd and resume_file:
    with st.spinner("AI is tailoring your resume..."):
        try:
            # Read old resume
            reader = PdfReader(resume_file)
            old_text = "".join([p.extract_text() or "" for p in reader.pages])

            # Gemini magic
            prompt = f"""
            You are an expert resume writer for Pakistani jobs.
            Job Description: {jd}
            Current Resume Text: {old_text}

            1. Extract as clean JSON only:
            {{
              "name": "...",
              "phone": "...",
              "email": "...",
              "linkedin": "...",
              "location": "e.g. Lahore, Karachi, Islamabad",
              "skills": "Python, React, Node.js, ...",
              "education": "BSCS from NUST, 2025",
              "cgpa": "3.8/4.0",
              "certifications": "ACCA Part 1, etc.",
              "experience_projects": "<ul><li>Bullet 1</li><li>Bullet 2</li></ul>"
            }}

            2. Rewrite every bullet in experience_projects to perfectly match the job description keywords naturally.
            3. Return ONLY valid JSON. No extra text.
            """
            response = model.generate_content(prompt)
            data = json.loads(response.text.strip("```json").strip("```"))

            # Fill template
            html = templates[template]
            for key, value in data.items():
                html = html.replace(f"{{{{{key}}}}}", str(value or ""))

            # Generate PDF
            pdf = weasyprint.HTML(string=html).write_pdf()

            st.success("Your perfect resume is ready!")
            st.download_button(
                label="Download Tailored Resume (PDF)",
                data=pdf,
                file_name=f"{data.get('name','Resume')}_Tailored.pdf",
                mime="application/pdf"
            )
            st.balloons()

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.caption("Completely free • No login • No limits • Built with love for Pakistani job seekers")
st.markdown("Made with Gemini 1.5 Flash • Works on mobile too")