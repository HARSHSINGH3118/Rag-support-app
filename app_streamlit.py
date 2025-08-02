import streamlit as st
from retriever import build_vector_db, retrieve_context  # assume returns documents with .page_content and .metadata
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

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "sentiments" not in st.session_state:
    st.session_state.sentiments = []
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []
if "feedback_saved" not in st.session_state:
    st.session_state.feedback_saved = set()

# Sidebar: Quick Presets
st.sidebar.subheader("🔖 Quick Questions")
for preset in [
    "How do I reset my password?",
    "I want to cancel my order",
    "Where is my refund?",
    "How do I update my account details?"
]:
    if st.sidebar.button(preset):
        st.session_state.query_input = preset

# Input query
query = st.text_input("Ask your question:", key="query_input")

if st.button("Submit") and query:
    sentiment = analyze_sentiment(query)
    context_docs = retrieve_context(query)

    # ✅ Fallback-compatible chunk parser
    context_chunks = []
    for doc in context_docs:
        if isinstance(doc, str):
            context_chunks.append((doc, "unknown"))
        else:
            context_chunks.append((doc.page_content, doc.metadata.get("source", "unknown")))

    context_text = "\n".join([chunk for chunk, _ in context_chunks])
    response = generate_empathetic_reply(query, context_text, sentiment)

    st.session_state.chat_history.append((query, context_chunks, sentiment, response))
    st.session_state.sentiments.append(sentiment)

    check_escalation([q for q, _, _, _ in st.session_state.chat_history], st.session_state.sentiments)

# Show chat messages
for i, (q, chunks, sentiment, r) in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(f"**🧑 You:** {q}")

    with st.chat_message("assistant"):
        st.markdown("\n**📚 Top Relevant Chunks:**")
        for j, (chunk, source) in enumerate(chunks, 1):
            st.markdown(f"{j}. *({source})*:\n{chunk}")
        st.markdown(f"\n**🔥 Detected Sentiment:** *{sentiment}*")
        st.markdown(f"\n**🤖 AI Response:**\n{r}")

    # Feedback
    csat_key = f"csat_{i}"
    if csat_key not in st.session_state:
        st.session_state[csat_key] = None

    csat = st.radio("📝 Was this response helpful?", ["Yes", "No"], key=csat_key, horizontal=True)

    if i not in st.session_state.feedback_saved:
        st.session_state.feedback_log.append((q, sentiment, r, csat))
        st.session_state.feedback_saved.add(i)

        # Save to CSV
        feedback_file = "feedback_log.csv"
        file_exists = os.path.isfile(feedback_file)
        with open(feedback_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Query", "Sentiment", "AI Reply", "Feedback"])
            writer.writerow([q, sentiment, r, csat])

# 📊 CSAT Summary in Sidebar
if st.sidebar.button("📊 Show Feedback Summary"):
    total = len(st.session_state.feedback_log)
    helpful = sum(1 for _, _, _, fb in st.session_state.feedback_log if fb == "Yes")
    score = (helpful / total) * 100 if total > 0 else 0
    st.sidebar.markdown(f"**Total Queries:** {total}")
    st.sidebar.markdown(f"**Helpful Responses:** {helpful}")
    st.sidebar.markdown(f"**CSAT Score:** {score:.2f}%")

# 📅 Download CSV
if os.path.exists("feedback_log.csv"):
    with open("feedback_log.csv", "rb") as f:
        st.sidebar.download_button(
            label="📅 Download Feedback CSV",
            data=f,
            file_name="feedback_log.csv",
            mime="text/csv"
        )
