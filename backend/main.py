from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import markdown
from graph import stock_analysis_graph      
from state import StockAnalysisState

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class RequestInfo(BaseModel):
    company_stock: str

@app.post("/analyze")
def analyze(req: RequestInfo):
    initial_state = {"company_stock": req.company_stock}
    result = stock_analysis_graph.invoke(initial_state)
    
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
        
    return {
        "ticker": result.get("ticker", ""),
        "report_markdown": result.get("final_report", ""),
        "report_html": markdown.markdown(result.get("final_report", "")),
        "news_summary": result.get("news_summary", ""),
        "market_research": result.get("market_research", "")
    }
