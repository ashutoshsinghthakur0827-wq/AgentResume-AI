def generate_final_career_report(
    candidate_profile,
    skill_gap_report,
    career_report
):
    """
    Combines all agent outputs into one final report.
    """

    missing_skills = skill_gap_report.get("missing_skills", [])

    if len(missing_skills) == 0:
        learning_message = (
            "Your resume covers the identified skills. "
            "Focus on advanced projects and interview preparation."
        )
    else:
        learning_message = (
            "Focus on learning these missing skills: "
            + ", ".join(missing_skills)
        )

    final_report = {
        "candidate_profile": candidate_profile,
        "skill_gap_analysis": skill_gap_report,
        "career_recommendation": career_report,
        "learning_plan": learning_message,
        "next_steps": [
            "Improve resume keywords",
            "Build 2 to 3 practical projects",
            "Practice DSA and problem-solving",
            "Prepare SQL and technical interview questions",
            "Update LinkedIn and GitHub profile"
        ]
    }

    return final_report