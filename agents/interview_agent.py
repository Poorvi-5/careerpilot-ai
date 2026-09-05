
from services.llm_service import get_llm


def generate_interview_question(
    job_description,
    resume_analysis,
    retrieved_context="",
    previous_evaluation=""
):

    llm = get_llm()

    prompt = f"""
You are an expert technical interviewer.

Create ONE interview question for this candidate.

JOB DESCRIPTION:
{job_description}

RESUME ANALYSIS:
{resume_analysis}

RELEVANT RESUME INFORMATION:
{retrieved_context}

PREVIOUS EVALUATION:
{previous_evaluation}

Rules:
- Ask a technical interview question relevant to the job.
- Use the relevant resume information when possible.
- Focus on skills required by the job description.
- If this is the first question, ask a medium-difficulty question.
- If previous evaluation is available, adapt the next question
  based on the candidate's weaknesses.
- If the candidate performed well, slightly increase difficulty.
- Do not repeat the previous question.
- Do not provide the answer.
- Do not invent candidate experience or skills.
- Return only the question.
"""

    response = llm.invoke(prompt)

    return response.content
