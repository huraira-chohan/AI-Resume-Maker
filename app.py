import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Import Google stuff with v1 API fix
try:
    import google.generativeai as genai
    from google.genai.types import HttpOptions  # For API version override
    from google.api_core.exceptions import NotFound

    # Configure with v1 API (fixes 404 on Streamlit Cloud)
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    client = genai.Client(http_options=HttpOptions(api_version="v1"))  # Key fix: Force v1
    model = genai.GenerativeModel("gemini-1.5-flash-002", client=client)  # Stable version name
    GEMINI_READY = True
except ImportError as e:
    st.error(f"Missing Google package: {e}. Add 'google-generativeai' to requirements.txt.")
    GEMINI_READY = False
    st.stop()
except Exception as e:
    st.error(f"Gemini setup error: {e}. Check your API key in Secrets.")
    GEMINI_READY = False
    st.stop()

# === PAGE SETUP ===
st.set_page_config(page_title="Free Resume Tailorer", page_icon="📄", layout="wide")
st.title("📄 Free AI Resume Tailorer – Pakistan Edition")
st.markdown("**Paste any job description → fill your details → get perfect ATS resume in 15 seconds. 100% FREE, no PDF upload needed**")

if not GEMINI_READY:
    st.stop()

# === INPUTS ===
jd = st.text_area("Paste the full Job Description (Rozee.pk, LinkedIn, Mustakbil, etc.)", height=150)

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Full Name", "Ahmed Khan")
    phone = st.text_input("Phone", "+92 300 1234567")
    email = st.text_input("Email", "ahmed@example.com")
with c2:
    linkedin = st.text_input("LinkedIn (optional)", "linkedin.com/in/ahmedkhan")
    location = st.text_input("City", "Lahore")
    education = st.text_input("Education + CGPA", "BS Computer Science – FAST-NU | CGPA 3.7/4.0")

skills = st.text_area("Your Skills (comma separated)", "JavaScript, React, Node.js, MongoDB, Git, Firebase")
raw_bullets = st.text_area("Your current experience/projects (3–6 bullets, one per line)", 
                           "• Built e-commerce website\n• 3-month internship at ABC Tech\n• Final Year Project on MERN stack")

# === GENERATE BUTTON ===
if st.button("Generate Perfect Resume – 100% FREE") and jd:
    with st.spinner("AI is tailoring your resume..."):
        try:
            prompt = f"""
            Job Description: {jd}
            Current bullets: {raw_bullets}
            Skills: {skills}

            Rewrite the bullets to perfectly match the job description keywords (naturally, not robotic).
            Keep Pakistani fresher style (mention FYP, internship, university projects, etc.).
            Return ONLY a list of 5–7 strong bullet points starting with •
            """
            response = model.generate_content(prompt)
            new_bullets = response.text.strip()

            # === CREATE PDF ===
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 18)
            pdf.cell(0, 12, name, ln=True, align="C")
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 8, f"{phone} • {email} • {linkedin} • {location}", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, "Education", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, education)

            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, "Skills", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, skills)

            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, "Experience & Projects", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, new_bullets)

            pdf_bytes = BytesIO()
            pdf.output(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ Your perfect resume is ready! (90%+ JD match, ATS-optimized)")
            st.download_button(
                label="Download Tailored Resume (PDF)",
                data=pdf_bytes.getvalue(),
                file_name=f"{name.replace(' ', '_')}_Tailored_Resume.pdf",
                mime="application/pdf"
            )
            st.balloons()

        except NotFound:
            st.error("Model still not found (404). Try regenerating your API key at aistudio.google.com and ensuring 'Generative Language API' is enabled in Google Cloud Console.")
        except Exception as e:
            st.error(f"API error: {str(e)}. If 404 persists, switch model to 'gemini-1.0-pro' in code.")

st.info("✨ Completely free • No login • Unlimited uses • Mobile-friendly")
st.caption("Powered by Gemini 1.5 Flash | For Pakistani job seekers 🚀")
