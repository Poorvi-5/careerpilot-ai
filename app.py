import uuid

import streamlit as st

from services.resume_parser import extract_text_from_pdf
from services.resume_analyzer import analyze_resume
from services.jd_analyzer import analyze_job_description
from services.skill_matcher import match_skills
from services.roadmap_generator import generate_roadmap
from services.pdf_report import create_pdf_report
from services.rag_service import create_vector_store

from graph.workflow import create_interview_graph


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# LOAD CUSTOM CSS
# =========================================================

def load_css():

    try:

        with open("style.css", "r", encoding="utf-8") as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        pass


load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = ""

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = ""

if "skill_match" not in st.session_state:
    st.session_state.skill_match = ""

if "roadmap" not in st.session_state:
    st.session_state.roadmap = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "interview_graph" not in st.session_state:
    st.session_state.interview_graph = create_interview_graph()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "question" not in st.session_state:
    st.session_state.question = ""

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

if "final_report" not in st.session_state:
    st.session_state.final_report = {}


# =========================================================
# HEADER
# =========================================================

st.title("🎯 CareerPilot AI")

st.markdown(
    """
    ### Agentic Resume & Interview Intelligence System

    Analyze your resume, compare it with a job description,
    generate a personalized learning roadmap, and practice
    with an adaptive AI interviewer.
    """
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📄 Resume & Job Analysis",
        "🗺️ Learning Roadmap",
        "🤖 AI Mock Interview",
        "📊 Final Report"
    ]
)


# =========================================================
# TAB 1
# RESUME & JOB ANALYSIS
# =========================================================

with tab1:

    st.header("📄 Resume & Job Analysis")

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # RESUME
    # -----------------------------------------------------

    with col1:

        st.subheader("Upload Resume")

        uploaded_resume = st.file_uploader(
            "Upload your resume PDF",
            type=["pdf"]
        )

    # -----------------------------------------------------
    # JOB DESCRIPTION
    # -----------------------------------------------------

    with col2:

        st.subheader("Job Description")

        job_description = st.text_area(
            "Paste the job description here",
            height=250,
            placeholder="Paste the complete job description..."
        )

    st.divider()

    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    if st.button(
        "🚀 Analyze Resume & Job",
        use_container_width=True
    ):

        # -------------------------------------------------
        # CHECK RESUME
        # -------------------------------------------------

        if uploaded_resume is None:

            st.error(
                "❌ Please upload your resume PDF."
            )

            st.stop()

        # -------------------------------------------------
        # CHECK FILE SIZE
        # -------------------------------------------------

        if uploaded_resume.size > 5 * 1024 * 1024:

            st.error(
                "❌ Resume PDF must be smaller than 5 MB."
            )

            st.stop()

        # -------------------------------------------------
        # CHECK JOB DESCRIPTION
        # -------------------------------------------------

        if not job_description.strip():

            st.error(
                "❌ Please paste the job description."
            )

            st.stop()

        # -------------------------------------------------
        # SAVE JOB DESCRIPTION
        # -------------------------------------------------

        st.session_state.job_description = (
            job_description
        )

        # =================================================
        # EXTRACT RESUME TEXT
        # =================================================

        with st.spinner(
            "📄 Reading your resume..."
        ):

            try:

                resume_text = extract_text_from_pdf(
                    uploaded_resume
                )

            except Exception as e:

                st.error(
                    "❌ Unable to read the PDF."
                )

                st.exception(e)

                st.stop()

        # -------------------------------------------------
        # CHECK EMPTY PDF
        # -------------------------------------------------

        if not resume_text.strip():

            st.error(
                "❌ Could not extract text from the resume."
            )

            st.warning(
                "Please upload a text-based PDF resume."
            )

            st.stop()

        # Save resume text
        st.session_state.resume_text = resume_text

        # =================================================
        # CREATE RAG VECTOR STORE
        # =================================================

        with st.spinner(
            "🧠 Creating resume knowledge base..."
        ):

            try:

                st.session_state.vector_store = (
                    create_vector_store(
                        resume_text
                    )
                )

            except Exception as e:

                st.error(
                    "❌ Failed to create resume knowledge base."
                )

                st.exception(e)

                st.stop()

        # =================================================
        # RESUME ANALYSIS
        # =================================================

        with st.spinner(
            "🔍 Analyzing resume..."
        ):

            try:

                st.session_state.resume_analysis = (
                    analyze_resume(
                        resume_text
                    )
                )

            except Exception as e:

                st.error(
                    "❌ Resume analysis failed."
                )

                st.exception(e)

                st.stop()

        # =================================================
        # JOB DESCRIPTION ANALYSIS
        # =================================================

        with st.spinner(
            "💼 Analyzing job description..."
        ):

            try:

                st.session_state.jd_analysis = (
                    analyze_job_description(
                        job_description
                    )
                )

            except Exception as e:

                st.error(
                    "❌ Job description analysis failed."
                )

                st.exception(e)

                st.stop()

        # =================================================
        # SKILL MATCHING
        # =================================================

        with st.spinner(
            "🎯 Matching resume with job requirements..."
        ):

            try:

                st.session_state.skill_match = (
                    match_skills(
                        st.session_state.resume_analysis,
                        st.session_state.jd_analysis
                    )
                )

            except Exception as e:

                st.error(
                    "❌ Skill matching failed."
                )

                st.exception(e)

                st.stop()

        # =================================================
        # LEARNING ROADMAP
        # =================================================

        with st.spinner(
            "🗺️ Generating personalized roadmap..."
        ):

            try:

                st.session_state.roadmap = (
                    generate_roadmap(
                        st.session_state.skill_match
                    )
                )

            except Exception as e:

                st.error(
                    "❌ Roadmap generation failed."
                )

                st.exception(e)

                st.stop()

        st.success(
            "✅ Resume and job analysis completed successfully!"
        )

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    if st.session_state.resume_analysis:

        st.divider()

        st.header("🔍 Analysis Results")

        # -------------------------------------------------
        # RESUME ANALYSIS
        # -------------------------------------------------

        with st.expander(
            "📄 Resume Analysis",
            expanded=True
        ):

            st.markdown(
                st.session_state.resume_analysis
            )

        # -------------------------------------------------
        # JD ANALYSIS
        # -------------------------------------------------

        with st.expander(
            "💼 Job Description Analysis",
            expanded=True
        ):

            st.markdown(
                st.session_state.jd_analysis
            )

        # -------------------------------------------------
        # SKILL MATCH
        # -------------------------------------------------

        with st.expander(
            "🎯 Resume ↔ Job Skill Match",
            expanded=True
        ):

            st.markdown(
                st.session_state.skill_match
            )

        # -------------------------------------------------
        # RAG STATUS
        # -------------------------------------------------

        if st.session_state.vector_store is not None:

            st.success(
                "🧠 Resume knowledge base is ready for AI interview."
            )


