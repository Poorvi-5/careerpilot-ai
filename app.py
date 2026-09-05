import uuid
import streamlit as st

from services.resume_parser import extract_text_from_pdf
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


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📂 CareerPilot AI")

st.sidebar.write(
    "Upload your resume and enter a job description "
    "to analyze your job readiness."
)


# =========================================================
# RESUME UPLOAD
# =========================================================

st.header("📄 Upload Resume")

resume = st.file_uploader(
    "Upload your Resume PDF",
    type=["pdf"]
)


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.header("💼 Job Description")

job_description = st.text_area(
    "Paste the Job Description here",
    height=250,
    placeholder="Paste the complete job description..."
)


# =========================================================
# ANALYZE RESUME + JOB
# =========================================================

if st.button("🔍 Analyze Resume & Job"):

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

        with st.spinner("📄 Reading resume..."):

            resume_text = extract_text_from_pdf(
                resume
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


# =========================================================
# RESUME ANALYSIS DISPLAY
# =========================================================

if st.session_state.resume_analysis:

    st.divider()

    st.header("📄 Resume Analysis")

    st.write(
        st.session_state.resume_analysis
    )


# =========================================================
# JOB DESCRIPTION ANALYSIS DISPLAY
# =========================================================

if st.session_state.jd_analysis:

    st.divider()

    st.header("💼 Job Description Analysis")

    st.write(
        st.session_state.jd_analysis
    )


# =========================================================
# SKILL MATCH DISPLAY
# =========================================================

if st.session_state.skill_match:

    st.divider()

    st.header("🎯 Resume-JD Skill Match")

    st.write(
        st.session_state.skill_match
    )


# =========================================================
# ROADMAP DISPLAY
# =========================================================

if st.session_state.roadmap:

    st.divider()

    st.header("🗺️ Personalized Learning Roadmap")

    st.write(
        st.session_state.roadmap
    )


# =========================================================
# AI MOCK INTERVIEW
# =========================================================

st.divider()

st.header("🎤 AI Mock Interview")

st.write(
    "Practice interview questions generated specifically "
    "for your resume and target job."
)


# =========================================================
# START INTERVIEW
# =========================================================

if st.button("🎯 Start Interview"):

    if resume is None:

        st.warning(
            "⚠️ Please upload your resume first."
        )

    elif not job_description.strip():

        st.warning(
            "⚠️ Please enter the job description first."
        )

    else:

        with st.spinner(
            "🤖 Preparing your interview..."
        ):

            # -----------------------------------------
            # Extract Resume
            # -----------------------------------------

            resume_text = extract_text_from_pdf(
                resume
            )


            # -----------------------------------------
            # Analyze Resume
            # -----------------------------------------

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


# =========================================================
# SHOW CURRENT QUESTION
# =========================================================

if st.session_state.interview_started:

    st.divider()

    st.subheader(
        f"❓ Question "
        f"{st.session_state.question_number}"
    )

    st.info(
        st.session_state.question
    )


    # =====================================================
    # ANSWER INPUT
    # =====================================================

    answer = st.text_area(

        "✍️ Your Answer",

        height=200,

        placeholder="Type your answer here...",

        key=f"answer_{st.session_state.question_number}"
    )


    # =====================================================
    # SUBMIT ANSWER
    # =====================================================

    if st.button("📤 Submit Answer"):

        if not answer.strip():

            st.warning(
                "⚠️ Please enter your answer."
            )

        else:

            with st.spinner(
                "🤖 AI is evaluating your answer..."
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
                # Add Candidate Answer
                # -----------------------------------------

                state_values["answer"] = answer


                # -----------------------------------------
                # Tell Graph to Evaluate
                # -----------------------------------------

                state_values["action"] = "evaluate"


                # -----------------------------------------
                # Run Evaluation
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
                # Save Evaluation
                # -----------------------------------------

                st.session_state.evaluation = (
                    result["evaluation"]
                )


                # -----------------------------------------
                # Save Interview History
                # -----------------------------------------

                st.session_state.interview_history = (
                    result["interview_history"]
                )


            st.success(
                "✅ Answer Evaluated!"
            )


# =========================================================
# SHOW CURRENT EVALUATION
# =========================================================

if st.session_state.evaluation:

    st.divider()

    st.subheader("📊 AI Evaluation")

    st.write(
        st.session_state.evaluation
    )


# =========================================================
# INTERVIEW HISTORY
# =========================================================

if (
    st.session_state.interview_started
    and st.session_state.interview_history
):

    st.divider()

    st.subheader("📚 Interview History")


    for item in st.session_state.interview_history:

        st.markdown(
            f"### Question "
            f"{item['question_number']}"
        )

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

        st.divider()


# =========================================================
# NEXT QUESTION
# =========================================================

if (
    st.session_state.interview_started
    and st.session_state.evaluation
):

    if len(
        st.session_state.interview_history
    ) >= 5:

        st.success(
            "🎉 You have completed all 5 "
            "interview questions!"
        )

        st.info(
            "You can now generate your final report."
        )

    else:

        if st.button("➡️ Next Question"):

            with st.spinner(
                "🤖 Generating next question..."
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
                # Tell Graph to Generate Question
                # -----------------------------------------

                state_values["action"] = "question"


                # -----------------------------------------
                # Generate Next Question
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
                # Save New Question
                # -----------------------------------------

                st.session_state.question = (
                    result["question"]
                )


                # -----------------------------------------
                # Clear Previous Evaluation
                # -----------------------------------------

                st.session_state.evaluation = ""


                # -----------------------------------------
                # Increase Question Number
                # -----------------------------------------

                st.session_state.question_number = (
                    len(
                        st.session_state
                        .interview_history
                    ) + 1
                )


            st.success(
                "➡️ Next question generated!"
            )


# =========================================================
# FINAL INTERVIEW REPORT
# =========================================================

if (
    st.session_state.interview_started
    and len(
        st.session_state.interview_history
    ) >= 5
):

    st.divider()

    st.subheader(
        "🏁 Interview Completed"
    )

    st.write(
        "You have completed all 5 interview questions."
    )


    if st.button(
        "📊 Generate Final Report"
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
            # Tell Graph to Generate Report
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


# =========================================================
# FINAL REPORT DISPLAY
# =========================================================

if st.session_state.final_report:

    st.divider()

    st.header(
        "📊 Final Interview Report"
    )

    report = st.session_state.final_report


    # =====================================================
    # SCORE CARDS
    # =====================================================

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


    # =====================================================
    # STRENGTHS
    # =====================================================

    st.subheader("💪 Strengths")

    for strength in report["strengths"]:

        st.success(
            f"✓ {strength}"
        )


    # =====================================================
    # WEAKNESSES
    # =====================================================

    st.subheader("⚠️ Areas to Improve")

    for weakness in report["weaknesses"]:

        st.warning(
            f"• {weakness}"
        )


    # =====================================================
    # TOPICS TO IMPROVE
    # =====================================================

    st.subheader("📚 Recommended Topics")

    for topic in report["topics_to_improve"]:

        st.info(
            f"📖 {topic}"
        )


    # =====================================================
    # FINAL RECOMMENDATION
    # =====================================================

    st.subheader("🎯 Final Recommendation")

    st.write(
        report["final_recommendation"]
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CareerPilot AI | Python • Streamlit • Gemini • "
    "LangChain • LangGraph • SQLite"
)