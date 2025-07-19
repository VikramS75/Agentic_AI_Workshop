import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

# Hardcoded Google API Key
GOOGLE_API_KEY = "AIzaSyCyGhGV5y7IUvXmF_ZpjFeCBemACPdvMGY"

# Set page configuration with a custom icon and theme color
st.set_page_config(page_title="Logistics Optimizer", page_icon="🚚", layout="wide")

# Custom CSS for enhanced visuals
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0fdfa 100%);
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 2em;
        font-size: 1.1em;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #2563eb;
        padding: 0.5em;
        font-size: 1.1em;
    }
    .st-bb {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 1.5em 2em;
        box-shadow: 0 2px 8px rgba(37,99,235,0.08);
    }
    .stMarkdown h2 {
        color: #2563eb;
    }
    textarea {
        min-height: 100px !important;
        height: 120px !important;
        font-size: 1.1em !important;
        border-radius: 8px !important;
        border: 2px solid #2563eb !important;
        padding: 0.5em !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header section with icon and subtitle
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://img.icons8.com/color/96/000000/delivery.png", width=80)
with col2:
    st.title("Logistics Optimization with CrewAI")
    st.markdown(
        "<span style='font-size:1.2em; color:#2563eb;'>Empower your logistics with AI-driven route and inventory optimization.</span>",
        unsafe_allow_html=True
    )

st.markdown("---")

# Input form in a card-like container
with st.container():
    st.markdown("<h4 style='color:#2563eb;'>📝 Enter Product List</h4>", unsafe_allow_html=True)
    with st.form("logistics_form"):
        product_input = st.text_area(
            "Product names (comma separated)",
            "TV, Laptops, Headphones",
            help="E.g. TV, Laptops, Headphones",
            height=100
        )
        submitted = st.form_submit_button("🚀 Optimize Logistics")

if submitted:
    with st.spinner("🤖 Running CrewAI agents to analyze and optimize your logistics..."):

        # Prepare LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=GOOGLE_API_KEY
        )

        # Define tools (empty for now)
        def logistics_analyst_tools():
            return []

        def optimization_strategist_tools():
            return []

        # Define agents
        logistics_analyst = Agent(
            role="Logistics Analyst",
            goal="Analyze logistics operations to find inefficiencies in delivery routes and inventory turnover.",
            backstory="A seasoned analyst with years of experience in identifying bottlenecks in supply chain networks.",
            verbose=True,
            llm=llm,
            tools=logistics_analyst_tools()
        )

        optimization_strategist = Agent(
            role="Optimization Strategist",
            goal="Design data-driven strategies to optimize logistics operations and improve performance.",
            backstory="Known for implementing cost-saving logistics strategies using advanced AI models.",
            verbose=True,
            llm=llm,
            tools=optimization_strategist_tools()
        )

        # Parse product input
        products = [p.strip() for p in product_input.split(",") if p.strip()]

        # Define tasks
        task1 = Task(
            description=f"Analyze logistics data for the following products: {products}. Focus on delivery routes and inventory turnover trends.",
            expected_output="Summary of current inefficiencies and potential improvement areas in logistics operations.",
            agent=logistics_analyst
        )

        task2 = Task(
            description="Based on the logistics analyst's findings, develop an optimization strategy to reduce delivery time and improve inventory management.",
            expected_output="Detailed optimization strategy with action points to improve logistics efficiency.",
            agent=optimization_strategist
        )

        # Create Crew
        crew = Crew(
            agents=[logistics_analyst, optimization_strategist],
            tasks=[task1, task2],
            verbose=True
        )

        # Execute CrewAI workflow
        result = crew.kickoff()

    # Show result in a visually distinct card
    st.success("✅ Optimization Complete!")
    st.markdown(
        "<h2>🔍 Final Optimization Strategy</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='st-bb'>{result}</div>",
        unsafe_allow_html=True
    )