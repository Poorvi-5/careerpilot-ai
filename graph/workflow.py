
import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from graph.state import InterviewState

from graph.nodes import (
    retrieve_node,
    question_node,
    evaluation_node,
    report_node
)


def route_action(state: InterviewState):

    return state["action"]


def create_interview_graph():

    graph = StateGraph(InterviewState)

    # Add nodes
    graph.add_node(
        "retrieve_context",
        retrieve_node
    )

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

    # Route based on action
    graph.add_conditional_edges(
        START,
        route_action,
        {
            "question": "retrieve_context",
            "evaluate": "evaluate_answer",
            "report": "generate_report"
        }
    )

    # RAG → Question
    graph.add_edge(
        "retrieve_context",
        "generate_question"
    )

    # Question generation ends here
    graph.add_edge(
        "generate_question",
        END
    )

    # Evaluation ends here
    graph.add_edge(
        "evaluate_answer",
        END
    )

    # Report ends here
    graph.add_edge(
        "generate_report",
        END
    )

    # SQLite persistence
    conn = sqlite3.connect(
        "careerpilot_checkpoints.db",
        check_same_thread=False
    )

    checkpointer = SqliteSaver(conn)

    interview_graph = graph.compile(
        checkpointer=checkpointer
    )

    return interview_graph
