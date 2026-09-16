COMMON_JOB_SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "express",
    "mongodb",
    "sql",
    "mysql",
    "git",
    "github",
    "docker",
    "fastapi",
    "django",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "power bi",
    "tableau",
    "excel",
    "communication",
    "problem solving",
    "data structures",
    "algorithms",
    "rest api",
    "cloud computing"
]


def find_skill_gaps(candidate_skills, job_description=""):
    """
    Finds matched and missing skills.
    """

    candidate_skills_lower = []

    for skill in candidate_skills:
        candidate_skills_lower.append(skill.lower())

    if job_description.strip():
        job_text = job_description.lower()

        required_skills = []

        for skill in COMMON_JOB_SKILLS:
            if skill in job_text:
                required_skills.append(skill)
    else:
        required_skills = [
            "python",
            "sql",
            "git",
            "problem solving",
            "communication"
        ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in candidate_skills_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(required_skills) > 0:
        skill_match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100,
            2
        )
    else:
        skill_match_percentage = 0

    return {
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": skill_match_percentage
    }