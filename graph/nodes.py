from graph.state import InterviewState

from agents.interview_agent import generate_interview_question
from services.answer_evaluator import evaluate_answer
from services.interview_report import generate_interview_report


# =========================================================
# GENERATE QUESTION
# =========================================================

def question_node(state: InterviewState):

    question = generate_interview_question(
        state["job_description"],
        state["resume_analysis"],
        state["evaluation"]
    )

    state["question"] = question

    return state


# =========================================================
# EVALUATE ANSWER
# =========================================================

def evaluation_node(state: InterviewState):

    evaluation = evaluate_answer(
        state["question"],
        state["answer"]
    )

    state["evaluation"] = evaluation

    state["interview_history"].append({

        "question_number":
            state["question_number"],

        "question":
            state["question"],

        "answer":
            state["answer"],

        "evaluation":
            evaluation
    })

    return state


# =========================================================
# FINAL REPORT
# =========================================================

def report_node(state: InterviewState):

    report = generate_interview_report(
        state["interview_history"]
    )

    state["final_report"] = report

    return state