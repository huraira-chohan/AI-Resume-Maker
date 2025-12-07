# utils.py — Beautiful, ATS-safe PDF using fpdf2
from fpdf import FPDF
from io import BytesIO

def generate_pdf(name, phone, email, linkedin, location, education, skills, bullets):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Name - Big & Bold
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(30, 64, 175)  # Blue
    pdf.cell(0, 15, name, ln=1, align="C")

    # Contact Info
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(100, 100, 100)
    contact = f"{phone} • {email}"
    if linkedin:
        contact += f" • {linkedin}"
    contact += f" • {location}"
    pdf.cell(0, 8, contact, ln=1, align="C")
    pdf.ln(10)

    # Section: Education
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(0, 10, "Education", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, education)
    pdf.ln(5)

    # Section: Skills
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(0, 10, "Technical Skills", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, skills)
    pdf.ln(5)

    # Section: Experience & Projects
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(0, 10, "Experience & Projects", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    for line in bullets.strip().split('\n'):
        if line.strip():
            bullet_text = line.strip().lstrip('•- ').strip()
            pdf.multi_cell(0, 8, f"• {bullet_text}")

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
