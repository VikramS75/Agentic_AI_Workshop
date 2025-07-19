
import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import google.generativeai as genai
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# === Streamlit UI ===
st.set_page_config(page_title="Smart Health Assistant", layout="wide", page_icon="🩺")

# Custom CSS for gradient header and cards
st.markdown("""
    <style>
    .gradient-header {
        background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
        color: white;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(24,90,157,0.12);
        text-align: center;
    }
    .section-card {
        background: #f7fafd;
        border-radius: 1.1rem;
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(67,206,162,0.08);
    }
    .agent-box {
        background: #e3f2fd;
        border-left: 6px solid #43cea2;
        border-radius: 0.7rem;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .download-btn .stButton>button {
        background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        border: none;
        padding: 0.7rem 1.5rem;
    }
    .sidebar-caption {
        color: #185a9d;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="gradient-header">
    <h1 style="margin-bottom:0.2em;">🩺 Smart Health Assistant</h1>
    <h4 style="font-weight:400;">Your Personalized Health, Diet & Fitness Planner</h4>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-caption">⚙️ Configuration</div>', unsafe_allow_html=True)
    gemini_api_key = st.text_input("Enter Gemini 1.5 Flash API Key:", type="password", help="Paste your Gemini API key here.")
    st.markdown("[🔑 Get Gemini API Key](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.markdown('<div class="sidebar-caption">ℹ️ About</div>', unsafe_allow_html=True)
    st.caption("This assistant calculates BMI, provides health recommendations, creates meal plans, and generates workout schedules based on your inputs.")

# === Session State ===
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "final_plan" not in st.session_state:
    st.session_state.final_plan = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# === Utility: Gemini Config Wrapper ===
def get_gemini_config(api_key: str, model: str = "gemini-1.5-flash"):
    return [{
        "model": model,
        "api_key": api_key,
        "api_type": "google",
        "base_url": "https://generativelanguage.googleapis.com/v1beta"
    }]

# === BMI Tool ===
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

# === Health Form ===
st.markdown('<div class="section-card">', unsafe_allow_html=True)
colored_header("👤 Enter Your Health Details", description="Fill in your information for a personalized plan.", color_name="blue-70")
with st.form("health_form"):
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, help="Enter your weight in kilograms.")
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, help="Enter your height in centimeters.")
        age = st.number_input("Age", min_value=18, max_value=100, value=30, help="Enter your age.")
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        dietary_preference = st.selectbox("Dietary Preference", ["Veg", "Non-Veg", "Vegan"])
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("✨ Generate Health Plan")
st.markdown('</div>', unsafe_allow_html=True)

# === Agent Initialization ===
def init_agents(api_key):
    genai.configure(api_key=api_key)
    config_list = get_gemini_config(api_key)

    bmi_agent = AssistantAgent(
        name="BMI_Agent",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message="""You are a BMI specialist. Analyze BMI results and:
        1. Calculate BMI from weight (kg) and height (cm)
        2. Categorize (underweight, normal, overweight, obese)
        3. Provide health recommendations
        Always include the exact BMI value in your response."""
    )

    # Register BMI tool to BMI Agent (fix)
    bmi_agent.register_function(function_map={"calculate_bmi": calculate_bmi})

    diet_agent = AssistantAgent(
        name="Diet_Planner",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message=f"""You are a nutritionist. Create meal plans based on:
        1. BMI analysis from BMI_Agent
        2. Dietary preference ({dietary_preference})
        Include breakfast, lunch, dinner, and snacks with portions."""
    )

    workout_agent = AssistantAgent(
        name="Workout_Scheduler",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message=f"""You are a fitness trainer. Create weekly workout plans based on:
        1. Age ({age}) and gender ({gender})
        2. BMI recommendations
        3. Meal plan from Diet_Planner
        Include cardio, strength training with duration and intensity."""
    )

    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message="Collects and shares user data with other agents."
    )

    return user_proxy, bmi_agent, diet_agent, workout_agent, config_list

# === Submit Handler ===
if submit_btn and gemini_api_key:
    try:
        user_proxy, bmi_agent, diet_agent, workout_agent, config_list = init_agents(gemini_api_key)

        groupchat = GroupChat(
            agents=[user_proxy, bmi_agent, diet_agent, workout_agent],
            messages=[],
            max_round=6,
            speaker_selection_method="round_robin"
        )

        manager = GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": config_list, "cache_seed": None}
        )

        initial_message = f"""
        User Health Profile:
        - Basic Information:
          • Weight: {weight} kg
          • Height: {height} cm
          • Age: {age}
          • Gender: {gender}
        - Preferences:
          • Dietary Preference: {dietary_preference}

        Please proceed with the health assessment in this sequence:
        1. Calculate BMI using the 'calculate_bmi' function with weight={weight} and height={height}
        2. Analyze BMI and provide recommendations
        3. Create a meal plan based on BMI analysis and dietary preference
        4. Develop a workout schedule based on age, gender, and meal plan
        """

        with st.spinner("Generating your personalized health plan..."):
            user_proxy.initiate_chat(
                manager,
                message=initial_message,
                clear_history=True
            )

            st.session_state.conversation = []
            for msg in groupchat.messages:
                if msg['role'] != 'system' and msg['content'].strip():
                    st.session_state.conversation.append((msg['name'], msg['content']))
                    if msg['name'] == "Workout_Scheduler":
                        st.session_state.final_plan = msg['content']

        st.success("🎉 Health plan generated successfully!")

    except Exception as e:
        st.error(f"❌ Error occurred: {str(e)}")
        st.info("Please ensure: 1) Valid API key 2) Stable internet connection 3) Correct input values")

# === Results Display ===
if st.session_state.conversation:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    colored_header("📝 Health Plan Generation Process", description="See how each agent contributed to your plan.", color_name="green-70")
    for agent, message in st.session_state.conversation:
        st.markdown(f'<div class="agent-box"><b>{agent} says:</b><br>{message}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    colored_header("🌟 Your Complete Health Plan", description="Download or review your personalized plan.", color_name="violet-70")
    if st.session_state.final_plan:
        st.markdown(st.session_state.final_plan)
        with stylable_container(key="download-btn", css_styles="padding-top:1em;"):
            st.download_button(
                label="⬇️ Download Health Plan",
                data=st.session_state.final_plan,
                file_name="personalized_health_plan.txt",
                mime="text/plain"
            )
    else:
        st.warning("⚠️ Workout schedule not generated. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)

elif not submit_btn:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    colored_header("📋 Instructions", description="How to use the Smart Health Assistant", color_name="orange-70")
    st.markdown("""
    <ol style='font-size:1.1em;'>
      <li>🔑 <b>Enter your Gemini API key</b> in the sidebar</li>
      <li>📝 <b>Fill in your health details</b></li>
      <li>✨ <b>Click 'Generate Health Plan'</b></li>
      <li>🌟 <b>View your personalized recommendations</b></li>
    </ol>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)