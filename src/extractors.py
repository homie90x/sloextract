import re
from .config import *
from .utils import clean_text, safe_extract, extract_field

#Extract Course code (for example, CSCI 1101) from syllabus text.
def extract_course(text):
    match = re.search(COURSE_PATTERN, text)
    if match:
        course = match.group(1).strip()
        parts = course.split()
        if len(parts) == 2:
            return parts[0].upper() + " " + parts[1]
        return course.upper()
    return ""


def extract_semester(text):
    match = re.search(SEMESTER_PATTERN, text)
    if match:
        semester = match.group(1).capitalize()
        year = match.group(2)
        return f"{semester} {year}"
    return ""

#extracting instructor name.
def extract_instructor(text):
    # Trying different patterns because of the wide variety
    patterns = [
        r'Instructor\s*(?::)?\s*([A-Za-z\s.]+?)(?:\n|Email|Office|Phone)',
        r'Professor\s*(?::)?\s*([A-Za-z\s.]+?)(?:\n|Email|Office|Phone)',
        r'Instructor\(s\)\s*(?::)?\s*([A-Za-z\s.]+?)(?:\n|Email|Office|Phone)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            name = clean_text(match.group(1))
            # Remove trailing punctuation
            name = re.sub(r'[,;:]$', '', name)
            return name
    return ""

#Extract all SLO blocks from syllabus text, returns a list of dictionaries
#each containing SLO data.
def extract_slo_blocks(text):
    #find the SLO section
    section_start = text.find(SLO_SECTION_START)
    if section_start == -1:
     return []

#Get the section from "course learning outcomes" to the end
    section = text[section_start:]

    slo_blocks = []
    parts = re.split(SLO_HEADER_PATTERN, section, flags=re.IGNORECASE)
    
    # parts[0] is everything before the first SLO (headers, etc.)
    # Then parts[1] is the number, parts[2] is the content, etc.
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            number = parts[i]
            content = parts[i + 1]

            # Extract each field from the content
            # Corslo: the sentence after the number (everything until "This learning outcome" or similar)
            corslo_match = re.search(r'^(.*?)(?=\s*This learning outcome|$)', content, re.DOTALL)
            corslo = safe_extract(corslo_match, 1)

            # CSLO (UM Morris CSLO)
            cslo_match = re.search(CSLO_PATTERN, content, re.DOTALL)
            cslo = safe_extract(cslo_match, 1)

            # PSLO (Discipline PSLO)
            pslo_match = re.search(PSLO_PATTERN, content, re.DOTALL)
            pslo = safe_extract(pslo_match, 1)

            # GenEd Outcome
            gened_match = re.search(GENED_PATTERN, content, re.DOTALL)
            gened = safe_extract(gened_match, 1)

            # Clean up any trailing punctuation or extra text
            corslo = clean_text(corslo)
            cslo = clean_text(cslo)
            pslo = clean_text(pslo)
            gened = clean_text(gened)

            slo_blocks.append({
                'number': number,
                'corslo': corslo,
                'cslo': cslo,
                'pslo': pslo,
                'gened': gened
            })
    
    return slo_blocks