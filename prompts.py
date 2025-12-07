def get_resume_prompt(jd: str, raw_bullets: str, skills: str) -> str:
    return f"""
    You are Pakistan's top resume writer for freshers (FAST, NUST, LUMS, COMSATS).

    Job Description:
    {jd}

    Candidate raw bullets:
    {raw_bullets}

    Skills: {skills}

    Task:
    - Rewrite 5–7 powerful bullets that perfectly match the JD keywords
    - Use strong action verbs (Developed, Built, Designed, Implemented)
    - Keep natural Pakistani fresher tone (mention FYP, internship, university projects)
    - Return ONLY the bullet points, each starting with •
    """
