#helper funcitons for our code

import re
from .config import EXTRA_WHITESPACE

#Helper funciton for cleaning up extra whitespace, newlines and normalize text.
def clean_text(text):
    if not text:
        return ""
    cleaned = re.sub(EXTRA_WHITESPACE, ' ', text)
    return cleaned.strip()

#Helper function for safely extraacting a group from a regex match.
def safe_extract(match, group_index=1, default=""):
    if match and match.group(group_index):
        return clean_text(match.group(group_index))
    return default

#Generic field extractor using regex pattern.
def extract_field(text, pattern, group_index=1, default=""):
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return safe_extract(match, group_index, default)


