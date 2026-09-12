from agent.graph import build_graph

def test_graph_execution():
    app = build_graph()
    state = {"question": "weather in Chennai", "route": "", "tool_results": "", "sources": [], "answer": "", "errors": []}
    output = app.invoke(state)
    assert "answer" in output
