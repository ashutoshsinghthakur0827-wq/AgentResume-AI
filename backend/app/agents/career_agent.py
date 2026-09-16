def recommend_careers(skills, experience_level):
    """
    Recommends career roles based on resume skills.
    """

    skill_list = []

    for skill in skills:
        skill_list.append(skill.lower())

    recommendations = []

    if "python" in skill_list and (
        "machine learning" in skill_list
        or "pandas" in skill_list
        or "numpy" in skill_list
    ):
        recommendations.append({
            "role": "Python Developer",
            "reason": "You have Python-related technical skills.",
            "required_next_skills": [
                "FastAPI",
                "Django",
                "REST API",
                "SQL"
            ]
        })

        recommendations.append({
            "role": "Data Analyst",
            "reason": "Your profile contains Python or data-related skills.",
            "required_next_skills": [
                "Advanced SQL",
                "Power BI",
                "Statistics",
                "Excel"
            ]
        })

    if "javascript" in skill_list or "react" in skill_list:
        recommendations.append({
            "role": "Frontend Developer",
            "reason": "You have frontend development skills.",
            "required_next_skills": [
                "React",
                "Responsive Design",
                "REST API",
                "Git"
            ]
        })

    if "node.js" in skill_list or "express" in skill_list:
        recommendations.append({
            "role": "MERN Stack Developer",
            "reason": "You have JavaScript backend or Node.js skills.",
            "required_next_skills": [
                "MongoDB",
                "Express",
                "React",
                "Node.js",
                "Authentication"
            ]
        })

    if "machine learning" in skill_list or "deep learning" in skill_list:
        recommendations.append({
            "role": "Machine Learning Engineer",
            "reason": "Your resume contains AI or machine learning skills.",
            "required_next_skills": [
                "Scikit-learn",
                "Model Deployment",
                "Deep Learning",
                "MLOps"
            ]
        })

    if "sql" in skill_list or "mysql" in skill_list:
        recommendations.append({
            "role": "Database or SQL Developer",
            "reason": "You have database-related skills.",
            "required_next_skills": [
                "Advanced SQL",
                "Database Design",
                "Joins",
                "Indexes"
            ]
        })

    if len(recommendations) == 0:
        recommendations.append({
            "role": "Software Developer Trainee",
            "reason": "Your profile can be improved with programming and project skills.",
            "required_next_skills": [
                "Java or Python",
                "Data Structures",
                "SQL",
                "Git",
                "Projects"
            ]
        })

    return {
        "experience_level": experience_level,
        "career_recommendations": recommendations
    }