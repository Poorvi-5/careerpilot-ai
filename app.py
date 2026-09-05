import uuid

import streamlit as st

from services.resume_parser import extract_text_from_pdf
from services.rag_service import create_vector_store
from services.pdf_report import create_pdf_report
from services.resume_analyzer import analyze_resume
from services.jd_analyzer import analyze_job_description
from services.skill_matcher import match_skills
from services.roadmap_generator import generate_roadmap

from graph.workflow import create_interview_graph


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)


# =========================================================
# LOAD CUSTOM CSS
# =========================================================

def load_css():

    with open("style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# =========================================================
# TITLE
# =========================================================

st.title("🚀 CareerPilot AI")

st.write(
    "AI-powered Resume, Job Matching and Mock Interview System"
)


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

if "interview_graph" not in st.session_state:
    st.session_state.interview_graph = create_interview_graph()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = ""

if "question" not in st.session_state:
    st.session_state.question = ""

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

if "final_report" not in st.session_state:
    st.session_state.final_report = {}

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📂 CareerPilot AI")

st.sidebar.write(
    "Your AI career assistant for resume analysis, "
    "job matching and interview preparation."
)

st.sidebar.divider()

st.sidebar.markdown(
    """
### 🧠 AI Pipeline

📄 Resume Analysis  
⬇️  
💼 Job Analysis  
⬇️  
🎯 Skill Matching  
⬇️  
🗺️ Learning Roadmap  
⬇️  
🎤 AI Mock Interview  
⬇️  
🏆 Final Report
"""
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Resume & Job Analysis",
        "🗺️ Learning Roadmap",
        "🎤 AI Mock Interview",
        "🏆 Final Report"
    ]
)



# =========================================================
# TAB 1 — RESUME & JOB ANALYSIS
# =========================================================

with tab1:

    st.header("📄 Resume & Job Analysis")

    st.write(
        "Upload your resume and paste the target job description "
        "to evaluate your job readiness."
    )

    # -----------------------------------------------------
    # Resume Upload
    # -----------------------------------------------------

    st.subheader("📄 Upload Resume")

    resume = st.file_uploader(
        "Upload your Resume PDF",
        type=["pdf"]
    )

    # -----------------------------------------------------
    # Job Description
    # -----------------------------------------------------

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the Job Description here",
        height=250,
        placeholder="Paste the complete job description..."
    )

    # -----------------------------------------------------
    # Analyze Button
    # -----------------------------------------------------

    if st.button(
        "🔍 Analyze Resume & Job",
        use_container_width=True
    ):

        if resume is None:

            st.warning(
                "⚠️ Please upload your resume first."
            )

        elif not job_description.strip():

            st.warning(
                "⚠️ Please enter the job description."
            )

        else:

            # ---------------------------------------------
            # Resume Parsing
            # ---------------------------------------------

            with st.spinner(
                "📄 Reading resume..."
            ):

                resume_text = extract_text_from_pdf(
                    resume
                )

            # ---------------------------------------------
            # Create Resume Knowledge Base
            # ---------------------------------------------

            with st.spinner(
                "🧠 Creating resume knowledge base..."
            ):

                st.session_state.vector_store = (
                    create_vector_store(resume_text)
                )

            # ---------------------------------------------
            # Resume Analysis
            # ---------------------------------------------

            with st.spinner(
                "🤖 Analyzing resume with Gemini..."
            ):

                resume_analysis = analyze_resume(
                    resume_text
                )

                st.session_state.resume_analysis = (
                    resume_analysis
                )

            # ---------------------------------------------
            # JD Analysis
            # ---------------------------------------------

            with st.spinner(
                "💼 Analyzing job description..."
            ):

                jd_analysis = analyze_job_description(
                    job_description
                )

                st.session_state.jd_analysis = (
                    jd_analysis
                )

            # ---------------------------------------------
            # Skill Matching
            # ---------------------------------------------

            with st.spinner(
                "🔎 Matching resume skills with JD..."
            ):

                skill_match = match_skills(
                    resume_analysis,
                    jd_analysis
                )

                st.session_state.skill_match = (
                    skill_match
                )

            # ---------------------------------------------
            # Roadmap
            # ---------------------------------------------

            with st.spinner(
                "🗺️ Creating personalized roadmap..."
            ):

                roadmap = generate_roadmap(
                    skill_match
                )

                st.session_state.roadmap = (
                    roadmap
                )

            st.success(
                "✅ Resume and Job analysis completed!"
            )

    # -----------------------------------------------------
    # Resume Analysis Result
    # -----------------------------------------------------

    if st.session_state.resume_analysis:

        st.divider()

        st.subheader("📄 Resume Analysis")

        st.write(
            st.session_state.resume_analysis
        )

    # -----------------------------------------------------
    # JD Analysis Result
    # -----------------------------------------------------

    if st.session_state.jd_analysis:

        st.divider()

        st.subheader("💼 Job Description Analysis")

        st.write(
            st.session_state.jd_analysis
        )

    # -----------------------------------------------------
    # Skill Match Result
    # -----------------------------------------------------

    if st.session_state.skill_match:

        st.divider()

        st.subheader("🎯 Resume-JD Skill Match")

        st.write(
            st.session_state.skill_match
        )



