from services.llm_service import get_llm


def generate_roadmap(skill_match):

    llm = get_llm()

    prompt = f"""
You are an expert AI career mentor.

Based on the following resume-job skill matching result,
create a personalized learning roadmap for the candidate.

SKILL MATCH RESULT:
{skill_match}

Create a practical 4-week roadmap.

For each week provide:

Week:
Skill to Learn:
Topics:
Practice:
Mini Project:

At the end provide:

Final Project:
Interview Preparation:

Important:
- Focus mainly on missing skills.
- Start with beginner-friendly concepts.
- Make the roadmap practical.
- Do not invent information about the candidate.
- Keep the answer concise.
"""

    response = llm.invoke(prompt)

    return response.content