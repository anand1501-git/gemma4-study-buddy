import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Gemma 4 Study Buddy",
    page_icon="📚",
    layout="centered",
)

st.title("📚 Gemma 4 Study Buddy")
st.write("Your AI-powered learning companion")

st.info(
    "Ask a question, simplify a difficult topic, "
    "or generate practice questions."
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning(
        "Set your GEMINI_API_KEY environment variable "
        "to start using the AI assistant."
    )
    st.stop()

client = genai.Client(api_key=api_key)

topic = st.text_input(
    "What do you want to learn?",
    placeholder="Example: Python loops",
)

action = st.selectbox(
    "Choose an activity",
    [
        "Explain simply",
        "Summarize a topic",
        "Generate practice questions",
    ],
)

level = st.selectbox(
    "Your learning level",
    ["Beginner", "Intermediate", "Advanced"],
)

if st.button("✨ Learn with Gemma 4"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        prompt = (
            f"You are a helpful study assistant. "
            f"Learning level: {level}. "
            f"Activity: {action}. "
            f"Topic: {topic}. "
            "Use clear language and helpful examples."
        )

        with st.spinner("Gemma 4 is preparing your answer..."):
            try:
                response = client.models.generate_content(
                    model="gemma-4-26b-a4b-it",
                    contents=prompt,
                )
                st.markdown("### Your answer")
                st.write(response.text)
            except Exception:
                st.error(
                    "The request failed. Check your API key, "
                    "model access, network, and usage limits."
                )