# =========================================================
# TAB 2
# LEARNING ROADMAP
# =========================================================

with tab2:

    st.header("🗺️ Personalized Learning Roadmap")

    if st.session_state.roadmap:

        st.markdown(
            st.session_state.roadmap
        )

    else:

        st.info(
            "First analyze your resume and job description "
            "to generate your personalized roadmap."
        )


# =========================================================
# TAB 3
# AI MOCK INTERVIEW
# =========================================================

with tab3:

    st.header("🤖 AI Mock Interview")

    st.markdown(
        """
        The AI interviewer adapts the difficulty of the next
        question based on your previous answer.
        """
    )

    # =====================================================
    # START INTERVIEW
    # =====================================================

    if not st.session_state.interview_started:

        if st.button(
            "🎤 Start AI Interview",
            use_container_width=True
        ):

            if (
                not st.session_state.resume_analysis
                or not st.session_state.job_description
            ):

                st.error(
                    "❌ Please complete Resume & Job Analysis first."
                )

            else:

                # Create unique thread
                st.session_state.thread_id = (
                    str(uuid.uuid4())
                )

                # Reset interview
                st.session_state.question = ""
                st.session_state.answer = ""
                st.session_state.evaluation = ""
                st.session_state.question_number = 1
                st.session_state.interview_history = []
                st.session_state.final_report = {}

                # -------------------------------------------------
                # INITIAL GRAPH STATE
                # -------------------------------------------------

                initial_state = {

                    "job_description":
                        st.session_state.job_description,

                    "resume_analysis":
                        st.session_state.resume_analysis,

                    "vector_store":
                        st.session_state.vector_store,

                    "retrieved_context":
                        "",

                    "question":
                        "",

                    "answer":
                        "",

                    "evaluation":
                        "",

                    "question_number":
                        1,

                    "interview_history":
                        [],

                    "final_report":
                        {},

                    "action":
                        "question"
                }

                config = {

                    "configurable": {

                        "thread_id":
                            st.session_state.thread_id
                    }
                }

                with st.spinner(
                    "🤖 Preparing your first interview question..."
                ):

                    try:

                        result = (
                            st.session_state.interview_graph.invoke(
                                initial_state,
                                config=config
                            )
                        )

                    except Exception as e:

                        st.error(
                            "❌ Failed to start interview."
                        )

                        st.exception(e)

                        st.stop()

                st.session_state.question = (
                    result["question"]
                )

                st.session_state.interview_started = True

                st.rerun()

    # =====================================================
    # INTERVIEW STARTED
    # =====================================================

    if st.session_state.interview_started:

        st.success(
            f"Interview Session: "
            f"{st.session_state.thread_id}"
        )

        # -------------------------------------------------
        # PROGRESS
        # -------------------------------------------------

        current_question = (
            st.session_state.question_number
        )

        progress = (
            current_question / 5
        )

        st.progress(
            min(progress, 1.0)
        )

        st.caption(
            f"Question {current_question} of 5"
        )

        st.divider()

        # -------------------------------------------------
        # QUESTION
        # -------------------------------------------------

        if st.session_state.question:

            st.subheader(
                f"❓ Question {current_question}"
            )

            st.info(
                st.session_state.question
            )

            # -------------------------------------------------
            # ANSWER
            # -------------------------------------------------

            answer = st.text_area(
                "Your Answer",
                height=200,
                key=f"answer_{current_question}",
                placeholder="Type your answer here..."
            )

            # -------------------------------------------------
            # SUBMIT
            # -------------------------------------------------

            if st.button(
                "📤 Submit Answer",
                use_container_width=True
            ):

                if not answer.strip():

                    st.warning(
                        "⚠️ Please write an answer first."
                    )

                else:

                    st.session_state.answer = answer

                    config = {

                        "configurable": {

                            "thread_id":
                                st.session_state.thread_id
                        }
                    }

                    current_state = (
                        st.session_state.interview_graph
                        .get_state(config)
                        .values
                    )

                    current_state["answer"] = answer

                    current_state["action"] = "evaluate"

                    with st.spinner(
                        "🧠 Evaluating your answer..."
                    ):

                        try:

                            result = (
                                st.session_state.interview_graph
                                .invoke(
                                    current_state,
                                    config=config
                                )
                            )

                        except Exception as e:

                            st.error(
                                "❌ Answer evaluation failed."
                            )

                            st.exception(e)

                            st.stop()

                    st.session_state.evaluation = (
                        result["evaluation"]
                    )

                    st.session_state.interview_history = (
                        result["interview_history"]
                    )

                    st.rerun()

            # =================================================
            # EVALUATION
            # =================================================

            if st.session_state.evaluation:

                st.divider()

                st.subheader(
                    "📝 AI Evaluation"
                )

                st.markdown(
                    st.session_state.evaluation
                )

                # -------------------------------------------------
                # NEXT QUESTION
                # -------------------------------------------------

                if (
                    st.session_state.question_number
                    < 5
                ):

                    if st.button(
                        "➡️ Next Question",
                        use_container_width=True
                    ):

                        st.session_state.question_number += 1

                        config = {

                            "configurable": {

                                "thread_id":
                                    st.session_state.thread_id
                            }
                        }

                        current_state = (
                            st.session_state.interview_graph
                            .get_state(config)
                            .values
                        )

                        current_state["question_number"] = (
                            st.session_state.question_number
                        )

                        current_state["answer"] = ""

                        current_state["evaluation"] = ""

                        current_state["action"] = "question"

                        with st.spinner(
                            "🤖 Generating adaptive question..."
                        ):

                            try:

                                result = (
                                    st.session_state.interview_graph
                                    .invoke(
                                        current_state,
                                        config=config
                                    )
                                )

                            except Exception as e:

                                st.error(
                                    "❌ Failed to generate next question."
                                )

                                st.exception(e)

                                st.stop()

                        st.session_state.question = (
                            result["question"]
                        )

                        st.session_state.evaluation = ""

                        st.rerun()

                else:

                    st.success(
                        "🎉 You completed all 5 interview questions!"
                    )

                    st.info(
                        "Go to the Final Report tab "
                        "to generate your complete interview report."
                    )

        # =================================================
        # INTERVIEW HISTORY
        # =================================================

        if st.session_state.interview_history:

            st.divider()

            st.subheader(
                "📚 Interview History"
            )

            for item in st.session_state.interview_history:

                with st.expander(
                    f"Question {item['question_number']}"
                ):

                    st.markdown(
                        "**Question:**"
                    )

                    st.write(
                        item["question"]
                    )

                    st.markdown(
                        "**Your Answer:**"
                    )

                    st.write(
                        item["answer"]
                    )

                    st.markdown(
                        "**Evaluation:**"
                    )

                    st.write(
                        item["evaluation"]
                    )


