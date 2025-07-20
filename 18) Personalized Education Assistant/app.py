import os
import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import google.generativeai as genai
import requests
import re
import streamlit as st

GEMINI_API_KEY = "AIzaSyCyGhGV5y7IUvXmF_ZpjFeCBemACPdvMGY"
SERPER_API_KEY = "ec041ae5b30ab472d64b108fe77af07d1d180609"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Helper Functions
def search_learning_materials(topic: str) -> Dict[str, Any]:
    """Search for learning materials on a given topic."""
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        
        # Search for videos
        video_query = f"{topic} tutorial video"
        video_results = requests.post(url, json={"q": video_query}, headers=headers).json()
        
        # Search for articles
        article_query = f"{topic} guide article"
        article_results = requests.post(url, json={"q": article_query}, headers=headers).json()
        
        # Search for exercises
        exercise_query = f"{topic} practice exercises"
        exercise_results = requests.post(url, json={"q": exercise_query}, headers=headers).json()
        
        videos = []
        articles = []
        exercises = []
        
        # Extract videos
        for v in video_results.get("organic", [])[:3]:
            videos.append(f"{v['title']}: {v['link']}")
        
        # Extract articles
        for a in article_results.get("organic", [])[:3]:
            articles.append(f"{a['title']}: {a['link']}")
            
        # Extract exercises
        for e in exercise_results.get("organic", [])[:3]:
            exercises.append(f"{e['title']}: {e['link']}")
        
        return {
            "topic": topic,
            "videos": videos,
            "articles": articles,
            "exercises": exercises
        }
    except Exception as e:
        return {
            "topic": topic,
            "videos": [f"Error searching videos: {str(e)}"],
            "articles": [f"Error searching articles: {str(e)}"],
            "exercises": [f"Error searching exercises: {str(e)}"]
        }

def generate_quiz_questions(topic: str) -> List[Dict[str, Any]]:
    """Generate quiz questions on a given topic."""
    try:
        prompt = f"""Create 3 multiple-choice questions about {topic}. Format each question as follows:

Question: [Your question here]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Answer: [Correct option letter]

Make sure the questions are clear and educational."""
        
        response = model.generate_content(prompt).text
        questions = []
        
        # Parse the response
        question_blocks = response.split("Question:")
        for block in question_blocks[1:]:  # Skip first empty element
            lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
            if len(lines) >= 6:
                question = lines[0]
                options = []
                answer_line = ""
                
                for line in lines[1:]:
                    if line.startswith(('A)', 'B)', 'C)', 'D)')):
                        options.append(line[3:].strip())
                    elif line.startswith("Answer:"):
                        answer_line = line.split(":")[-1].strip()
                
                if len(options) == 4 and answer_line:
                    # Convert answer letter to actual answer text
                    answer_index = ord(answer_line.upper()) - ord('A')
                    if 0 <= answer_index < 4:
                        questions.append({
                            "question": question,
                            "options": options,
                            "answer": options[answer_index]
                        })
        
        return questions[:3]
    except Exception as e:
        return [{"question": f"Error generating quiz: {str(e)}", "options": ["Error", "Error", "Error", "Error"], "answer": "Error"}]

def suggest_projects(topic: str, level: str) -> List[Dict[str, Any]]:
    """Generate project ideas based on topic and expertise level."""
    try:
        prompt = f"""Suggest 3 practical project ideas for someone at a {level} level learning about {topic}.
For each project, provide:
- A clear title
- A detailed description explaining what the project involves
- Why it's suitable for {level} level

Format each project as:
Project: [Title]
Description: [Detailed description]
"""
        
        response = model.generate_content(prompt).text
        projects = []
        
        # Parse the response
        project_blocks = response.split("Project:")
        for block in project_blocks[1:]:  # Skip first empty element
            lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
            
            title = lines[0] if lines else "Untitled Project"
            description = ""
            
            for line in lines[1:]:
                if line.startswith("Description:"):
                    description = line.split(":", 1)[1].strip()
                    break
            
            if description:
                projects.append({
                    "title": title,
                    "description": description,
                    "level": level
                })
        
        return projects[:3]
    except Exception as e:
        return [{"title": f"Error generating projects: {str(e)}", "description": "Unable to generate project suggestions", "level": level}]

# Execution function
def generate_learning_path(topic: str, level: str):
    """Generate a complete learning path for the given topic and level."""
    
    try:
        # Directly call helper functions
        learning_materials = search_learning_materials(topic)
        quiz_questions = generate_quiz_questions(topic)
        project_ideas = suggest_projects(topic, level)

        return {
            "learning_materials": learning_materials,
            "quiz_questions": quiz_questions,
            "project_ideas": project_ideas
        }
    except Exception as e:
        st.error(f"❌ Error generating content: {str(e)}")
        return {
            "learning_materials": {},
            "quiz_questions": [],
            "project_ideas": []
        }

