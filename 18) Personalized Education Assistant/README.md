# 🎓 Personalized Education Assistant

A modern, interactive Streamlit app that provides personalized educational recommendations, curated learning materials, quizzes, and project ideas tailored to your topics of interest and expertise level.

---

## 🚀 Overview
This app leverages **Google Gemini AI** and the **Serper API** to help users:
- Discover high-quality learning materials (videos, articles, exercises)
- Test their understanding with personalized quizzes
- Get practical project ideas based on their skill level

All in a visually appealing, user-friendly interface.

---

## ✨ Features
- **Content Selection:** Curated learning materials for any topic
- **Quiz Generation:** Multiple-choice quizzes to test your knowledge
- **Project Suggestions:** Practical project ideas for beginner, intermediate, or advanced learners
- **Modern UI:** Sidebar, colored containers, icons, and responsive layout

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "18) Personalized Education Assistant"
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys
- **Serper API Key:** Used for Google search results
- **Gemini API Key:** Used for Google Gemini AI (or replace with OpenAI if desired)

You can set these as environment variables:
```bash
export SERPER_API_KEY=your_serper_api_key
export GEMINI_API_KEY=your_gemini_api_key
```

Or edit the variables at the top of `app.py` (not recommended for production).

---

## ▶️ Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

1. Enter your learning topic (e.g., "Python Programming")
2. Select your skill level (Beginner, Intermediate, Advanced)
3. Click **"Generate My Learning Path"**
4. Explore the tabs for learning materials, quizzes, and project ideas

---

## 🔑 How to Get API Keys

### Serper API Key
1. Go to [Serper](https://serper.dev/) and sign up
2. Generate your API key from the dashboard

### Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and sign in
2. Create and copy your Gemini API key

---

## 📦 Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

---

## 🙏 Credits
- [Streamlit](https://streamlit.io/)
- [Google Gemini AI](https://ai.google.dev/)
- [Serper API](https://serper.dev/)