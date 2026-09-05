from services.llm_service import get_llm


def analyze_resume(resume_text):

    llm = get_llm()

    prompt = f"""
You are an expert resume analyzer.

Analyze the following resume and extract the information.

RESUME:
{resume_text}

Return the answer in this format:

Name:
Education:
Skills:
Experience:
Projects:
Certifications:

Important:
- Be concise.
- Only use information present in the resume.
- Do not invent information.
"""

    response = llm.invoke(prompt)

    return response.content