# =========================================================
# TAB 2 — LEARNING ROADMAP
# =========================================================

with tab2:

    st.header("🗺️ Personalized Learning Roadmap")

    st.write(
        "Your roadmap is generated based on the skills "
        "missing from your target job requirements."
    )

    if st.session_state.roadmap:

        st.write(
            st.session_state.roadmap
        )

    else:

        st.info(
            "💡 First complete Resume & Job Analysis "
            "to generate your personalized roadmap."
        )


# =========================================================
# TAB 3 — AI MOCK INTERVIEW
# =========================================================

with tab3:

    st.header("🎤 AI Mock Interview")

    st.write(
        "Practice technical interview questions generated "
        "specifically for your resume and target job."
    )

    # -----------------------------------------------------
    # Start Interview
    # -----------------------------------------------------

    if st.button(
        "🎯 Start Interview",
        use_container_width=True
    ):

        if resume is None:

            st.warning(
                "⚠️ Please upload your resume in the "
                "'Resume & Job Analysis' tab first."
            )

        elif not job_description.strip():

            st.warning(
                "⚠️ Please enter the job description in the "
                "'Resume & Job Analysis' tab first."
            )

        else:

            with st.spinner(
                "🤖 Preparing your interview..."
            ):

                # -----------------------------------------
                # Reuse Resume Analysis if available
                # -----------------------------------------

                if st.session_state.resume_analysis:

                    resume_analysis = (
                        st.session_state.resume_analysis
                    )

                else:

                    resume_text = extract_text_from_pdf(
                        resume
                    )

                    resume_analysis = analyze_resume(
                        resume_text
                    )

                    st.session_state.resume_analysis = (
                        resume_analysis
                    )

                # -----------------------------------------
                # Create New Interview
                # -----------------------------------------

                st.session_state.thread_id = str(
                    uuid.uuid4()
                )

                st.session_state.question_number = 1

                st.session_state.question = ""

                st.session_state.evaluation = ""

                st.session_state.interview_history = []

                st.session_state.final_report = {}

                st.session_state.interview_started = True

                # -----------------------------------------
                # Initial State
                # -----------------------------------------

                initial_state = {

                    "job_description":
                        job_description,

                    "resume_analysis":
                        resume_analysis,

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

                # -----------------------------------------
                # Generate First Question
                # -----------------------------------------

                result = (
                    st.session_state
                    .interview_graph
                    .invoke(

                        initial_state,

                        config={
                            "configurable": {
                                "thread_id":
                                    st.session_state.thread_id
                            }
                        }
                    )
                )

                st.session_state.question = (
                    result["question"]
                )

            st.success(
                "🎤 Interview Started!"
            )

    # -----------------------------------------------------
    # Current Question
    # -----------------------------------------------------

    if st.session_state.interview_started:

        st.divider()

        st.progress(
            min(
                st.session_state.question_number / 5,
                1.0
            )
        )

        st.subheader(
            f"❓ Question "
            f"{st.session_state.question_number} / 5"
        )

        st.info(
            st.session_state.question
        )

        # -------------------------------------------------
        # Answer
        # -------------------------------------------------

        answer = st.text_area(

            "✍️ Your Answer",

            height=200,

            placeholder="Type your answer here...",

            key=f"answer_{st.session_state.question_number}"
        )

        # -------------------------------------------------
        # Submit Answer
        # -------------------------------------------------

        if st.button(
            "📤 Submit Answer",
            use_container_width=True
        ):

            if not answer.strip():

                st.warning(
                    "⚠️ Please enter your answer."
                )

            else:

                with st.spinner(
                    "🤖 AI is evaluating your answer..."
                ):

                    # -------------------------------------
                    # Get Saved State
                    # -------------------------------------

                    current_state = (
                        st.session_state
                        .interview_graph
                        .get_state(

                            {
                                "configurable": {
                                    "thread_id":
                                        st.session_state.thread_id
                                }
                            }
                        )
                    )

                    # -------------------------------------
                    # Convert State
                    # -------------------------------------

                    state_values = dict(
                        current_state.values
                    )

                    # -------------------------------------
                    # Add Answer
                    # -------------------------------------

                    state_values["answer"] = answer

                    # -------------------------------------
                    # Evaluation Action
                    # -------------------------------------

                    state_values["action"] = "evaluate"

                    # -------------------------------------
                    # Run Evaluation
                    # -------------------------------------

                    result = (
                        st.session_state
                        .interview_graph
                        .invoke(

                            state_values,

                            config={
                                "configurable": {
                                    "thread_id":
                                        st.session_state.thread_id
                                }
                            }
                        )
                    )

                    # -------------------------------------
                    # Save Evaluation
                    # -------------------------------------

                    st.session_state.evaluation = (
                        result["evaluation"]
                    )

                    # -------------------------------------
                    # Save History
                    # -------------------------------------

                    st.session_state.interview_history = (
                        result["interview_history"]
                    )

                st.success(
                    "✅ Answer Evaluated!"
                )

        # -------------------------------------------------
        # Show Evaluation
        # -------------------------------------------------

        if st.session_state.evaluation:

            st.divider()

            st.subheader("📊 AI Evaluation")

            st.write(
                st.session_state.evaluation
            )

        # -------------------------------------------------
        # Interview History
        # -------------------------------------------------

        if st.session_state.interview_history:

            st.divider()

            st.subheader("📚 Interview History")

            for item in st.session_state.interview_history:

                with st.expander(
                    f"Question {item['question_number']}"
                ):

                    st.write("**Question:**")

                    st.write(
                        item["question"]
                    )

                    st.write("**Your Answer:**")

                    st.write(
                        item["answer"]
                    )

                    st.write("**AI Evaluation:**")

                    st.write(
                        item["evaluation"]
                    )

        # -------------------------------------------------
        # Next Question
        # -------------------------------------------------

        if (
            st.session_state.evaluation
            and len(
                st.session_state.interview_history
            ) < 5
        ):

            if st.button(
                "➡️ Next Question",
                use_container_width=True
            ):

                with st.spinner(
                    "🤖 Generating next question..."
                ):

                    # -------------------------------------
                    # Get Saved State
                    # -------------------------------------

                    current_state = (
                        st.session_state
                        .interview_graph
                        .get_state(

                            {
                                "configurable": {
                                    "thread_id":
                                        st.session_state.thread_id
                                }
                            }
                        )
                    )

                    # -------------------------------------
                    # Convert State
                    # -------------------------------------

                    state_values = dict(
                        current_state.values
                    )

                    # -------------------------------------
                    # Question Action
                    # -------------------------------------

                    state_values["action"] = "question"

                    # -------------------------------------
                    # Generate Question
                    # -------------------------------------

                    result = (
                        st.session_state
                        .interview_graph
                        .invoke(

                            state_values,

                            config={
                                "configurable": {
                                    "thread_id":
                                        st.session_state.thread_id
                                }
                            }
                        )
                    )

                    # -------------------------------------
                    # Save Question
                    # -------------------------------------

                    st.session_state.question = (
                        result["question"]
                    )

                    # -------------------------------------
                    # Clear Evaluation
                    # -------------------------------------

                    st.session_state.evaluation = ""

                    # -------------------------------------
                    # Increase Question Number
                    # -------------------------------------

                    st.session_state.question_number = (
                        len(
                            st.session_state.interview_history
                        ) + 1
                    )

                st.success(
                    "➡️ Next question generated!"
                )

        # -------------------------------------------------
        # Interview Complete
        # -------------------------------------------------

        if len(
            st.session_state.interview_history
        ) >= 5:

            st.success(
                "🎉 You have completed all 5 "
                "interview questions!"
            )

            st.info(
                "Go to the 'Final Report' tab to generate "
                "your complete interview report."
            )


# =========================================================
# TAB 4 — FINAL REPORT
# =========================================================

with tab4:

    st.header("🏆 Final Interview Report")

    if (
        st.session_state.interview_started
        and len(
            st.session_state.interview_history
        ) >= 5
    ):

        st.write(
            "Your interview is complete. Generate your "
            "AI-powered performance report."
        )

        # -------------------------------------------------
        # Generate Report
        # -------------------------------------------------

        if st.button(
            "📊 Generate Final Report",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Generating final interview report..."
            ):

                # -----------------------------------------
                # Get Saved State
                # -----------------------------------------

                current_state = (
                    st.session_state
                    .interview_graph
                    .get_state(

                        {
                            "configurable": {
                                "thread_id":
                                    st.session_state.thread_id
                            }
                        }
                    )
                )

                # -----------------------------------------
                # Convert State
                # -----------------------------------------

                state_values = dict(
                    current_state.values
                )

                # -----------------------------------------
                # Report Action
                # -----------------------------------------

                state_values["action"] = "report"

                # -----------------------------------------
                # Generate Report
                # -----------------------------------------

                result = (
                    st.session_state
                    .interview_graph
                    .invoke(

                        state_values,

                        config={
                            "configurable": {
                                "thread_id":
                                    st.session_state.thread_id
                            }
                        }
                    )
                )

                # -----------------------------------------
                # Save Report
                # -----------------------------------------

                st.session_state.final_report = (
                    result["final_report"]
                )

            st.success(
                "✅ Final interview report generated!"
            )

    elif st.session_state.interview_started:

        st.info(
            "🎤 Complete all 5 interview questions first."
        )

    else:

        st.info(
            "🎤 Start and complete an AI mock interview "
            "to generate your final report."
        )

    # -----------------------------------------------------
    # Display Final Report
    # -----------------------------------------------------

    if st.session_state.final_report:

        report = st.session_state.final_report

        st.divider()

        st.subheader("📊 Performance Overview")

        # ---------------------------------------------
        # Score Cards
        # ---------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏆 Overall Score",
                f"{report['overall_score']}/100"
            )

        with col2:

            st.metric(
                "🧠 Technical Knowledge",
                f"{report['technical_knowledge']}/100"
            )

        with col3:

            st.metric(
                "💡 Problem Solving",
                f"{report['problem_solving']}/100"
            )

        with col4:

            st.metric(
                "🗣️ Communication",
                f"{report['communication']}/100"
            )

        # ---------------------------------------------
        # Strengths
        # ---------------------------------------------

        st.subheader("💪 Strengths")

        for strength in report["strengths"]:

            st.success(
                f"✓ {strength}"
            )

        # ---------------------------------------------
        # Weaknesses
        # ---------------------------------------------

        st.subheader("⚠️ Areas to Improve")

        for weakness in report["weaknesses"]:

            st.warning(
                f"• {weakness}"
            )

        # ---------------------------------------------
        # Topics
        # ---------------------------------------------

        st.subheader("📚 Recommended Topics")

        for topic in report["topics_to_improve"]:

            st.info(
                f"📖 {topic}"
            )

        # ---------------------------------------------
        # Recommendation
        # ---------------------------------------------

        st.subheader("🎯 Final Recommendation")

        st.write(
            report["final_recommendation"]
        )

        st.divider()

        st.subheader("📥 Download Report")

        pdf_file = create_pdf_report(
            report,
            "careerpilot_interview_report.pdf"
        )

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📄 Download Interview Report",
                data=file,
                file_name="careerpilot_interview_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CareerPilot AI | Python • Streamlit • Gemini • "
    "LangChain • LangGraph • SQLite"
)
