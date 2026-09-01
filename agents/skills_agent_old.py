# --------------------------------------------------
# SKILLS DISCOVERY AGENT
# --------------------------------------------------

def discover_skills(resume_text):

    technical_skills = [
        "Java",
        "Python",
        "SQL",
        "MySQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "VS Code",
        "Debugging",
        "Software Testing"
    ]

    transferable_skills = [
        "Communication",
        "Team Collaboration",
        "Problem Solving",
        "Time Management",
        "Adaptability"
    ]

    resume_lower = resume_text.lower()

    found_technical = []
    found_transferable = []

    for skill in technical_skills:

        if skill.lower() in resume_lower:
            found_technical.append(skill)

    for skill in transferable_skills:

        if skill.lower() in resume_lower:
            found_transferable.append(skill)

    return found_technical, found_transferable