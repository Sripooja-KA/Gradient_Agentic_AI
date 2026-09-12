import streamlit as st
from dotenv import load_dotenv
from agent.graph import build_agent
from guardrails.validation import sanitize_user_input

load_dotenv()

st.set_page_config(page_title="Grounded Research Agent", page_icon="⚡", layout="wide")

st.title("⚡ Grounded Research Agent")
st.caption("Grounded AI Assistant | Powered by LangGraph, Groq Open-Weights, Reddit API, & Open-Meteo REST API")

query = st.text_input("Enter your query (e.g., 'What is the current weather in Chennai?' or 'What are people on Reddit saying about remote work?'):")

if st.button("Execute Agent Workflow") and query:
    sanitized_query = sanitize_user_input(query)
    app = build_agent()
    
    initial_state = {
        "question": sanitized_query,
        "route": "",
        "raw_evidence": "",
        "sources": [],
        "answer": "",
        "is_grounded": False,
        "errors": []
    }
    
    with st.spinner("Processing workflow nodes..."):
        final_state = app.invoke(initial_state)

    st.subheader("Final Answer")
    st.write(final_state.get("answer", "No response generated."))

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Routed Category:**", final_state.get("route"))
        st.write("**Grounded Status:**", final_state.get("is_grounded"))
    with col2:
        st.write("**Cited Sources:**", final_state.get("sources"))

    with st.expander("Inspect Execution State & Trace Details"):
        st.json(final_state)