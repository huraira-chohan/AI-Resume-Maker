# utils.py — Safe PDF generation using fpdf2 (works 100% on Streamlit Cloud)
from fpdf import FPDF
from io import BytesIO

def generate_pdf(name, phone, email, linkedin, location, education, skills, bullets):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, name, ln=1, align="C")
    pdf.set_font("Arial", size=11)
    contact = f"{phone} • {email}"
    if linkedin:
        contact += f" • {linkedin}"
    contact += f" • {location}"
    pdf.cell(0, 10, contact, ln=1, align="C")
    pdf.ln(10)

    # Education
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Education", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, education)
    pdf.ln(5)

    # Skills
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Technical Skills", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, skills)
    pdf.ln(5)

    # Experience & Projects
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Experience & Projects", ln=1)
    pdf.set_font("Arial", size=11)
    for bullet in bullets.strip().split('\n'):
        if bullet.strip():
            pdf.multi_cell(0, 8, f"• {bullet.strip('• - ')}")

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
