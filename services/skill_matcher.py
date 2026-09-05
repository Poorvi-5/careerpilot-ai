from services.llm_service import get_llm


def match_skills(resume_analysis, jd_analysis):

    llm = get_llm()

    prompt = f"""
You are an expert technical recruiter.

Compare the candidate's resume skills with the skills
required in the job description.

RESUME ANALYSIS:
{resume_analysis}

JOB DESCRIPTION ANALYSIS:
{jd_analysis}

Return the result in exactly this format:

Match Score:
Give a percentage from 0 to 100.

Matched Skills:
List the skills present in both the resume and job description.

Missing Skills:
List the important job-required skills that are missing
from the resume.

Extra Skills:
List useful skills present in the resume but not specifically
required by the job description.

Recommendation:
Give a short recommendation to the candidate.

Important:
- Do not invent skills.
- Consider similar skill names as related where appropriate.
- Keep the answer concise.
"""

    response = llm.invoke(prompt)

    return response.content