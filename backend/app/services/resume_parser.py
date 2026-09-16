import re
from typing import Dict, List


SKILLS = [
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "React.js",
    "Node.js",
    "Express.js",
    "MongoDB",
    "Python",
    "Java",
    "C++",
    "C",
    "SQL",
    "MySQL",
    "Git",
    "GitHub",
    "REST API",
    "FastAPI",
    "Django",
    "Flask",
    "Tailwind CSS",
    "Bootstrap",
    "TypeScript",
    "Power BI",
    "Excel",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Structures",
    "Algorithms",
    "Docker",
    "AWS",
]


def clean_text(text: str) -> str:
    """
    Clean extracted resume text.
    """

    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = text.replace("\r", "\n")

    # Remove repeated spaces but preserve lines
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def find_email(text: str) -> str:
    """
    Detect email address.
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return ""


def find_phone(text: str) -> str:
    """
    Detect Indian and international phone numbers.
    """

    patterns = [
        r"\+91[\s-]?[6-9]\d{9}",
        r"\b[6-9]\d{9}\b",
        r"\+\d{1,3}[\s-]?\d{8,12}",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return ""


def find_name(text: str) -> str:
    """
    Detect name from the first few lines.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return ""

    ignored_words = [
        "resume",
        "cv",
        "curriculum vitae",
        "profile",
        "contact",
        "email",
        "phone",
        "mobile",
        "linkedin",
        "github",
        "objective",
        "summary",
        "skills",
        "education",
    ]

    for line in lines[:10]:
        lower_line = line.lower()

        if any(word in lower_line for word in ignored_words):
            continue

        if "@" in line:
            continue

        if re.search(r"\d", line):
            continue

        words = line.split()

        if 2 <= len(words) <= 5:
            valid_words = True

            for word in words:
                cleaned_word = re.sub(
                    r"[^A-Za-z.-]",
                    "",
                    word,
                )

                if not cleaned_word:
                    valid_words = False
                    break

            if valid_words:
                return line

    return ""


def find_skills(text: str) -> List[str]:
    """
    Detect technical skills.
    """

    text_lower = text.lower()
    detected_skills = []

    for skill in SKILLS:
        skill_lower = skill.lower()

        # Special handling for short skills
        if skill_lower in ["c", "java", "sql"]:
            pattern = (
                r"(?<![a-z0-9+#])"
                + re.escape(skill_lower)
                + r"(?![a-z0-9+#])"
            )
        else:
            pattern = r"\b" + re.escape(skill_lower) + r"\b"

        if re.search(pattern, text_lower):
            if skill not in detected_skills:
                detected_skills.append(skill)

    return detected_skills


def find_section(
    text: str,
    section_names: List[str],
) -> str:
    """
    Extract basic resume section text.
    """

    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        line_lower = line.lower().strip()

        if any(
            section_name in line_lower
            for section_name in section_names
        ):
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    common_headings = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "achievements",
        "summary",
        "objective",
        "contact",
    ]

    for line in lines[start_index:]:
        line_lower = line.lower().strip()

        if any(
            heading in line_lower
            and len(line_lower) < 35
            for heading in common_headings
        ):
            break

        if line.strip():
            section_lines.append(line.strip())

    return "\n".join(section_lines).strip()


def parse_resume(text: str) -> Dict:
    """
    Convert resume text into structured data.
    """

    cleaned_text = clean_text(text)

    if not cleaned_text:
        return {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "education": "",
            "experience": "",
            "projects": "",
            "certifications": "",
            "summary": "",
            "raw_text": "",
        }

    parsed_resume = {
        "name": find_name(cleaned_text),
        "email": find_email(cleaned_text),
        "phone": find_phone(cleaned_text),
        "skills": find_skills(cleaned_text),
        "education": find_section(
            cleaned_text,
            ["education", "academic background"],
        ),
        "experience": find_section(
            cleaned_text,
            ["experience", "work experience", "employment"],
        ),
        "projects": find_section(
            cleaned_text,
            ["projects", "personal projects", "academic projects"],
        ),
        "certifications": find_section(
            cleaned_text,
            ["certifications", "certificates"],
        ),
        "summary": find_section(
            cleaned_text,
            ["summary", "profile", "objective"],
        ),
        "raw_text": cleaned_text,
    }

    return parsed_resume