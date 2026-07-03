import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from state import StockAnalysisState
from tools import fetch_stock_data, fetch_stock_financials, fetch_stock_news, resolve_ticker

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.environ.get("GROQ_API_KEY"), temperature=0)

def collect_stock_data(state: StockAnalysisState) -> dict:
    if state.get("error"): return {}
    try:
        print("[Node 1] Collecting stock data...")
        ticker = resolve_ticker(state["company_stock"])
        stock_data = fetch_stock_data(ticker)
        
        if "New data not available" in stock_data:
            return {"error": f"Company '{state['company_stock']}' does not exist or data not available."}
        if "unavailable due to an error" in stock_data:
            return {"error": "fetching failed"}
            
        financial_data = fetch_stock_financials(ticker)
        if "unavailable due to an error" in financial_data:
            return {"error": "fetching failed"}
            
        return {
            "ticker": ticker,
            "stock_data": stock_data,
            "financial_data": financial_data,
        }
    except Exception as e:
        print(f"Error in Node 1: {e}")
        return {"error": "fetching failed"}

def read_news(state: StockAnalysisState) -> dict:
    if state.get("error"): return {}
    try:
        print("[Node 2] Summarizing news...")
        raw_news = fetch_stock_news(state["ticker"])
        if "unavailable due to an error" in raw_news:
            return {"error": "fetching failed"}
            
        prompt = f"""You are a 'News Reader' Agent.
Goal: Find and summarize the latest news articles about the company.
Backstory: A diligent researcher who keeps an eye on the latest financial news and trends that impact stock performance.

Find the latest financial news for {state['company_stock']} ({state['ticker']}) and summarize the key points from these recent articles:
{raw_news}

Provide a concise summary of the most recent and relevant news."""
        response = llm.invoke(prompt)
        return {"news_summary": response.content}
    except Exception as e:
        print(f"Error in Node 2: {e}")
        return {"error": "fetching failed"}

def research_market(state: StockAnalysisState) -> dict:
    if state.get("error"): return {}
    try:
        print("[Node 3] Researching market trends...")
        prompt = f"""You are a 'Stock Market Researcher' Agent.
Goal: Research stock performance, market trends and industry movements to provide insights.
Backstory: An experienced stock market researcher who gathers information from sources to offer insights about the performance of the company.

Conduct research on {state['company_stock']} ({state['ticker']}) focusing on these topics:
- General market trends affecting the company.
- Industry comparisons between competitors and recent events affecting the company.
- Risks and opportunities related to current market conditions.

Provide a clear analysis covering these exact points."""
        response = llm.invoke(prompt)
        return {"market_research": response.content}
    except Exception as e:
        print(f"Error in Node 3: {e}")
        return {"error": "fetching failed"}

def analyze_and_write_report(state: StockAnalysisState) -> dict:
    if state.get("error"): return {}
    try:
        print("[Node 4] Writing final report...")
        prompt = f"""You are a 'Financial Analyst' Agent.
Goal: Analyze financial stock data and use information about the company to write a comprehensive stock analysis report.
Backstory: A skilled financial analyst who analyzes company data and provides detailed stock reports.

Analyze the gathered research on {state['company_stock']} ({state['ticker']}) and write a comprehensive Markdown stock analysis report.
The report MUST include a definitive conclusion on whether this stock is a good investment (e.g., Strong Buy, Buy, Hold, Sell, or Strong Sell) and explicitly justify it using the quantitative data.

Use the following gathered data:

--- STOCK PRICE & METRICS ---
{state.get('stock_data', 'No stock data available')}

--- FINANCIAL STATEMENTS ---
{state.get('financial_data', 'No financial data available')}

--- RECENT NEWS ---
{state.get('news_summary', 'No news available')}

--- MARKET RESEARCH ---
{state.get('market_research', 'No market research available')}
"""
        response = llm.invoke(prompt)
        return {"final_report": response.content}
    except Exception as e:
        print(f"Error in Node 4: {e}")
        return {"error": "fetching failed"}

