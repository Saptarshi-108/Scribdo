from langdetect import detect
from fpdf import FPDF
import uuid
import os

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"
    
def generate_pdf(summary, lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Consolas", size=12)
    pdf.multi_cell(0, 10, f"Language: {lang}\n\nSummary:\n\n{summary}")
    pdf_path = os.path.join("temp", f"{uuid.uuid4()}.pdf")
    pdf.output(pdf_path)
    return pdf_path
