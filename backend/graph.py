from langgraph.graph import StateGraph, START, END
from state import StockAnalysisState
from nodes import collect_stock_data, read_news, research_market, analyze_and_write_report

def build_graph():
    graph = StateGraph(StockAnalysisState)

    graph.add_node("collect_stock_data", collect_stock_data)
    graph.add_node("read_news", read_news)
    graph.add_node("research_market", research_market)
    graph.add_node("analyze_and_write_report", analyze_and_write_report)

    graph.add_edge(START, "collect_stock_data")
    graph.add_edge("collect_stock_data", "read_news")
    graph.add_edge("collect_stock_data", "research_market")
    graph.add_edge(["read_news", "research_market"], "analyze_and_write_report")
    graph.add_edge("analyze_and_write_report", END)

    return graph.compile()

stock_analysis_graph = build_graph()

