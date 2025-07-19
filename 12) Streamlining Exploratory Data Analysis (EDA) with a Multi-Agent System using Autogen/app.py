import os
import pandas as pd
import streamlit as st
import google.generativeai as genai
from autogen.agentchat import (
    AssistantAgent,
    UserProxyAgent,
    GroupChat,
    GroupChatManager,
)

api_key = "AIzaSyC7K1mPTvB9WDVC06u31HlkvBzH0hMOdbA"
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please provide your API key.")

genai.configure(api_key=api_key)

def gemini_call(prompt, model_name="models/gemini-1.5-flash"):
    return genai.GenerativeModel(model_name).generate_content(prompt).text

# ===== Agent Definitions =====
class DataPrepAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        df = st.session_state["df"]
        prompt = f"""You are a Data Cleaning Agent.
- Handle missing values
- Fix data types
- Remove duplicates

Dataset head:
{df.head().to_string()}

Summary stats:
{df.describe(include='all').to_string()}

Return Python code for preprocessing and a short explanation."""
        return gemini_call(prompt)

class EDAAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        df = st.session_state["df"]
        prompt = f"""You are an EDA Agent.
- Provide summary statistics
- Extract at least 3 insights
- Suggest visualizations

Dataset head:
{df.head().to_string()}"""
        return gemini_call(prompt)

class ReportGeneratorAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        insights = st.session_state.get("eda_output", "")
        prompt = f"""You are a Report Generator.
Create a clean EDA report based on insights:

{insights}

Include:
- Overview
- Key Findings
- Visual Suggestions
- Summary conclusion."""
        return gemini_call(prompt)

class CriticAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        report = st.session_state.get("report_output", "")
        prompt = f"""You are a Critic Agent.
Review the EDA report:

{report}

Comment on clarity, accuracy, completeness, and suggest improvements."""
        return gemini_call(prompt)

class ExecutorAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        code = st.session_state.get("prep_output", "")
        prompt = f"""You are an Executor Agent.
Validate the following data preprocessing code:

{code}

- Is it runnable?
- Suggest corrections if needed."""
        return gemini_call(prompt)

# ===== Admin / Proxy Agent =====
admin_agent = UserProxyAgent(
    name="Admin",
    human_input_mode="NEVER",
    code_execution_config=False  # disables Docker requirement
)

# ===== Streamlit UI =====
st.set_page_config(layout="wide", page_title="Agentic EDA with Gemini + Autogen", page_icon="🔍")

# Custom CSS for enhanced visuals
def set_custom_style():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stButton>button {
            background: linear-gradient(90deg, #4f8cff 0%, #6dd5ed 100%);
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 2em;
            font-size: 1.1em;
        }
        .stExpanderHeader {
            font-size: 1.1em;
            color: #4f8cff;
        }
        .stDataFrame, .stTable {
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(79,140,255,0.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
set_custom_style()

st.markdown("""
<div style='display: flex; align-items: center; gap: 1rem;'>
    <span style='font-size: 2.5rem;'>🔍</span>
    <span style='font-size: 2.2rem; font-weight: 700; color: #4f8cff;'>Agentic EDA with Gemini + Autogen</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='font-size:1.1rem; color:#333; margin-bottom:1.5rem;'>
    <b>Automate and streamline your Exploratory Data Analysis (EDA) with a collaborative multi-agent system powered by Google Gemini and Autogen.</b><br>
    <ul>
        <li>Upload your CSV dataset</li>
        <li>Let specialized AI agents clean, analyze, and report on your data</li>
        <li>Get actionable insights, visual suggestions, and expert feedback</li>
    </ul>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("📁 Upload your CSV file", type=["csv"], help="Upload a CSV file to begin EDA.")

if uploaded:
    df = pd.read_csv(uploaded)
    st.session_state["df"] = df
    st.subheader("📄 Raw Dataset Preview")
    st.dataframe(df.head(), use_container_width=True, hide_index=True)

    st.markdown("""
    <div style='margin: 1.5em 0 1em 0; text-align:center;'>
        <span style='font-size:1.3em; color:#4f8cff;'>Ready to analyze your data?</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        run_eda = st.button("🚀 Run Agentic EDA", use_container_width=True)

    if run_eda:
        with st.spinner("Initializing agents..."):
            agents = [
                admin_agent,
                DataPrepAgent(name="DataPrep"),
                EDAAgent(name="EDA"),
                ReportGeneratorAgent(name="ReportGen"),
                CriticAgent(name="Critic"),
                ExecutorAgent(name="Executor"),
            ]
            chat = GroupChat(agents=agents, messages=[])
            manager = GroupChatManager(groupchat=chat)

        with st.spinner("Running multi-agent system..."):
            # ===== Data Preparation Output =====
            prep = agents[1].generate_reply([], "Admin")
            st.session_state["prep_output"] = prep
            with st.expander("🧹 Data Preparation Output", expanded=True):
                st.markdown("**Python Code:**", unsafe_allow_html=True)
                st.code(prep, language="python")

            # ===== EDA Agent Output =====
            eda_out = agents[2].generate_reply([], "Admin")
            st.session_state["eda_output"] = eda_out
            with st.expander("📊 EDA Insights", expanded=True):
                st.markdown(eda_out, unsafe_allow_html=True)

            # ===== Report Generation =====
            report = agents[3].generate_reply([], "Admin")
            st.session_state["report_output"] = report
            with st.expander("📄 EDA Report", expanded=True):
                st.markdown(report, unsafe_allow_html=True)

            # ===== Critic Feedback =====
            critique = agents[4].generate_reply([], "Admin")
            with st.expander("🧐 Critic Agent Feedback", expanded=False):
                st.markdown(critique, unsafe_allow_html=True)

            # ===== Code Execution Check =====
            exec_feedback = agents[5].generate_reply([], "Admin")
            with st.expander("✅ Executor Agent Validation", expanded=False):
                st.markdown(exec_feedback, unsafe_allow_html=True)

        st.success("✔️ Agentic EDA completed successfully.", icon="✅")
else:
    st.info("Upload a CSV file above to begin.", icon="📁")