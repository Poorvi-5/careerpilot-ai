# 🎯 CareerPilot AI

### Agentic Resume & Interview Intelligence System

CareerPilot AI is an AI-powered career assistant that analyzes a candidate's resume against a job description, identifies skill gaps, generates a personalized learning roadmap, and conducts an adaptive technical mock interview.

The system combines **LLMs, RAG, FAISS, LangGraph, and Streamlit** to create an end-to-end AI career intelligence platform.

---

## 🚀 Features

* 📄 Resume PDF parsing
* 🧠 AI-powered resume analysis
* 💼 Job description analysis
* 🎯 Resume-to-JD skill matching
* 📊 Match score and missing skills identification
* 🗺️ Personalized 4-week learning roadmap
* 🔎 RAG-based resume knowledge retrieval
* 🤖 Adaptive AI mock interview
* 📝 AI answer evaluation
* 🔄 Difficulty adaptation based on previous answers
* 🧩 LangGraph agentic workflow
* 💾 SQLite checkpoint-based persistence
* 📊 Final interview performance dashboard
* 📄 Downloadable interview PDF report
* ⚠️ Centralized Gemini API error handling

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      Streamlit      │
                    │         UI          │
                    └──────────┬──────────┘
                               │
                 ┌─────────────▼─────────────┐
                 │     Resume + Job Input    │
                 └─────────────┬─────────────┘
                               │
              ┌────────────────▼────────────────┐
              │       Resume PDF Parser         │
              └────────────────┬────────────────┘
                               │
          ┌────────────────────▼────────────────────┐
          │             Gemini LLM                  │
          │                                         │
          │ Resume Analysis                         │
          │ JD Analysis                             │
          │ Skill Matching                          │
          │ Roadmap Generation                      │
          └────────────────────┬────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    FAISS + RAG      │
                    │ Resume Knowledge    │
                    │      Retrieval      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │     LangGraph       │
                    │  Interview Agent    │
                    └──────────┬──────────┘
                               │
              ┌────────────────▼────────────────┐
              │      Adaptive Interview        │
              │                                 │
              │ Question → Answer → Evaluation │
              │          → Next Question        │
              └────────────────┬────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Final Report      │
                    │ Dashboard + PDF     │
                    └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Frontend

* Streamlit
* HTML/CSS

### AI / LLM

* Google Gemini
* LangChain
* LangGraph

### RAG

* FAISS
* Google Generative AI Embeddings
* Recursive Character Text Splitter

### Document Processing

* PyMuPDF

### Persistence

* SQLite
* LangGraph Checkpointer

### Reporting

* ReportLab

---

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
│   ├── interview_report.py
│   ├── pdf_report.py
│   └── rag_service.py
│
├── graph/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   └── workflow.py
│
├── app.py
├── style.css
├── requirements.txt
├── .env
├── .gitignore
└── careerpilot_checkpoints.db
```

---

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Poorvi-5/careerpilot-ai.git
cd careerpilot-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_gemini_api_key
```

Never commit the `.env` file to GitHub.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔄 Application Workflow

### 1. Resume & Job Analysis

Upload a resume PDF and paste a job description.

CareerPilot AI:

* Extracts resume text
* Analyzes candidate information
* Analyzes job requirements
* Compares required and available skills
* Generates a skill match score

### 2. Learning Roadmap

Based on missing skills, the system generates a personalized 4-week learning roadmap containing:

* Skills to learn
* Topics
* Practice tasks
* Mini projects
* Final project
* Interview preparation

### 3. AI Mock Interview

The candidate starts a 5-question technical interview.

The system:

```text
Generate Question
       ↓
Candidate Answer
       ↓
AI Evaluation
       ↓
Analyze Performance
       ↓
Generate Next Question
```

The next question adapts according to the candidate's previous performance.

### 4. RAG

Resume information is converted into embeddings and stored in FAISS.

During the interview, relevant resume information is retrieved and supplied to the interviewer agent.

This helps the interviewer ask questions based on the candidate's actual resume.

### 5. Final Report

After five questions, CareerPilot AI generates:

* Overall score
* Technical knowledge score
* Problem-solving score
* Communication score
* Strengths
* Weaknesses
* Topics to improve
* Final recommendation

A PDF report can also be generated.

---

## 🧠 Agentic Workflow

LangGraph manages the interview workflow.

```text
START
  │
  ▼
Retrieve Resume Context
  │
  ▼
Generate Interview Question
  │
  ▼
Candidate Answers
  │
  ▼
Evaluate Answer
  │
  ├──────► Next Question
  │
  ▼
Generate Final Report
  │
  ▼
END
```

The workflow uses **state management, conditional routing, checkpoints, and an adaptive interviewer agent**.

---

## 🔐 Security

Sensitive configuration is stored in environment variables.

The following files are excluded from Git:

```text
.env
venv/
__pycache__/
*.pyc
careerpilot_checkpoints.db
```

---

## 🎯 Future Improvements

* Voice-based mock interviews
* Resume improvement suggestions
* Multiple interview modes
* Company-specific interview preparation
* Job recommendation system
* Advanced analytics dashboard
* Cloud deployment
* Authentication and user profiles
* Long-term candidate memory
* Multi-agent career planning

---

## 👩‍💻 Author

**Poorvi Sharma**

CSE-AIML Student

---

## ⭐ Project Goal

CareerPilot AI aims to provide a complete AI-powered career preparation workflow — from **resume analysis and skill-gap detection to personalized learning and adaptive interview preparation**.
