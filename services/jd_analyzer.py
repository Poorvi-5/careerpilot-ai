from services.llm_service import get_llm, safe_invoke


def analyze_job_description(job_description):

    llm = get_llm()

    prompt = f"""
You are an expert job description analyzer.

Analyze the following job description.

JOB DESCRIPTION:
{job_description}

Extract the following information:

Job Role:
Required Skills:
Preferred Skills:
Experience Required:
Responsibilities:

Important:
- Be concise.
- Only use information present in the job description.
- Do not invent information.
"""

    return safe_invoke(
        llm,
        prompt
    )