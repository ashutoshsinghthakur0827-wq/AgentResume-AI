import re
from typing import Dict, List


ATS_KEYWORDS = [
    "experience",
    "education",
    "skills",
    "projects",
    "certification",
    "summary",
    "objective",
    "responsibilities",
    "achievements",
    "github",
    "linkedin",
    "email",
    "phone",
]


TECHNICAL_SKILLS = [
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "express.js",
    "mongodb",
    "python",
    "java",
    "sql",
    "git",
    "github",
    "rest api",
    "fastapi",
    "django",
    "machine learning",
    "artificial intelligence",
    "data structures",
    "algorithms",
]


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def count_keywords(text: str) -> int:
    """
    Count ATS-friendly resume keywords.
    """

    normalized_text = normalize_text(text)

    count = 0

    for keyword in ATS_KEYWORDS:
        if keyword in normalized_text:
            count += 1

    return count


def find_detected_skills(text: str) -> List[str]:
    """
    Detect technical skills from resume.
    """

    normalized_text = normalize_text(text)

    skills = []

    for skill in TECHNICAL_SKILLS:
        if skill in normalized_text:
            skills.append(skill)

    return skills


def calculate_ats_score(text: str) -> int:
    """
    Calculate simple ATS score out of 100.
    """

    if not text or not text.strip():
        return 0

    normalized_text = normalize_text(text)

    score = 0

    # Resume length
    word_count = len(normalized_text.split())

    if word_count >= 100:
        score += 20
    elif word_count >= 50:
        score += 12
    elif word_count >= 20:
        score += 6

    # Important sections
    keyword_count = count_keywords(normalized_text)

    score += min(keyword_count * 4, 32)

    # Technical skills
    skill_count = len(find_detected_skills(normalized_text))

    score += min(skill_count * 3, 30)

    # Contact details
    if re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        normalized_text,
    ):
        score += 8

    if re.search(r"\b[6-9]\d{9}\b", normalized_text):
        score += 5

    # Keep score between 0 and 100
    return min(score, 100)


def analyze_resume(text: str) -> Dict:
    """
    Generate ATS analysis.
    """

    if not text or not text.strip():
        return {
            "ats_score": 0,
            "score": 0,
            "word_count": 0,
            "keyword_count": 0,
            "detected_skills": [],
            "strengths": [],
            "improvements": [
                "Resume text is empty.",
                "Please upload and process a resume first.",
            ],
            "message": "No resume text available.",
        }

    normalized_text = normalize_text(text)

    word_count = len(normalized_text.split())
    keyword_count = count_keywords(normalized_text)
    detected_skills = find_detected_skills(normalized_text)
    ats_score = calculate_ats_score(normalized_text)

    strengths = []
    improvements = []

    if word_count >= 50:
        strengths.append("Resume contains sufficient text.")
    else:
        improvements.append(
            "Add more details about your education, skills and projects."
        )

    if keyword_count >= 5:
        strengths.append("Resume contains useful ATS keywords.")
    else:
        improvements.append(
            "Add clear sections such as Skills, Education and Projects."
        )

    if detected_skills:
        strengths.append(
            f"Detected technical skills: {len(detected_skills)}"
        )
    else:
        improvements.append(
            "Add technical skills relevant to your target job."
        )

    if "github" not in normalized_text:
        improvements.append(
            "Add your GitHub profile if available."
        )

    if "linkedin" not in normalized_text:
        improvements.append(
            "Add your LinkedIn profile if available."
        )

    if "experience" not in normalized_text:
        improvements.append(
            "Add internship, training or project experience."
        )

    if "projects" not in normalized_text:
        improvements.append(
            "Add a dedicated Projects section."
        )

    return {
        "ats_score": ats_score,
        "score": ats_score,
        "word_count": word_count,
        "keyword_count": keyword_count,
        "detected_skills": detected_skills,
        "strengths": strengths,
        "improvements": improvements,
        "message": "ATS analysis completed successfully.",
    }