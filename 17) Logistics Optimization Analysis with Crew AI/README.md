# 🚚 Logistics Optimization Analysis with Crew AI

## Overview
This project is an AI-powered logistics optimization tool leveraging Crew AI agents to analyze logistics data and develop actionable strategies. It solves real-world logistics problems such as delivery route optimization and inventory management enhancement. Simply input a list of products and receive AI-generated insights for efficient logistics planning.

## ✨ Key Features
- **Multi-Agent Collaboration:** Two specialized AI agents (Logistics Analyst & Optimization Strategist) work together for thorough analysis and optimization.
- **Customizable Product Input:** Enter any list of products to tailor the logistics analysis to your context.
- **Modern Streamlit UI:** A clean and interactive interface using Streamlit.
- **Actionable Output:** Detailed optimization strategies derived from AI analysis.

## 🧠 How It Works
1. **Logistics Analyst Agent**
   - Examines logistics operations, focusing on delivery routes and inventory turnover.
2. **Optimization Strategist Agent**
   - Develops a data-driven strategy based on the analyst’s insights.
3. **Crew AI Workflow**
   - Agents collaborate to deliver a complete logistics optimization plan.

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <repo-url>
cd "17) Logistics Optimization Analysis with Crew AI"
```

### 2. Install Dependencies
Use a virtual environment if possible:
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key
The Google Gemini API key is currently hardcoded in `app.py`. For secure deployment, use environment variables.

### 4. Run the App
```bash
streamlit run app.py
```

## 🖥️ Usage
1. Launch the Streamlit app (typically at `http://localhost:8501`).
2. Enter products as a comma-separated list.
3. Click on **🚀 Optimize Logistics**.
4. View detailed logistics analysis and strategies.

## 📦 Requirements
- Python 3.8 or higher
- All dependencies listed in `requirements.txt`

## 🤖 Technologies Used
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Streamlit](https://streamlit.io/)
- [Gemini LLM](https://ai.google.dev/)
