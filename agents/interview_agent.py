from services.llm_service import get_llm, safe_invoke


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

Interview adaptation rules:

1. If there is no previous evaluation:
   - Ask a medium-difficulty technical question.

2. If the previous answer was weak:
   - Ask a simpler question.
   - Focus on the topic the candidate struggled with.

3. If the previous answer was average:
   - Ask a similar-difficulty question.
   - Test deeper understanding of the same or a related topic.

4. If the previous answer was strong:
   - Increase the difficulty.
   - Ask a more advanced technical question.

5. Always consider:
   - Job description requirements.
   - Candidate's actual resume.
   - Retrieved resume information.

6. Do not:
   - Repeat the previous question.
   - Invent candidate experience or skills.
   - Provide the answer.

Return ONLY the interview question.
"""

    return safe_invoke(
        llm,
        prompt
    )