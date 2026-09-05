from services.llm_service import get_llm


def evaluate_answer(question, answer):

    llm = get_llm()

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer to the interview question.

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate the answer based on:

1. Correctness
2. Technical Depth
3. Relevance
4. Communication

Return the result in this format:

Score: X/10

Correctness:
Give a short evaluation.

Technical Depth:
Give a short evaluation.

Relevance:
Give a short evaluation.

Communication:
Give a short evaluation.

Strengths:
List the strong points.

Improvements:
List what the candidate should improve.

Overall Feedback:
Give concise feedback.

Important:
- Be fair.
- Do not invent information.
- Focus on the candidate's actual answer.
"""

    response = llm.invoke(prompt)

    return response.content