import streamlit as st
from retriever import build_vector_db, retrieve_context
from sentiment import analyze_sentiment
from responder import generate_empathetic_reply
from escalation import check_escalation
import csv
import os
import pandas as pd

st.set_page_config(page_title="RAG Support Assistant", page_icon="🤖", layout="centered")
st.title("🤖 RAG Customer Support Assistant")
st.markdown("Ask your queries and get empathetic, AI-generated answers based on support articles.")

# Build DB once
@st.cache_resource
def load_db():
    build_vector_db()
load_db()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "sentiments" not in st.session_state:
    st.session_state.sentiments = []
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []
if "feedback_saved" not in st.session_state:
    st.session_state.feedback_saved = set()

# Sidebar quick presets
st.sidebar.subheader("🔖 Quick Questions")
for preset in [
    "How do I reset my password?",
    "I want to cancel my order",
    "Where is my refund?",
    "How do I update my account details?"
]:
    if st.sidebar.button(preset):
        st.session_state.query_input = preset

# Input field
query = st.text_input("💡 Ask something:", key="query_input")

if st.button("Submit") and query:
    sentiment = analyze_sentiment(query)
    st.session_state.sentiments.append(sentiment)

    context_chunks, source_files = retrieve_context(query, return_sources=True)
    context_text = "\n".join(context_chunks)
    response = generate_empathetic_reply(query, context_text, sentiment)

    # Escalation check
    escalated, reason = check_escalation(
    [q for q, _ in st.session_state.chat_history],
    st.session_state.sentiments,
    return_reason=True
)


    # Store full entry
    st.session_state.chat_history.append((query, response))

    # Chat messages
    with st.chat_message("user"):
        st.write(f"**You:** {query}")

    with st.chat_message("assistant"):
        st.markdown("📚 **Top Relevant Chunks:**")
        for i, (chunk, source) in enumerate(zip(context_chunks, source_files)):
            with st.expander(f"{i+1}. {source}"):
                st.write(chunk)
        st.info(f"🧠 Detected Sentiment: **{sentiment}**")
        st.markdown(f"\n🤖 **AI Response:**\n{response}")

        if escalated:
            st.error(f"🚨 Escalation Detected: {reason}")

    # Feedback (CSAT)
    csat_key = f"csat_{len(st.session_state.chat_history)}"
    if csat_key not in st.session_state:
        st.session_state[csat_key] = None

    csat = st.radio("📝 Was this response helpful?", ["Yes", "No"], key=csat_key, horizontal=True)

    if len(st.session_state.chat_history) not in st.session_state.feedback_saved:
        st.session_state.feedback_log.append((query, sentiment, response, csat))
        st.session_state.feedback_saved.add(len(st.session_state.chat_history))

        # Save to feedback_log.csv
        feedback_file = "feedback_log.csv"
        file_exists = os.path.isfile(feedback_file)
        with open(feedback_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Query", "Sentiment", "AI Reply", "Feedback"])
            writer.writerow([query, sentiment, response, csat])

# Sidebar: Feedback Summary
if st.sidebar.button("📊 Show Feedback Summary"):
    total = len(st.session_state.feedback_log)
    helpful = sum(1 for _, _, _, fb in st.session_state.feedback_log if fb == "Yes")
    score = (helpful / total) * 100 if total > 0 else 0
    st.sidebar.markdown(f"**Total Queries:** {total}")
    st.sidebar.markdown(f"**Helpful Responses:** {helpful}")
    st.sidebar.markdown(f"**CSAT Score:** {score:.2f}%")

# 📥 Download Feedback CSV
if os.path.exists("feedback_log.csv"):
    with open("feedback_log.csv", "rb") as f:
        st.sidebar.download_button(
            label="📥 Download Feedback CSV",
            data=f,
            file_name="feedback_log.csv",
            mime="text/csv"
        )

# 📥 Download Escalation Log
if os.path.exists("escalations.csv"):
    with open("escalations.csv", "rb") as f:
        st.sidebar.download_button(
            label="🚨 Download Escalation Log",
            data=f,
            file_name="escalations.csv",
            mime="text/csv"
        )
