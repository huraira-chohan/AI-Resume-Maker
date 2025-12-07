from weasyprint import HTML
from io import BytesIO

def generate_pdf(html_content) -> BytesIO:
    buffer = BytesIO()
    HTML(string=html_content).write_pdf(buffer)
    buffer.seek(0)
    return buffer
