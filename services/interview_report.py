from services.llm_service import get_llm, safe_invoke
import json


def generate_interview_report(interview_history):

    llm = get_llm()

    history_text = ""

    for item in interview_history:

        history_text += f"""
Question {item['question_number']}:

Question:
{item['question']}

Candidate Answer:
{item['answer']}

Evaluation:
{item['evaluation']}

-------------------------
"""

    prompt = f"""
You are an expert technical interviewer.

Analyze the complete interview performance.

INTERVIEW HISTORY:
{history_text}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "overall_score": 0,
    "technical_knowledge": 0,
    "problem_solving": 0,
    "communication": 0,
    "strengths": [],
    "weaknesses": [],
    "topics_to_improve": [],
    "final_recommendation": ""
}}

Rules:
- Scores must be between 0 and 100.
- strengths must be a list of strings.
- weaknesses must be a list of strings.
- topics_to_improve must be a list of strings.
- final_recommendation must be a short string.
- Base everything only on the interview history.
- Do not invent information.
"""

    report_text = safe_invoke(
        llm,
        prompt
    )

    report_text = report_text.replace(
        "```json",
        ""
    )

    report_text = report_text.replace(
        "```",
        ""
    )

    report_text = report_text.strip()

    try:

        report = json.loads(
            report_text
        )

        return report

    except json.JSONDecodeError:

        return {
            "overall_score": 0,
            "technical_knowledge": 0,
            "problem_solving": 0,
            "communication": 0,
            "strengths": [],
            "weaknesses": [],
            "topics_to_improve": [],
            "final_recommendation":
                "Unable to generate structured report."
        }