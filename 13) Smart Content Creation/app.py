
import streamlit as st
import time
import google.generativeai as genai
import os
from typing import List, Tuple
import json

# --- Custom CSS for Modern UI ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #3b82f6;
        margin-bottom: 0.2em;
    }
    .subtitle {
        color: #6366f1;
        font-size: 1.2rem;
        margin-bottom: 1.5em;
    }
    .agent-bubble {
        border-radius: 1.2em;
        padding: 1.1em 1.5em;
        margin-bottom: 1em;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px #e0e7ff;
        background: #fff;
        border-left: 6px solid #6366f1;
    }
    .agent-bubble.critic {
        border-left: 6px solid #f59e42;
        background: #fef9f4;
    }
    .final-content-card {
        background: #f1f5f9;
        border-radius: 1.2em;
        padding: 1.5em;
        border: 2px solid #6366f1;
        margin-bottom: 2em;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.9em;
        margin-top: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# Configure Gemini API
# For security, consider using environment variables
api_key = "AIzaSyDG-0xIaprzdT70VTf-LnMt62_s-F8SJqA"
genai.configure(api_key=api_key)

# System messages
CREATOR_SYSTEM_MESSAGE = """
You are a Content Creator Agent specializing in Generative AI. Your role is to:
1. Draft clear, concise, and technically accurate content
2. Revise content based on constructive feedback
3. Structure output in markdown format
4. Focus exclusively on content creation (no commentary)
5. Provide comprehensive coverage of the topic
"""

CRITIC_SYSTEM_MESSAGE = """
You are a Content Critic Agent evaluating Generative AI content. Your role is to:
1. Analyze technical accuracy and language clarity
2. Provide specific, constructive feedback
3. Identify both strengths and areas for improvement
4. Maintain professional, objective tone
5. Suggest concrete improvements
"""

# Agent class for content generation using direct Gemini API
class ContentAgent:
    def __init__(self, model_name: str, system_message: str):
        self.model_name = model_name
        self.system_message = system_message
        self.model = genai.GenerativeModel(model_name)
    
    def generate(self, prompt: str) -> str:
        """Generate content using the Gemini model"""
        full_prompt = f"{self.system_message}\n\n{prompt}"
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                    top_p=0.8,
                    top_k=40
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"

# Initialize agents
@st.cache_resource
def initialize_agents():
    creator = ContentAgent("gemini-1.5-flash", CREATOR_SYSTEM_MESSAGE)
    critic = ContentAgent("gemini-1.5-flash", CRITIC_SYSTEM_MESSAGE)
    return creator, critic

# --- Modern Title and Subtitle ---
st.markdown("<div class='main-title'>🤖 Agentic AI Content Refinement</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A creative collaboration between <b>Content Creator</b> and <b>Content Critic</b> agents, powered by Gemini AI</div>", unsafe_allow_html=True)

# Sidebar controls with enhancements
with st.sidebar:
    st.header("⚙️ Configuration")
    topic = st.text_input("📝 Discussion Topic", "Agentic AI", help="Enter the topic you want to create content about")
    turns = st.slider("🔄 Conversation Turns", min_value=3, max_value=5, value=3, step=2, 
                     help="Number of back-and-forth exchanges between agents")
    st.markdown("---")
    st.info("**How it works:**\n\n1. 🎨 Creator drafts content\n2. 🔍 Critic provides feedback\n3. 🔄 Iterative improvement\n4. 🏁 Final markdown output", icon="💡")

# Main content area
col1, col2 = st.columns([3, 1])

with col2:
    generate_btn = st.button("🚀 Start Simulation", type="primary", use_container_width=True)
    
    if st.button("Clear Results", use_container_width=True):
        if 'conversation_history' in st.session_state:
            del st.session_state['conversation_history']
        if 'final_content' in st.session_state:
            del st.session_state['final_content']
        st.rerun()

with col1:
    if generate_btn:
        # Initialize agents
        creator_agent, critic_agent = initialize_agents()
        
        # Initialize conversation state
        conversation_history: List[Tuple[str, str, str]] = []
        creator_output = ""
        critic_feedback = ""
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Start conversation
        for turn in range(1, turns + 1):
            progress = turn / turns
            progress_bar.progress(progress)
            
            with st.container():
                # Content Creator Turn (odd turns)
                if turn % 2 == 1:
                    status_text.text(f"🎨 Turn {turn}: Content Creator working...")
                    
                    if turn == 1:
                        prompt = f"""Draft comprehensive content about {topic} in markdown format covering:
- Key concepts and definitions
- Technical foundations
- Real-world applications and use cases
- Current challenges and limitations
- Future implications and trends

Make it informative, well-structured, and engaging."""
                    else:
                        prompt = f"""Revise this content based on the critic's feedback:

**Critic's Feedback:**
{critic_feedback}

**Current Content:**
{creator_output}

Provide improved markdown content that addresses the feedback while maintaining quality and structure."""
                    
                    # Generate content
                    with st.spinner("Content Creator is working..."):
                        creator_output = creator_agent.generate(prompt)
                    
                    conversation_history.append(("Creator", prompt, creator_output))
                
                # Content Critic Turn (even turns)
                else:
                    status_text.text(f"🔍 Turn {turn}: Content Critic analyzing...")
                    
                    prompt = f"""Evaluate this content on the following criteria:

1. **Technical Accuracy**: Are the concepts and information correct?
2. **Clarity of Explanations**: Are complex ideas explained clearly?
3. **Depth of Coverage**: Is the topic covered comprehensively?
4. **Structure and Organization**: Is the content well-organized?
5. **Engagement**: Is the content interesting and engaging?

**Content to Evaluate:**
{creator_output}

Provide specific, constructive feedback with concrete suggestions for improvement."""
                    
                    # Generate feedback
                    with st.spinner("Content Critic is analyzing..."):
                        critic_feedback = critic_agent.generate(prompt)
                    
                    conversation_history.append(("Critic", prompt, critic_feedback))
                
                time.sleep(0.5)  # Avoid rate limiting
        
        # Store results in session state
        st.session_state['conversation_history'] = conversation_history
        st.session_state['final_content'] = creator_output
        
        progress_bar.progress(1.0)
        status_text.text("✅ Simulation completed!")
        
        # Auto-scroll to results
        st.rerun()

# Display results if available
if 'final_content' in st.session_state:
    st.markdown("---")
    st.subheader("✅ Final Refined Content")
    st.markdown(f"<div class='final-content-card'>{st.session_state['final_content']}</div>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Final Content",
        data=st.session_state['final_content'],
        file_name=f"refined_content_{topic.replace(' ', '_')}.md",
        mime="text/markdown"
    )
    st.markdown("---")
    st.subheader("🗨️ Conversation History")
    if 'conversation_history' in st.session_state:
        for i, (role, prompt, response) in enumerate(st.session_state['conversation_history'], 1):
            bubble_class = "agent-bubble"
            avatar = "🎨" if role == "Creator" else "🔍"
            if role == "Critic":
                bubble_class += " critic"
            st.markdown(f"<div class='{bubble_class}'><b>{avatar} {role} - Turn {i}</b><br/><br/><b>Prompt:</b><br/>{prompt}<br/><br/><b>Response:</b><br/>{response}</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    "<div class='footer'>Powered by <b>Google Gemini AI</b> | Built with <b>Streamlit</b></div>",
    unsafe_allow_html=True
)