
from graph.state import InterviewState

from agents.interview_agent import generate_interview_question
from services.rag_service import search_resume
from services.answer_evaluator import evaluate_answer
from services.interview_report import generate_interview_report


def retrieve_node(state: InterviewState):

    vector_store = state.get("vector_store")

    if vector_store is not None:

        results = search_resume(
            vector_store,
            "candidate skills projects experience education",
            k=3
        )

        context = ""

        for result in results:

            context += (
                result.page_content + "\n"
            )

        state["retrieved_context"] = context

    else:

        state["retrieved_context"] = ""

    return state


def question_node(state: InterviewState):

    question = generate_interview_question(
        state["job_description"],
        state["resume_analysis"],
        state.get("retrieved_context", ""),
        state["evaluation"]
    )

    state["question"] = question

    return state


def evaluation_node(state: InterviewState):

    evaluation = evaluate_answer(
        state["question"],
        state["answer"]
    )

    state["evaluation"] = evaluation

    state["interview_history"].append({
        "question_number": state["question_number"],
        "question": state["question"],
        "answer": state["answer"],
        "evaluation": evaluation
    })

    return state


def report_node(state: InterviewState):

    report = generate_interview_report(
        state["interview_history"]
    )

    state["final_report"] = report

    return state