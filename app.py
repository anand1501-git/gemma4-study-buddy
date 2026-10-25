
import os
import streamlit as st
from google import genai

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Gemma Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #f1efff;
    --muted: #c4c1dd;
    --purple: #a99aff;
    --line: rgba(190, 180, 255, 0.20);
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(167, 139, 250, 0.22),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(96, 165, 250, 0.18),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #0b1020,
            #17152e,
            #101b31
        );
    color: #f8fafc;
}

.block-container {
    max-width: 1050px;
    padding: 0.8rem 1.5rem 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(167, 139, 250, 0.22),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(96, 165, 250, 0.18),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #0b1020,
            #17152e,
            #101b31
        );
    color: #f8fafc;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.5px;
}

p, label {
    font-family: 'DM Sans', sans-serif;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 2rem;
    font-family: 'Manrope', sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    color: #f8fafc;
}

.brand-icon {
    display: grid;
    place-items: center;
    width: 44px;
    height: 44px;
    border-radius: 14px;
    background: linear-gradient(135deg, #a78bfa, #5940db);
    color: white;
    font-size: 23px;
    box-shadow: 0 8px 25px #7057f555;
}

.hero {
    padding: 2.5rem 2.6rem;
    border: 1px solid #ffffff25;
    border-radius: 28px;
    color: white;
    background: linear-gradient(
        120deg,
        #292052 0%,
        #5541b8 58%,
        #7865f7 100%
    );
    box-shadow: 0 18px 45px #08091c55;
    margin-bottom: 2.5rem;
}

.hero-tag {
    display: inline-block;
    padding: 7px 12px;
    border: 1px solid #ffffff40;
    border-radius: 99px;
    background: #ffffff12;
    color: #f0edff;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.4px;
}

.hero h1 {
    color: white !important;
    font-size: clamp(2rem, 5vw, 3.2rem);
    line-height: 1.15;
    margin: 1.2rem 0 0.8rem;
}

.hero p {
    max-width: 620px;
    color: #e2ddff;
    font-size: 1.04rem;
    line-height: 1.8;
    margin-bottom: 0;
}

.section-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #b8aaff;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.section-description {
    color: #c4c1dd;
    margin-top: -0.5rem;
    margin-bottom: 1.3rem;
    line-height: 1.7;
}

div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border-radius: 12px;
    border: 1px solid #dcd6ff;
    background: #f9f8ff;
    color: #202044;
    min-height: 46px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #a99aff;
    box-shadow: 0 0 0 2px #a99aff35;
}

div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    color: #e2defa;
    font-weight: 600;
}

.stButton > button {
    width: 100%;
    min-height: 50px;
    border: 0;
    border-radius: 13px;
    background: linear-gradient(100deg, #8068ff, #5940db);
    color: white;
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    box-shadow: 0 8px 22px #7057f540;
    transition: transform .2s, box-shadow .2s;
}

.stButton > button:hover {
    color: white;
    border: 1px solid #c4b5fd;
    transform: translateY(-2px);
    box-shadow: 0 12px 26px #7057f566;
}

.panel {
    padding: 1.4rem 1.5rem;
    border: 1px solid var(--line);
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.09),
        rgba(255, 255, 255, 0.035)
    );
    box-shadow: 0 8px 30px #08091c25;
    margin: 0.8rem 0;
}

.panel h3 {
    color: #f1efff !important;
}

.panel p {
    color: #c4c1dd !important;
    line-height: 1.75;
    margin-bottom: 0;
}

.answer {
    padding: 1.5rem;
    border: 1px solid #b8aaff55;
    border-radius: 18px;
    background: #f8f7ff;
    color: #24213d;
    line-height: 1.85;
    margin-top: 0.8rem;
}

