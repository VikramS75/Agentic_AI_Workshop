# Smart Content Creation: Agentic AI Content Refinement

## 🚀 Overview
This project simulates a two-agent conversation for content creation and refinement using a reflection-based agentic pattern. It utilizes **Google Gemini AI** and **Streamlit** to build an interactive web app where:

- A **Content Creator Agent** drafts content on Generative AI.
- A **Content Critic Agent** evaluates and provides feedback for iterative refinement.

## 🎯 Objectives
- **Draft Content:** Content Creator Agent writes on a user-specified topic (default: *Agentic AI*).
- **Evaluate Content:** Content Critic Agent reviews for clarity and technical accuracy.
- **Refine via Feedback:** Critic suggests improvements; Creator revises accordingly.
- **Iterate with Reflection:** Process continues for 3–5 user-selected turns, producing a refined final draft.

## ✨ Features
- **Two-Agent Simulation:** Interactive dialogue between Creator and Critic agents.
- **Modern UI:** Chat-style interface with avatars, bubbles, and sleek layout.
- **Interactive Sidebar:** Choose topic and number of iterations (turns).
- **Progress Tracking:** Visual progress bar with simulation status.
- **Final Output:** View and download the refined markdown content.
- **Conversation History:** Full log shown for transparency and learning.

## ⚙️ Getting Started

### Prerequisites
- Python 3.8+
- [Google Gemini API Key](https://ai.google.dev/)

### Installation
```bash
# Clone the repository and navigate to the directory
git clone <your-repo-url>
cd "13) Smart Content Creation/"

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Update the code to use your API key from an environment variable (recommended for security).

### Run the App
```bash
streamlit run app.py
```

## 🧠 Usage
1. Choose a topic (default: *Agentic AI*) in the sidebar.
2. Select the number of turns (3 or 5).
3. Click **🚀 Start Simulation**.
4. View, download, and review the final content and conversation history.

## 🗨️ Example Agent Roles

- **Content Creator Agent:**  
  > You are the Content Creator Agent. Draft clear, concise, and technically accurate content on Generative AI topics.

- **Content Critic Agent:**  
  > You are the Content Critic Agent. Evaluate the drafted content for clarity and correctness. Suggest improvements.

## 🙌 Credits
- Built using [Streamlit](https://streamlit.io/) and [Google Gemini AI](https://ai.google.dev/).
- UI inspired by modern chat and agentic interaction patterns.

## 📄 License
This project is intended for educational and demonstration purposes only.
