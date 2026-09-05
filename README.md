# 🚀 CareerPilot AI

**CareerPilot AI** is an agentic AI-powered career assistant that analyzes a candidate's resume against a job description, identifies skill gaps, generates a personalized learning roadmap, and conducts an adaptive AI mock interview.

## ✨ Features

* 📄 Resume PDF parsing
* 🤖 AI-powered resume analysis
* 💼 Job description analysis
* 🎯 Resume–JD skill matching
* 📊 Job readiness score
* ⚠️ Missing skill identification
* 🗺️ Personalized 4-week learning roadmap
* 🎤 AI-powered mock interview
* 🧠 Adaptive interview questions based on previous performance
* 📋 AI answer evaluation
* 📊 Final interview performance report
* 💾 Persistent interview state using LangGraph checkpoints
* 🧵 Thread-based interview sessions

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Resume + JD Input │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
      ┌───────────────┐                 ┌───────────────┐
      │ Resume Parser │                 │  JD Analyzer  │
      └───────┬───────┘                 └───────┬───────┘
              │                                 │
              └──────────────┬──────────────────┘
                             ▼
                    ┌─────────────────────┐
                    │   Skill Matcher     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Roadmap Generator   │
                    └─────────────────────┘

                    AI Mock Interview
                           │
                           ▼
                    ┌─────────────────────┐
                    │     LangGraph       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       Generate Question   Evaluate Answer   Final Report
              │                │                │
              └────────────────┴────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ SQLite Checkpoints  │
                    └─────────────────────┘
```

## 🛠️ Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core programming language       |
| Streamlit     | Web interface                   |
| PyMuPDF       | Resume PDF text extraction      |
| Gemini        | Large Language Model            |
| LangChain     | LLM integration                 |
| LangGraph     | Agentic interview workflow      |
| SQLite        | Persistent checkpoints          |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
careerpilot-ai/
│
├── agents/
│   ├── __init__.py
│   └── interview_agent.py
│
├── services/
│   ├── llm_service.py
│   ├── resume_parser.py
│   ├── resume_analyzer.py
│   ├── jd_analyzer.py
│   ├── skill_matcher.py
│   ├── roadmap_generator.py
│   ├── answer_evaluator.py
│   └── interview_report.py
│
├── graph/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   └── workflow.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Poorvi-5/careerpilot-ai.git
cd careerpilot-ai
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Setup

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_gemini_api_key
```

Never commit the `.env` file to GitHub.

## ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🎯 Workflow

### 1. Resume Analysis

Upload a resume PDF.

CareerPilot AI extracts and analyzes:

* Education
* Skills
* Experience
* Projects
* Certifications

### 2. Job Description Analysis

Paste the target job description.

The system extracts:

* Required skills
* Preferred skills
* Experience requirements
* Responsibilities

### 3. Skill Matching

The system compares the resume with the job description and provides:

* Match score
* Matched skills
* Missing skills
* Extra skills
* Recommendation

### 4. Personalized Roadmap

Based on missing skills, CareerPilot AI generates a practical 4-week learning roadmap.

### 5. AI Mock Interview

The system generates interview questions based on the candidate's resume and target job.

After each answer, the AI evaluates:

* Correctness
* Technical depth
* Relevance
* Communication

The next question can adapt according to the candidate's previous performance.

### 6. Final Report

After completing the interview, CareerPilot AI generates an overall performance report containing:

* Overall score
* Technical knowledge
* Problem-solving
* Communication
* Strengths
* Weaknesses
* Topics to improve
* Final recommendation

## 🧠 Agentic Workflow

CareerPilot AI uses **LangGraph** to manage the interview workflow.

```text
START
  │
  ▼
Generate Question
  │
  ▼
Candidate Answer
  │
  ▼
Evaluate Answer
  │
  ▼
Next Question
  │
  ▼
Repeat
  │
  ▼
Final Report
```

Interview state is persisted using SQLite checkpoints, allowing the workflow to maintain state for a specific interview thread.

## 🔮 Future Improvements

* 🔎 Resume and job-description RAG
* 📚 FAISS/Chroma vector database
* 🧠 More advanced multi-agent architecture
* 🎙️ Voice-based mock interviews
* 📈 Interview performance analytics
* 📄 AI resume improvement suggestions
* 🌐 Cloud deployment
* 🔐 User authentication
* 💾 Persistent user profiles
* 📊 Interactive dashboards

## 👩‍💻 Author

**Poorvi Sharma**

CSE-AIML | Artificial Intelligence & Machine Learning

---

⭐ If you find this project useful, consider giving the repository a star!
