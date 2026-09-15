import pdfplumber
import re
from .extractors import (
    extract_course,
    extract_semester,
    extract_instructor,
    extract_slo_blocks
)
from .utils import clean_text


def parse_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        raise Exception(f"Error Reading PDF: {str(0)}")

    #Extracting basic course info
    course = extract_course(full_text)
    semester = extract_semester(full_text)
    instructor = extract_instructor(full_text)

    #Extract SLO blocks 
    slo_blocks = extract_slo_blocks(full_text)

    if not slo_blocks:
        slo_blocks = extract_slo_blocks_alternative(full_text)

    #biuld rows for Excel

    rows = []
    for slo in slo_blocks:
        rows.append({
            'Course': course,
            'Semester': semester,
            'instructor': instructor,
            'Number': slo['number'],
            'Corslo': slo['corslo'],
            'PSLO': slo['pslo'],
            'McSLO': '',  # Not in this syllabus
            'CSLO': slo['cslo'],
            'GenEd Outcome': slo['gened']
        })
    return rows 

#Parse HTML syllabus file (still in production)
def parse_html(file_path):
    raise NotImplementedError("HTML parsing not implemented yet :()")

def extract_slo_blocks_alternative(text):
    slo_blocks = []

    pattern = r'(\d+)\.\s*(Students will be able to[^.]*\.)'
    matches = re.findall(pattern, text, re.DOTALL)

    for number, corslo in matches:
        slo_blocks.append({
            'number': number,
            'corslo': corslo,
            'cslo': '',
            'pslo': '',
            'gened': ''
        })

    return slo_blocks


