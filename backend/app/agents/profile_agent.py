def create_candidate_profile(parsed_resume):
    """
    Creates a simple candidate profile from parsed resume data.
    """

    name = parsed_resume.get("name", "Unknown Candidate")
    email = parsed_resume.get("email", "")
    phone = parsed_resume.get("phone", "")
    skills = parsed_resume.get("skills", [])
    education = parsed_resume.get("education", [])
    experience = parsed_resume.get("experience", [])
    projects = parsed_resume.get("projects", [])

    if len(experience) == 0:
        experience_level = "Fresher"
    elif len(experience) <= 2:
        experience_level = "Entry Level"
    else:
        experience_level = "Experienced"

    profile = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "experience_level": experience_level,
        "profile_summary": (
            f"{name} is a {experience_level.lower()} candidate "
            f"with knowledge of {len(skills)} identified skills."
        )
    }

    return profile