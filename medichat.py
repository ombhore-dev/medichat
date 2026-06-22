import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="🏥 MediChat - AI Medical Assistant", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .main-title { text-align: center; color: #0288D1; font-size: 42px; font-weight: bold; margin-bottom: 10px; }
        .sub-title { text-align: center; font-size: 18px; color: #455A64; margin-bottom: 30px; }
        .disclaimer-box { background-color: #FFF8E1; padding: 15px; border-left: 5px solid #FFC107; border-radius: 8px; margin-bottom: 20px; }
        .chat-box { background-color: #FFFFFF; padding: 25px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .user-msg { background-color: #E3F2FD; padding: 12px 18px; border-radius: 18px 18px 4px 18px; margin: 8px 0; }
        .bot-msg  { background-color: #F1F8E9; padding: 12px 18px; border-radius: 18px 18px 18px 4px; margin: 8px 0; border-left: 4px solid #0288D1; }
    </style>

    <h1 class='main-title'>🏥 MediChat</h1>
    <p class='sub-title'>Your AI-powered Medical Assistant — Ask symptoms, medications, nutrition & more!</p>
    <div class='disclaimer-box'>
        ⚠️ <b>Disclaimer:</b> MediChat provides general health information only. 
        It is <b>not a substitute</b> for professional medical advice, diagnosis, or treatment. 
        Always consult a qualified healthcare provider for personal medical concerns.
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h3 style='color:#0288D1'>⚙️ Settings</h3>", unsafe_allow_html=True)

language = st.sidebar.selectbox("🌐 Response Language", ["English", "Hindi", "Marathi"])

tone = st.sidebar.selectbox("🗣️ Response Tone", ["Simple (Easy to understand)", "Clinical (Medical terms)", "Detailed (In-depth)"])

specialty = st.sidebar.selectbox("🩺 Medical Specialty", [
    "General Medicine",
    "Cardiology",
    "Neurology",
    "Dermatology",
    "Pediatrics",
    "Orthopedics",
    "Psychiatry / Mental Health",
    "Nutrition & Diet",
    "Gynecology",
    "Oncology"
])

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align:center; color:gray;'>🔮 Powered by OpenAI GPT-4o</p>", unsafe_allow_html=True)

# Quick prompt buttons
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)
quick_prompt = None
with col1:
    if st.button("🤧 Cold vs Flu"):
        quick_prompt = "What are the differences between cold and flu symptoms?"
with col2:
    if st.button("❤️ Blood Pressure"):
        quick_prompt = "What foods help lower high blood pressure naturally?"
with col3:
    if st.button("😴 Sleep Health"):
        quick_prompt = "How much sleep do adults need and tips for better sleep?"
with col4:
    if st.button("😟 Anxiety Signs"):
        quick_prompt = "What are common signs and symptoms of anxiety disorder?"

# ── System prompt (STRICT medical-only) ──────────────────────────
def build_system_prompt(specialty, tone, language):
    tone_map = {
        "Simple (Easy to understand)": "Use very simple, easy-to-understand language. Avoid medical jargon.",
        "Clinical (Medical terms)":    "Use proper clinical and medical terminology.",
        "Detailed (In-depth)":         "Provide detailed, comprehensive explanations with causes, symptoms, treatment options, and prevention."
    }
    return f"""You are MediChat, a medical-only AI assistant specializing in {specialty}.

STRICT RULES — MUST FOLLOW AT ALL TIMES:
- You ONLY answer health and medical related questions.
- If the user asks ANYTHING non-medical (geography, sports, politics, math, history, coding, general knowledge, entertainment, etc.),
  respond EXACTLY with: "I'm a medical assistant. I can only help with health and medical questions. Please ask me something related to health, symptoms, medications, or wellness."
- Do NOT answer non-medical questions under any circumstance, even if the user insists, rephrases, or tries to trick you.
- Do NOT break character or pretend to be a general assistant.

MEDICAL GUIDELINES:
- Provide accurate, evidence-based medical information.
- {tone_map[tone]}
- Respond in {language}.
- Always recommend consulting a real doctor for personal diagnosis or treatment.
- For emergencies (chest pain, breathing difficulty, suicidal thoughts), IMMEDIATELY direct to emergency services.
- Never diagnose conditions or prescribe medications — only educate and inform.
- Be compassionate and supportive, especially for mental health topics.
- Use bullet points or numbered lists for clarity when needed.
- Mention when symptoms require urgent medical attention."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.markdown("### 💬 Chat")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>👤 <b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>⚕️ <b>MediChat:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# Input
user_input = st.chat_input("Ask a medical question...")

# Handle quick prompt
if quick_prompt:
    user_input = quick_prompt

# Send message
if user_input:
    if not OPENAI_API_KEY:
        st.error("⚠️ OPENAI_API_KEY not found in .env file. Please add it and restart the app.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            client = OpenAI(api_key=OPENAI_API_KEY)

            with st.spinner("⚕️ MediChat is thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": build_system_prompt(specialty, tone, language)},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    max_tokens=1000,
                    temperature=0.5
                )

            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        except Exception as e:
            st.error(f"⚠️ API Error: {str(e)}")