# Column headers (matching your Excel)
COLUMNS = ["Course", "Semester", "instructor", "Number", "Corslo", "PSLO", "McSLO", "CSLO", "GenEd Outcome"]

# Regex patterns
COURSE_PATTERN = r'([A-Za-z]{2,4}\s?\d{4})'
SEMESTER_PATTERN = r'(Fall|Spring|Summer)\s+(20\d{2})'
INSTRUCTOR_PATTERN = r'Instructor\s*([A-Za-z\s]+?)(?:\n|Email)'

#SLO
SLO_SECTION_START = "Course Learning Outcomes"
SLO_HEADER_PATTERN = r'(?:Student\s+Learning\s+Outcome|SLO)\s*#?\s*(\d+)\s*[:.\-]?'
CSLO_PATTERN = r'UM Morris CSLO:\s*(.*?)(?=;|Discipline PSLO|GenEd Outcome|$)'
PSLO_PATTERN = r'Discipline PSLO:\s*(.*?)(?=;|GenEd Outcome|$)'
GENED_PATTERN = r'GenEd Outcome:\s*(.*?)(?=;|$)'

EXTRA_WHITESPACE = r'\s+'


