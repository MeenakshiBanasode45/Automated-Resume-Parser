"""
parser.py - Resume parsing logic.
Extracts candidate information (name, email, phone, skills, education)
from PDF files using pdfplumber, regular expressions (re), and keyword matching.
"""

import re

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

# Predefined list of commonly recognized technical and soft skills
COMMON_SKILLS = [
    "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript",
    "HTML", "CSS", "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI",
    "Git", "GitHub", "Docker", "Kubernetes", "AWS", "Azure", "Linux",
    "Machine Learning", "Deep Learning", "Data Analysis", "Pandas", "NumPy",
    "TensorFlow", "PyTorch", "Power BI", "Tableau", "Excel",
    "Communication", "Problem Solving", "Leadership", "Teamwork"
]

# Predefined list of commonly recognized educational degrees and qualifications
EDUCATION_KEYWORDS = [
    "B.Tech", "B.E.", "B.Sc", "BCA", "B.Com", "BBA", "BA",
    "M.Tech", "M.E.", "M.Sc", "MCA", "M.Com", "MBA", "MA",
    "Bachelor of Technology", "Bachelor of Engineering",
    "Bachelor of Science", "Bachelor of Computer Applications",
    "Master of Technology", "Master of Science",
    "Master of Computer Applications", "Bachelor", "Master",
    "Diploma", "High School", "HSC", "SSC", "PhD"
]


def extract_text_from_pdf(pdf_file):
    """
    Extracts plain text from an uploaded PDF file or file path.
    Returns the combined text of all pages.
    """
    if pdfplumber is None:
        raise ImportError("pdfplumber is not installed. Run 'pip install pdfplumber' to install it.")

    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text


def extract_name(text):
    """
    Extracts the candidate's name from the top lines of the resume text.
    In standard resumes, the candidate's name appears on the very first few lines.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Skip generic header words that are not names
    ignore_words = ["resume", "curriculum vitae", "cv", "bio-data", "profile", "contact"]

    for line in lines[:5]:  # Look at the first 5 non-empty lines
        lower_line = line.lower()

        # Skip header headings
        if any(word in lower_line for word in ignore_words):
            continue

        # Skip lines that contain email addresses, URLs, or numbers
        if "@" in line or "http" in lower_line or any(char.isdigit() for char in line):
            continue

        # A typical name has 1 to 4 words consisting of alphabetic characters
        words = line.split()
        if 1 <= len(words) <= 4 and all(part.replace(".", "").replace("-", "").isalpha() for part in words):
            return line.title()

    # Fallback to the first non-empty line if no specific match was identified
    return lines[0].title() if lines else "Not Found"


def extract_email(text):
    """
    Extracts the candidate's email address using a standard email regular expression.
    """
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    match = re.search(email_pattern, text)
    if match:
        return match.group(0).strip()
    return "Not Found"


def extract_phone(text):
    """
    Extracts the candidate's phone number using regular expressions.
    Matches Indian (+91), international, and standard 10-digit phone numbers.
    """
    # Pattern to match numbers with optional country code, dashes, spaces, and parentheses
    phone_pattern = r'(?:\+?\d{1,3}[\s-]?)?\(?\d{3,5}\)?[\s.-]?\d{3,5}[\s.-]?\d{3,5}'
    matches = re.findall(phone_pattern, text)

    for match in matches:
        # Strip out non-digit characters to verify the number length
        digits_only = re.sub(r'\D', '', match)
        if 10 <= len(digits_only) <= 13:
            return match.strip()

    return "Not Found"


def extract_skills(text):
    """
    Extracts skills by matching predefined skill keywords against the resume text.
    Uses regex word boundaries to avoid false partial matches.
    """
    found_skills = []
    text_lower = text.lower()

    for skill in COMMON_SKILLS:
        skill_clean = skill.lower()
        # Special case for programming languages like C, C++, C#
        if skill in ["C++", "C#"]:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        elif skill == "C":
            # Avoid matching 'C' inside 'C++' or 'C#' or within words
            if re.search(r'(?<![a-zA-Z+#])c(?![a-zA-Z+#])', text_lower):
                found_skills.append(skill)
        else:
            # Standard word boundary matching
            pattern = rf'\b{re.escape(skill_clean)}\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)

    return found_skills


def extract_education(text):
    """
    Extracts educational degrees by searching for predefined degree keywords.
    """
    found_education = []
    text_upper = text.upper()

    for edu in EDUCATION_KEYWORDS:
        edu_clean = edu.upper()
        pattern = rf'\b{re.escape(edu_clean)}\b'
        if re.search(pattern, text_upper):
            if edu not in found_education:
                found_education.append(edu)

    return found_education


def parse_resume(pdf_file):
    """
    Main parser function that takes a PDF file, extracts the text,
    and returns a structured dictionary of candidate details.
    """
    text = extract_text_from_pdf(pdf_file)

    if not text.strip():
        return {
            "name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
            "skills": "Not Found",
            "education": "Not Found",
            "raw_text": ""
        }

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": ", ".join(skills) if skills else "Not Found",
        "education": ", ".join(education) if education else "Not Found",
        "raw_text": text
    }
