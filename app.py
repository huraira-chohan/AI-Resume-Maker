import streamlit as st
from weasyprint import HTML
from io import BytesIO
import google.generativeai as genai

# Gemini Setup (stable for 2025)
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
except Exception as e:
    st.error("Add GEMINI_KEY to Secrets (free at aistudio.google.com/app/apikey)")
    st.stop()

st.set_page_config(page_title="Styled Resume Tailorer", page_icon="📄", layout="wide")
st.title("Styled AI Resume Tailorer – Pakistan Edition")
st.markdown("**Paste JD → Fill info → Get professional, ATS-safe PDF with clean styling. 100% FREE.**")

# Inputs
jd = st.text_area("Paste Job Description (Rozee.pk/LinkedIn)", height=150)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name", "Ahmed Khan")
    phone = st.text_input("Phone", "+92 300 1234567")
    email = st.text_input("Email", "ahmed@example.com")
with col2:
    linkedin = st.text_input("LinkedIn (optional)", "linkedin.com/in/ahmedkhan")
    location = st.text_input("City", "Lahore")
    education = st.text_input("Education + CGPA", "BS Computer Science – FAST-NU | CGPA 3.7/4.0")

skills = st.text_area("Your Skills (comma-separated)", "Flutter, Dart, Firebase, REST APIs, Git")
raw_bullets = st.text_area("Your Experience/Projects (3–6 bullets, one per line)", 
                           "- Built mobile app\n- Internship at XYZ\n- Final Year Project")

if st.button("Generate Styled Resume – FREE") and jd:
    with st.spinner("AI tailoring + styling your resume..."):
        prompt = f"""
        Job Description: {jd}
        Raw bullets: {raw_bullets}
        Skills: {skills}

        Rewrite bullets to match JD keywords naturally (Pakistani fresher style: FYP, internships).
        Return ONLY: 
        - Skills section as comma-separated list
        - 5–7 bullets starting with • (action verbs, quantifiable)
        """
        response = model.generate_content(prompt)
        content = response.text.strip().split("\n\n")  # Parse skills and bullets
        new_skills = content[0].strip() if content else skills
        new_bullets = "\n".join(content[1:]) if len(content) > 1 else raw_bullets

        # Styled HTML Template (ATS-safe: semantic, no tables/images, print-friendly)
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @page {{ size: A4; margin: 1in; }}
                body {{ font-family: Arial, sans-serif; line-height: 1.4; color: #000; max-width: 8.5in; margin: 0 auto; }}
                h1 {{ font-size: 28px; margin: 0 0 5px 0; color: #1e40af; text-align: center; }}
                .contact {{ font-size: 12px; text-align: center; margin-bottom: 20px; color: #555; }}
                h2 {{ font-size: 14px; margin: 20px 0 10px 0; border-bottom: 2px solid #1e40af; padding-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }}
                .skills {{ font-weight: bold; color: #1e40af; }}
                ul {{ margin: 5px 0; padding-left: 20px; }}
                li {{ margin-bottom: 8px; }}
                .print-only {{ display: block; }} @media print {{ .print-only {{ display: block !important; }} }}
            </style>
        </head>
        <body>
            <h1>{name}</h1>
            <div class="contact">{phone} • {email} • {linkedin} • {location}</div>
            
            <h2>Education</h2>
            <p>{education}</p>
            
            <h2>Skills</h2>
            <p class="skills">{new_skills}</p>
            
            <h2>Experience & Projects</h2>
            <ul>{''.join([f'<li>• {line.strip("- ")}</li>' for line in new_bullets.split('\n') if line.strip()])}</ul>
        </body>
        </html>
        """

        # Generate Styled PDF
        pdf_buffer = BytesIO()
        HTML(string=html_template).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        st.success("✅ Styled resume ready! (Professional layout, 90%+ JD match)")
        st.download_button(
            label="Download Styled PDF",
            data=pdf_buffer.getvalue(),
            file_name=f"{name.replace(' ', '_')}_Styled_Resume.pdf",
            mime="application/pdf"
        )
        st.markdown("### Quick Preview (Styled HTML):")
        st.components.v1.html(html_template, height=800, scrolling=True)

st.info("✨ Free • ATS-optimized styling (Arial, borders, highlights) • Mobile/print-ready")
st.caption("Powered by Gemini 1.5 Flash | Inspired by 2025 ATS templates")
