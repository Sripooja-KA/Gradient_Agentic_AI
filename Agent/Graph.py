# LangGraph workflow will be implemented here.
# Planned flow:
# START -> validate -> route -> retrieve -> validate evidence
# -> generate answer -> validate citations -> END
import os
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from agent.state import AgentState
from agent.router import route_intent
from tools.reddit import fetch_reddit_posts
from tools.weather import fetch_weather_data

def router_node(state: AgentState) -> AgentState:
    route = route_intent(state["question"])
    return {**state, "route": route}

def tool_execution_node(state: AgentState) -> AgentState:
    route = state["route"]
    if route == "reddit":
        res = fetch_reddit_posts(state["question"])
        return {**state, "raw_evidence": res["evidence"], "sources": [res["source"]]}
    elif route == "weather":
        res = fetch_weather_data("Chennai")
        return {**state, "raw_evidence": res["evidence"], "sources": [res["source"]]}
    
    return {**state, "raw_evidence": "", "sources": []}

def synthesis_node(state: AgentState) -> AgentState:
    if state["route"] == "none":
        return {
            **state,
            "answer": "I do not have sufficient live grounded sources (Reddit discussions or Open-Meteo weather data) to answer this question reliably.",
            "is_grounded": False
        }
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {
            **state,
            "answer": f"Retrieved Evidence from {state['sources']}:\n{state['raw_evidence']}\n\n(Groq API key not found in environment to synthesize final narrative).",
            "is_grounded": True
        }

    try:
        # Utilizing open-weights model available on Groq
        llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.1, groq_api_key=api_key)
        prompt = (
            f"You are a Grounded Research Assistant. Answer the user's question ONLY using the provided evidence block.\n"
            f"Question: {state['question']}\n"
            f"Evidence: {state['raw_evidence']}\n"
            f"Sources: {state['sources']}\n\n"
            f"Include explicit citations to the sources used."
        )
        response = llm.invoke(prompt)
        return {**state, "answer": response.content, "is_grounded": True}
    except Exception as e:
        return {
            **state,
            "answer": f"Based on {state['sources']}:\n{state['raw_evidence']}",
            "is_grounded": True,
            "errors": [str(e)]
        }

def build_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    workflow.add_node("tools", tool_execution_node)
    workflow.add_node("synthesizer", synthesis_node)

    workflow.set_entry_point("router")
    workflow.add_edge("router", "tools")
    workflow.add_edge("tools", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()