.answer h1, .answer h2, .answer h3 {
    color: #30265e !important;
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

hr {
    border-color: #ffffff25;
}

.footer {
    padding-top: 2.5rem;
    text-align: center;
    color: #aaa7c6;
    font-size: 0.83rem;
}

@media (max-width: 640px) {
    .block-container {
        padding: 1.2rem 1rem 2.5rem;
    }

    .hero {
        padding: 1.7rem 1.3rem;
        border-radius: 21px;
    }

    .brand {
        margin-bottom: 1.5rem;
    }

    .panel {
        padding: 1.2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="brand">
    <div class="brand-icon">✦</div>
    <div>Gemma <span style="color:#a99aff">Study Buddy</span></div>
</div>

<div class="hero">
    <span class="hero-tag">✦ YOUR PERSONAL AI LEARNING COMPANION</span>
    <h1>Learn smarter.<br>Grow every day.</h1>
    <p>
        Big topics become small steps. Ask a question, understand a concept,
        or practise your skills with your AI-powered study companion.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 01 - YOUR LEARNING GOALS
# --------------------------------------------------

st.markdown(
    '<div class="section-label">01 — Your Learning Goals</div>',
    unsafe_allow_html=True,
)

st.subheader("What shall we explore?")

st.markdown(
    '<p class="section-description">'
    'Choose a topic and customise your learning session.'
    '</p>',
    unsafe_allow_html=True,
)

topic = st.text_input(
    "Topic",
    placeholder="e.g. Python loops, DBMS joins, machine learning",
)

col1, col2 = st.columns(2, gap="large")

with col1:
    action = st.selectbox(
        "Choose your learning activity",
        [
            "Explain simply",
            "Summarize a topic",
            "Generate practice questions",
        ],
    )

with col2:
    level = st.selectbox(
        "Your learning level",
        ["Beginner", "Intermediate", "Advanced"],
    )

learn = st.button(
    "✦  Learn with Gemma 4",
    use_container_width=True,
)

# --------------------------------------------------
# 02 - YOUR LEARNING SPACE
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">02 — Your Learning Space</div>',
    unsafe_allow_html=True,
)

st.subheader("A little space to grow")

st.markdown(
    '<p class="section-description">'
    'Learn at your own pace. Build understanding one step at a time.'
    '</p>',
    unsafe_allow_html=True,
)

space1, space2, space3 = st.columns(3, gap="medium")

with space1:
    st.markdown("""
    <div class="panel">
        <div style="font-size:2rem">🎯</div>
        <h3>Made for your goals</h3>
        <p>Get explanations tailored to your chosen learning level.</p>
    </div>
    """, unsafe_allow_html=True)

with space2:
    st.markdown("""
    <div class="panel">
        <div style="font-size:2rem">💡</div>
        <h3>Understand deeply</h3>
        <p>Explore concepts with clear language and helpful examples.</p>
    </div>
    """, unsafe_allow_html=True)

with space3:
    st.markdown("""
    <div class="panel">
        <div style="font-size:2rem">⚡</div>
        <h3>Practise and grow</h3>
        <p>Review important ideas and generate practice questions.</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# AI LEARNING SESSION
# --------------------------------------------------

if learn:
    if not topic.strip():
        st.warning("Please enter a topic to get started.")
    else:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.error(
                "API key not found. Set GEMINI_API_KEY in your "
                "Terminal and restart the app."
            )
        else:
            prompt = (
                "You are a helpful and accurate study assistant. "
                f"Learning level: {level}. "
                f"Activity: {action}. "
                f"Topic: {topic}. "
                "Use clear language, headings, and helpful examples. "
                "For practice questions, include answers after the questions."
            )

            try:
                client = genai.Client(api_key=api_key)

                with st.spinner("✦ Preparing your learning session..."):
                    response = client.models.generate_content(
                        model="gemma-4-26b-a4b-it",
                        contents=prompt,
                    )

                st.markdown("---")
                st.markdown("## ✨ Your Learning Session")
                st.caption(f"Topic: {topic} · Level: {level}")

                st.markdown(
                    '<div class="answer">',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    response.text or "No text was returned. Please try again."
                )
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception:
                st.error(
                    "We couldn't generate an answer this time. "
                    "Check your API configuration and try again."
                )
                with st.expander("Technical error details"):
                    import traceback
                    st.code(traceback.format_exc())

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    Built with care for curious minds · Powered by Gemma 4
</div>
""", unsafe_allow_html=True)
