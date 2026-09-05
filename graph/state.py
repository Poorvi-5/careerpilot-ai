from typing import TypedDict, List


class InterviewState(TypedDict):

    job_description: str

    resume_analysis: str

    vector_store: object

    retrieved_context: str

    question: str

    answer: str

    evaluation: str

    question_number: int

    interview_history: List[dict]

    final_report: dict

    action: str