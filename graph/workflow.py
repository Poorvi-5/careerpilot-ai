import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from graph.state import InterviewState

from graph.nodes import (
    question_node,
    evaluation_node,
    report_node
)


# =========================================================
# ROUTER
# =========================================================

def route_action(state: InterviewState):

    return state["action"]


# =========================================================
# CREATE INTERVIEW GRAPH
# =========================================================

def create_interview_graph():

    graph = StateGraph(InterviewState)


    # =====================================================
    # ADD NODES
    # =====================================================

    graph.add_node(
        "generate_question",
        question_node
    )

    graph.add_node(
        "evaluate_answer",
        evaluation_node
    )

    graph.add_node(
        "generate_report",
        report_node
    )


    # =====================================================
    # START → ROUTER
    # =====================================================

    graph.add_conditional_edges(

        START,

        route_action,

        {
            "question": "generate_question",

            "evaluate": "evaluate_answer",

            "report": "generate_report"
        }
    )


    # =====================================================
    # ALL NODES → END
    # =====================================================

    graph.add_edge(
        "generate_question",
        END
    )

    graph.add_edge(
        "evaluate_answer",
        END
    )

    graph.add_edge(
        "generate_report",
        END
    )


    # =====================================================
    # SQLITE CHECKPOINTER
    # =====================================================

    conn = sqlite3.connect(
        "careerpilot_checkpoints.db",
        check_same_thread=False
    )

    checkpointer = SqliteSaver(conn)


    # =====================================================
    # COMPILE GRAPH
    # =====================================================

    interview_graph = graph.compile(
        checkpointer=checkpointer
    )


    return interview_graph