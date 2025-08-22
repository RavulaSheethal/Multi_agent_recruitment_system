This project implements a multi-agent system for intelligent recruitment.
The system simulates the recruitment process by profiling candidates, designing assessments, analyzing behavior, and optimizing market insights.
It demonstrates how AI agents can collaborate to make hiring more efficient, unbiased, and scalable.

##System Architecture

The solution is built around four specialized agents:
Candidate Profiler
Generates a Talent Intelligence Report (TIR) for each candidate.
Extracts skills, past experiences, and gaps from synthetic profiles.
Assessment Designer
Creates technical assessments tailored to the candidate’s background.
Provides scoring rubrics for objective evaluation.
Behavioral Analyzer
Analyzes behavioral snippets (simulated conversations).
Extracts communication style, teamwork, leadership, and problem-solving signals.
Market Optimizer
Provides market insights like sourcing opportunities and role demand.
Helps align recruitment strategy with current market trends.

Flow: Candidate Data → Candidate Profiler → Assessment Designer and Behavioral Analyzer → Market Optimizer → Reports

##Repository Structure

Multi_agent_recruitment_system/

data → Contains synthetic datasets used for the demo.

synthetic_profiles.jsonl – synthetic candidate profiles.

reports → Stores generated output reports in JSON and Markdown formats.

src → Core source code for the project.

agents → Individual AI agents.

candidate_profiler.py – Extracts candidate skills & generates Talent Intelligence Report.

assessment_designer.py – Creates challenges, rubrics, and bias mitigation protocols.

behavioral_analyzer.py – Analyzes candidate communication for soft skills.

market_optimizer.py – Provides salary benchmarks & sourcing insights.

shared → Utilities and shared schemas.

nlp_utils.py – Common NLP helper functions.

schemas.py – Data models to ensure consistent structure.

appcli.py → Command Line Interface (entry point for running agents).

requirements.txt → Python dependencies.


##Setup Instructions

Clone Repository

git clone https://github.com/RavulaSheethal/Multi_agent_recruitment_system.git

cd Multi_agent_recruitment_system

Create Virtual Environment

python -m venv .venv

..venv\Scripts\activate (On Windows)

source .venv/bin/activate (On Mac/Linux)

Install Dependencies

pip install -r requirements.txt

##Usage Guide

Generate Candidate Profile

python -m app.cli profile --candidate_id cand_001

Run Assessment Designer

python -m app.cli assess --candidate_id cand_001

Run Behavioral Analyzer

python -m app.cli behavior --candidate_id cand_001

Get Market Insights

python -m app.cli market --role "ML Engineer" --location "IN-HYD"

Reports are saved under the reports/ folder in both JSON and Markdown formats.

Bias Mitigation

Demographics excluded. Only skills, experience, and behavior are analyzed.

Assessments tailored to roles, not personal background.

Ensures fairness and transparency in candidate evaluation.

##Future Improvements

Add a Streamlit or Flask UI for live interaction.
Expand synthetic dataset to include more diverse roles and behaviors.
Integrate with real-world job boards or ATS for sourcing candidates.
Deploy via Streamlit Cloud or Docker for public access.