# Streamlit UI
def main():
    st.set_page_config(page_title="Personalized Learning Assistant", page_icon="🎓", layout="wide")

    # Sidebar with app info and instructions
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=80)
        st.title("🎓 EduPath AI")
        st.markdown("""
        <div style='font-size: 16px;'>
        <b>Welcome to EduPath AI!</b><br>
        <ul>
        <li>Enter your learning topic and skill level</li>
        <li>Get curated materials, quizzes, and project ideas</li>
        <li>Powered by Google Gemini & Serper API</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.info("Tip: Try topics like 'Python Programming', 'Machine Learning', or 'Data Science'!")

    st.markdown("""
        <style>
        .big-title { font-size: 3rem; font-weight: 700; color: #2E86C1; }
        .subtitle { font-size: 1.3rem; color: #555; }
        .stButton>button { background-color: #2E86C1; color: white; font-size: 1.1rem; border-radius: 8px; }
        .stTabs [data-baseweb="tab"] { font-size: 1.1rem; }
        .section-container { background: #F4F8FB; border-radius: 12px; padding: 2rem 2rem 1.5rem 2rem; margin-bottom: 2rem; box-shadow: 0 2px 8px #e3e3e3; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="big-title">🎓 Personalized Learning Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate comprehensive learning materials, quizzes, and project ideas for any topic!</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Input area in a colored container
    with st.container():
        # st.markdown('<div class="section-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            topic = st.text_input("📚 Enter your learning topic:", placeholder="e.g., Machine Learning, Python, Data Science")
        with col2:
            level = st.selectbox("📊 Select your skill level:", ["Beginner", "Intermediate", "Advanced"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Generate button centered
    col_btn = st.columns([2, 1, 2])
    with col_btn[1]:
        generate = st.button("🚀 Generate My Learning Path", type="primary")

    if generate:
        if not topic.strip():
            st.error("Please enter a topic to learn about.")
            return
        with st.spinner("🔍 Creating your personalized learning path..."):
            result = generate_learning_path(topic, level)
            if result:
                st.success("✅ Learning path generated successfully!")
                st.markdown("---")
                tab1, tab2, tab3 = st.tabs([
                    "📚 Learning Materials",
                    "📝 Quiz",
                    "🚀 Project Ideas"
                ])
                with tab1:
                    st.subheader("📚 Learning Materials")
                    learning_materials = result.get("learning_materials", {})
                    if learning_materials.get("videos"):
                        st.markdown("### 🎥 Videos")
                        for video in learning_materials["videos"]:
                            st.write(f"• {video}")
                    if learning_materials.get("articles"):
                        st.markdown("### 📄 Articles")
                        for article in learning_materials["articles"]:
                            st.write(f"• {article}")
                    if learning_materials.get("exercises"):
                        st.markdown("### 💪 Exercises")
                        for exercise in learning_materials["exercises"]:
                            st.write(f"• {exercise}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with tab2:
                    st.subheader("📝 Quiz Questions")
                    quiz_questions = result.get("quiz_questions", [])
                    if quiz_questions:
                        for i, q in enumerate(quiz_questions, 1):
                            st.markdown(f"**Question {i}: {q['question']}**")
                            for j, option in enumerate(q['options'], 1):
                                st.write(f"   {chr(64+j)}) {option}")
                            st.write(f"**✅ Correct Answer:** {q['answer']}")
                            st.markdown("---")
                    else:
                        st.write("No quiz questions generated.")
                    st.markdown('</div>', unsafe_allow_html=True)
                with tab3:
                    st.subheader("🚀 Project Ideas")
                    project_ideas = result.get("project_ideas", [])
                    if project_ideas:
                        for i, project in enumerate(project_ideas, 1):
                            st.markdown(f"### Project {i}: {project['title']}")
                            st.write(f"**Description:** {project['description']}")
                            st.write(f"**Level:** {project['level']}")
                            st.markdown("---")
                    else:
                        st.write("No project ideas generated.")
                    st.markdown('</div>', unsafe_allow_html=True)
                if result.get("raw_result"):
                    with st.expander("🔍 View Raw AI Output"):
                        st.text(str(result["raw_result"]))
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 1.1rem;'>
            <p>🤖 Powered by <b>Google Gemini AI</b> | 🔍 Web Search via <b>Serper API</b></p>
            <p>💡 This tool generates learning materials, quizzes, and project ideas for any topic</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()