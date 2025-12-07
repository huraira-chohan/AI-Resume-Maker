import streamlit as st
from fpdf import FPDF
from io import BytesIO

# === GEMINI SETUP (the only working way in Dec 2025) ===
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # This model name WORKS 100% right now
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("Add your Gemini API key in Secrets → GEMINI_KEY (get free at aistudio.google.com/app/apikey)")
    st.stop()

# === UI ===
st.set_page_config(page_title="Free Resume Tailorer", page_icon="Resume")
st.title("Free AI Resume Tailorer – Pakistan Edition")
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
                       "• Built mobile app\n• Internship at XYZ\n• Final Year Project")

if st.button("Generate Perfect Resume – FREE") and jd:
    with st.spinner("Tailoring your resume..."):
        prompt = f"""
        Job Description: {jd}
        Current bullets: {bullets}
        Skills: {skills}

        Rewrite the bullets to match the job description perfectly (natural language).
        Return ONLY 5–7 bullet points starting with •
        """
        try:
            response = model.generate_content(prompt)
            new_bullets = response.text.strip()
        except Exception as e:
            st.error(f"Gemini error: {e}")
            new_bullets = bullets  # fallback

        # === PDF ===
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 12, name, ln=1, align="C")
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 8, f"{phone} • {email} • {linkedin} • {location}", ln=1, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "B", 13); pdf.cell(0, 10, "Education", ln=1)
        pdf.set_font("Arial", size=11); pdf.multi_cell(0, 8, education)

        pdf.set_font("Arial", "B", 13); pdf.cell(0, 10, "Skills", ln=1)
        pdf.set_font("Arial", size=11); pdf.multi_cell(0, 8, skills)

        pdf.set_font("Arial", "B", 13); pdf.cell(0, 10, "Experience & Projects", ln=1)
        pdf.set_font("Arial", size=11); pdf.multi_cell(0, 8, new_bullets)

        pdf_bytes = BytesIO()
        pdf.output(pdf_bytes)
        pdf_bytes.seek(0)

        st.success("Done! Your perfect resume is ready")
        st.download_button(
            "Download PDF Resume",
            data=pdf_bytes.getvalue(),
            file_name=f"{name.replace(' ', '_')}_Resume.pdf",
            mime="application/pdf"
        )
        st.balloons()

st.caption("100% free • No PDF upload • Works every time • Made for Pakistani freshers")
