import os
import streamlit as st
from PIL import Image
import tempfile
import json
import google.generativeai as genai
from autogen.agentchat import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

GEMINI_API_KEY = "AIzaSyCyGhGV5y7IUvXmF_ZpjFeCBemACPdvMGY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- UI CONFIG ---
st.set_page_config(page_title="🧾 Bill Management Agent", layout="wide")

# Custom CSS for a modern, card-based, vibrant look
st.markdown("""
    <style>
    body { background: linear-gradient(120deg, #f8fafc 0%, #e0e7ff 100%) !important; }
    .main { background: transparent !important; }
    .title-container {
        display: flex; align-items: center; gap: 18px; margin-bottom: 0.5em;
    }
    .title-icon {
        font-size: 2.5em; background: #6366f1; color: #fff; border-radius: 50%; padding: 0.2em 0.4em;
        box-shadow: 0 2px 8px #6366f133;
    }
    .big-title {
        font-size: 2.2em; font-weight: 800; color: #3730a3; letter-spacing: 1px;
    }
    .subtitle {
        font-size: 1.1em; color: #6366f1; margin-bottom: 1.5em;
    }
    .category-card {
        background: linear-gradient(90deg, #e0e7ff 0%, #f1f5f9 100%);
        border-radius: 14px; padding: 1.2em 1.5em; margin-bottom: 1.2em;
        box-shadow: 0 2px 8px #6366f111;
    }
    .category-title {
        font-size: 1.2em; font-weight: 700; color: #4f46e5; margin-bottom: 0.5em;
    }
    .expense-item {
        font-size: 1.05em; color: #22223b; margin-left: 1em;
    }
    .summary-box {
        background: linear-gradient(90deg, #f3e8ff 0%, #e0e7ff 100%);
        border-radius: 16px; padding: 1.5em; margin-bottom: 2em;
        box-shadow: 0 2px 12px #a78bfa22;
        font-size: 1.1em; color: #6d28d9;
    }
    .chat-log-title {
        font-size: 1.2em; font-weight: 700; color: #6366f1; margin-top: 2em;
    }
    .user {
        background: #e0f2fe; color: #0c4a6e; padding: 12px; border-radius: 10px; margin-bottom: 10px;
        border-left: 5px solid #38bdf8;
    }
    .agent {
        background: #ede9fe; color: #5b21b6; padding: 12px; border-radius: 10px; margin-bottom: 10px;
        border-left: 5px solid #a78bfa;
    }
    .footer {
        margin-top: 2em; color: #a1a1aa; font-size: 0.95em; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title and Subtitle ---
st.markdown('<div class="title-container"><span class="title-icon">🧾</span><span class="big-title">AI Bill Management Agent</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your bill and let AI categorize and analyze your expenses with beautiful insights.</div>', unsafe_allow_html=True)

# --- Upload File Card ---
uploaded_file = st.file_uploader("📤 Upload your bill", type=["jpg", "jpeg", "png"], label_visibility="visible")
st.markdown('</div>', unsafe_allow_html=True)

chat_log = []

def process_bill_with_gemini(image_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image_file.read())
        tmp_path = tmp.name
    image = Image.open(tmp_path)
    response = model.generate_content([
        "Extract all expenses from this bill image. Group them into categories: Groceries, Dining, Utilities, Shopping, Entertainment, Others. Return as JSON format like {category: [{item, cost}]}",
        image
    ])
    try:
        text = response.text.strip()
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        data = json.loads(text[json_start:json_end])
        return data, response.text
    except Exception as e:
        return None, response.text

def summarize_expenses_with_gemini(expenses):
    prompt = (
        f"Given the following categorized expenses: {expenses}, "
        "summarize the total expenditure, show each category total, and mention which category has the highest cost and why it could be unusual."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
    llm_config=False
)

bill_processing_agent = AssistantAgent(
    name="BillProcessingAgent",
    llm_config=False,
    system_message="You categorize expenses from a bill into standard categories."
)

summary_agent = AssistantAgent(
    name="ExpenseSummarizationAgent",
    llm_config=False,
    system_message="You analyze categorized expenses and summarize trends."
)

group_chat = GroupChat(agents=[user_proxy, bill_processing_agent, summary_agent], messages=[])
manager = GroupChatManager(groupchat=group_chat)

# --- Main Execution Flow ---
if uploaded_file:
    st.success("✅ File uploaded. Processing...")
    with st.spinner("🔍 Extracting expenses..."):
        categorized_data, raw_response = process_bill_with_gemini(uploaded_file)
    if not categorized_data:
        st.error("❌ Failed to extract expenses.")
        st.text(raw_response)
    else:
        user_proxy.send("Bill uploaded", manager)
        chat_log.append(("UserProxy → chat_manager", "Bill uploaded"))
        user_proxy.send(f"Categorized expenses: {categorized_data}", bill_processing_agent)
        chat_log.append(("UserProxy → BillProcessingAgent", json.dumps(categorized_data, indent=2)))
        bp_response = "Categorization complete. Expenses sorted into available categories."
        chat_log.append(("BillProcessingAgent", bp_response))
        user_proxy.send("Summarize this data", summary_agent)
        chat_log.append(("UserProxy → ExpenseSummarizationAgent", "Summarize this data"))
        with st.spinner("📊 Generating spending summary..."):
            summary = summarize_expenses_with_gemini(categorized_data)
        chat_log.append(("ExpenseSummarizationAgent", summary))

        # --- Display Categorized Expenses ---
        st.markdown("<div class='category-title'>📂 Categorized Expenses</div>", unsafe_allow_html=True)
        for category, items in categorized_data.items():
            if items:
                st.markdown(f"<div class='category-card'><span class='category-title'>🗂️ {category}</span>", unsafe_allow_html=True)
                for i in items:
                    st.markdown(f"<div class='expense-item'>• <b>{i['item']}</b>: ₹{i['cost']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='category-title'>📋 Spending Summary</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)

        # --- Agent Chat Logs ---
        st.markdown("<div class='chat-log-title'>💬 Agent Chat Logs</div>", unsafe_allow_html=True)
        for sender, message in chat_log:
            style = "user" if "UserProxy" in sender else "agent"
            st.markdown(f"<div class='{style}'><strong>{sender}</strong><br>{message}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown('<div class="footer">Made with ❤️ by your AI Bill Management Agent</div>', unsafe_allow_html=True)