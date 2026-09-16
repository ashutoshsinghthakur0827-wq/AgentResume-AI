import re
from typing import Dict, List


SKILL_ALIASES = {
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "JavaScript": ["javascript", "java script", "js"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node", "node.js", "nodejs"],
    "Express.js": ["express", "express.js", "expressjs"],
    "MongoDB": ["mongodb", "mongo db", "mongo"],
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c++"],
    "SQL": ["sql", "mysql", "postgresql"],
    "REST API": ["rest api", "restful api", "rest-api"],
    "Git": ["git"],
    "GitHub": ["github", "git hub"],
    "Data Structures": [
        "data structures",
        "data structure",
        "dsa",
    ],
    "Algorithms": [
        "algorithms",
        "algorithm",
    ],
    "Tailwind CSS": [
        "tailwind",
        "tailwind css",
    ],
    "TypeScript": [
        "typescript",
        "type script",
    ],
    "FastAPI": [
        "fastapi",
        "fast api",
    ],
    "Docker": [
        "docker",
    ],
    "AWS": [
        "aws",
        "amazon web services",
    ],
    "Power BI": [
        "power bi",
        "powerbi",
    ],
    "Excel": [
        "excel",
        "microsoft excel",
    ],
    "Pandas": [
        "pandas",
    ],
    "NumPy": [
        "numpy",
    ],
    "Machine Learning": [
        "machine learning",
        "machine-learning",
    ],
    "Artificial Intelligence": [
        "artificial intelligence",
        "artificial-intelligence",
    ],
}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_skill(
    text: str,
    alias: str,
) -> bool:
    """
    Match complete skill names.
    """

    text = normalize_text(text)
    alias = normalize_text(alias)

    if not text or not alias:
        return False

    escaped_alias = re.escape(alias)

    pattern = (
        rf"(?<![a-z0-9+#])"
        rf"{escaped_alias}"
        rf"(?![a-z0-9+#])"
    )

    return re.search(pattern, text) is not None


def detect_skills(text: str) -> List[str]:
    normalized_text = normalize_text(text)

    detected_skills = []

    for main_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if contains_skill(normalized_text, alias):
                detected_skills.append(main_skill)
                break

    return detected_skills


def match_resume_with_job(
    resume_text: str,
    job_description: str,
) -> Dict:
    """
    Compare resume skills with job description skills.
    """

    if not resume_text or not resume_text.strip():
        return {
            "success": False,
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": [],
            "job_skills": [],
            "suggestions": [],
            "message": "Resume text is empty.",
        }

    if not job_description or not job_description.strip():
        return {
            "success": False,
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": detect_skills(resume_text),
            "job_skills": [],
            "suggestions": [],
            "message": "Job description is empty.",
        }

    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_description)

    matched_skills = [
        skill
        for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in job_skills
        if skill not in resume_skills
    ]

    if job_skills:
        match_percentage = round(
            len(matched_skills) / len(job_skills) * 100
        )
    else:
        match_percentage = 0

    suggestions = [
        f"Learn or practice {skill}."
        for skill in missing_skills
    ]

    return {
        "success": True,
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "suggestions": suggestions,
        "message": "Job matching completed successfully.",
    }