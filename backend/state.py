from typing import TypedDict, Optional

class StockAnalysisState(TypedDict):
    company_stock: str
    ticker: str
    stock_data: str
    financial_data: str
    news_summary: str
    market_research: str
    final_report: str
    error: Optional[str]