# =========================================================
# TAB 4
# FINAL REPORT
# =========================================================

with tab4:

    st.header("📊 Final Interview Report")

    # =====================================================
    # GENERATE REPORT
    # =====================================================

    if (
        st.session_state.interview_started
        and len(st.session_state.interview_history) >= 5
    ):

        if st.button(
            "📊 Generate Final Report",
            use_container_width=True
        ):

            config = {

                "configurable": {

                    "thread_id":
                        st.session_state.thread_id
                }
            }

            current_state = (
                st.session_state.interview_graph
                .get_state(config)
                .values
            )

            current_state["action"] = "report"

            with st.spinner(
                "📊 Generating final interview report..."
            ):

                try:

                    result = (
                        st.session_state.interview_graph
                        .invoke(
                            current_state,
                            config=config
                        )
                    )

                except Exception as e:

                    st.error(
                        "❌ Failed to generate final report."
                    )

                    st.exception(e)

                    st.stop()

            st.session_state.final_report = (
                result["final_report"]
            )

            st.success(
                "✅ Final interview report generated!"
            )

    # =====================================================
    # DISPLAY REPORT
    # =====================================================

    if st.session_state.final_report:

        report = st.session_state.final_report

        st.divider()

        # =================================================
        # SCORE CARDS
        # =================================================

        st.subheader(
            "🏆 Performance Overview"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Overall Score",
                f"{report['overall_score']}/100"
            )

        with col2:

            st.metric(
                "Technical Knowledge",
                f"{report['technical_knowledge']}/100"
            )

        with col3:

            st.metric(
                "Problem Solving",
                f"{report['problem_solving']}/100"
            )

        with col4:

            st.metric(
                "Communication",
                f"{report['communication']}/100"
            )

        st.divider()

        # =================================================
        # PERFORMANCE
        # =================================================

        st.subheader(
            "📈 Performance Breakdown"
        )

        chart_data = {

            "Technical Knowledge":
                report["technical_knowledge"],

            "Problem Solving":
                report["problem_solving"],

            "Communication":
                report["communication"]
        }

        st.bar_chart(
            chart_data,
            height=350
        )

        st.divider()

        # =================================================
        # STRENGTHS AND WEAKNESSES
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "💪 Strengths"
            )

            if report["strengths"]:

                for strength in report["strengths"]:

                    st.success(
                        f"✓ {strength}"
                    )

            else:

                st.write(
                    "No strengths identified."
                )

        with col2:

            st.subheader(
                "⚠️ Areas to Improve"
            )

            if report["weaknesses"]:

                for weakness in report["weaknesses"]:

                    st.warning(
                        f"• {weakness}"
                    )

            else:

                st.write(
                    "No major weaknesses identified."
                )

        st.divider()

        # =================================================
        # TOPICS
        # =================================================

        st.subheader(
            "📚 Recommended Topics"
        )

        if report["topics_to_improve"]:

            for topic in report["topics_to_improve"]:

                st.info(
                    f"→ {topic}"
                )

        else:

            st.write(
                "No specific topics identified."
            )

        st.divider()

        # =================================================
        # RECOMMENDATION
        # =================================================

        st.subheader(
            "🎯 Final Recommendation"
        )

        st.markdown(
            f"""
            > {report["final_recommendation"]}
            """
        )

        st.divider()

        # =================================================
        # PDF
        # =================================================

        st.subheader(
            "📄 Interview Report PDF"
        )

        if st.button(
            "📝 Create PDF Report",
            use_container_width=True
        ):

            try:

                pdf_filename = create_pdf_report(
                    report
                )

                with open(
                    pdf_filename,
                    "rb"
                ) as pdf_file:

                    st.download_button(
                        label="⬇️ Download Interview Report",
                        data=pdf_file,
                        file_name="careerpilot_interview_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    "❌ Failed to create PDF report."
                )

                st.exception(e)

    else:

        st.info(
            """
            Complete the 5-question AI mock interview first.
            Then generate your final performance report here.
            """
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">

    <b>CareerPilot AI</b><br>

    Agentic Resume & Interview Intelligence System

    </div>
    """,
    unsafe_allow_html=True
)