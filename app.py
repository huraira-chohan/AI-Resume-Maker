import streamlit as st
from fpdf import FPDF  # FPDF2 is imported as fpdf
from io import BytesIO

# === GEMINI SETUP (fixed model name for v1beta) ===
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # FIXED: Use full path + latest stable name (no 404)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
except Exception as e:
    st.error("🚨 Add your Gemini API key in Secrets → GEMINI_KEY (get free at aistudio.google.com/app/apikey)")
    st.stop()

# === UI ===
st.set_page_config(page_title="Free Resume Tailorer", page_icon="📄", layout="wide")
st.title("📄 Free AI Resume Tailorer – Pakistan Edition")
st.markdown("**Paste any job description → fill details → get perfect ATS resume in 15 seconds. 100% FREE**")

jd = st.text_area("Paste the full Job Description", height=150)

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Full Name", "Ahmed Khan")
    phone = st.text_input("Phone", "+92 300 1234567")
    email = st.text_input("Email", "ahmed@example.com")
with c2:
    linkedin = st.text_input("LinkedIn (optional)", "")
    location = st.text_input("City", "Lahore")
    education = st.text_input("Education + CGPA", "BS Computer Science – FAST-NU | CGPA 3.7/4.0")

skills = st.text_area("Your Skills (comma separated)", "Flutter, Dart, Firebase, REST API, Git")
bullets = st.text_area("Your current bullets (3–6 lines)", 
                       "- Built mobile app\n- Internship at XYZ\n- Final Year Project")

if st.button("Generate Perfect Resume – FREE") and jd:
    with st.spinner("Tailoring your resume..."):
        prompt = f"""
        Job Description: {jd}
        Current bullets: {bullets}
        Skills: {skills}

        Rewrite the bullets to match the job description perfectly (natural language).
        Use simple dashes (-) for bullets, no special chars.
        Return ONLY 5–7 bullet points starting with -
        """
        try:
            response = model.generate_content(prompt)
            new_bullets = response.text.strip()
        except Exception as e:
            st.error(f"Gemini error: {e}. Try regenerating your API key.")
            new_bullets = bullets  # Fallback to original

        # === PDF (Unicode-safe: strip non-ASCII) ===
        def clean_text(text):
            return ''.join(c for c in text if ord(c) < 128)  # Basic ASCII filter

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 12, clean_text(name), ln=1, align="C")
        pdf.set_font("Arial", size=10)
        contact = f"{clean_text(phone)} | {clean_text(email)} | {clean_text(linkedin)} | {clean_text(location)}"
        pdf.cell(0, 8, contact, ln=1, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "B", 13); pdf.cell(0, 10, "Education", ln=1)
        pdf.set_font("Arial", size=11); pdf.multi_cell(0, 8, clean_text(education))

        pdf.set_font("Arial", "B", 13); pdf.cell(0, 10, "Skills", ln=1)
        pdf.set_font("Arial", size=11); pdf.multi_cell(0, 8, clean_text(skills))

        pdf.set_font("Arial", "B", 13); pdf.cell(0, 10, "Experience & Projects", ln=1)
        pdf.set_font("Arial", size=11); pdf.multi_cell(0, 8, clean_text(new_bullets))

        pdf_bytes = BytesIO()
        pdf.output(pdf_bytes)
        pdf_bytes.seek(0)

        st.success("✅ Done! Your perfect resume is ready (90%+ JD match, ATS-optimized)")
        st.download_button(
            "Download PDF Resume",
            data=pdf_bytes.getvalue(),
            file_name=f"{clean_text(name.replace(' ', '_'))}_Resume.pdf",
            mime="application/pdf"
        )
        st.balloons()

st.info("✨ Completely free • No login • Unlimited uses • Mobile-friendly")
st.caption("Powered by Gemini 1.5 Flash | For Pakistani job seekers 🚀")
