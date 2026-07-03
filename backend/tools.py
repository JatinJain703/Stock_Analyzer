import yfinance as yf
import requests
import datetime

def resolve_ticker(company_input: str) -> str:
    """Try to resolve company name to ticker using Yahoo Finance Search."""
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_input}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0]['symbol']
    except Exception:
        pass
    return company_input.upper()

def fetch_stock_data(ticker: str) -> str:
    """Fetch current stock price data and 1-month history."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1mo")
        
        if hist.empty:
            return f"Stock Data for {ticker}:\nNew data not available"

        latest_date = hist.index[-1].date()
        current_date = datetime.datetime.now().date()
        
        if (current_date - latest_date).days > 7:
            return f"Stock Data for {ticker}:\nNew data not available"

        output = f"Stock Data for {ticker}:\n"
        output += f"P/E Ratio: {info.get('forwardPE', 'N/A')}\n"
        output += f"EPS: {info.get('trailingEps', 'N/A')}\n"
        output += f"Market Cap: {info.get('marketCap', 'N/A')}\n"
        output += f"Previous Close: {info.get('previousClose', 'N/A')}\n\n"
        output += "Historical Prices (Past Month):\n"
        for date, row in hist.iterrows():
            output += f"Date: {date.date()}, Close: {row['Close']:.2f}\n"
        return output
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return f"Stock Data for {ticker}:\nData currently unavailable due to an error."

def fetch_stock_financials(ticker: str) -> str:
    """Fetch income statement, balance sheet, and cash flow."""
    try:
        stock = yf.Ticker(ticker)
        output = f"Financial Statements for {ticker}:\n\n"
        output += "Income Statement:\n" + stock.income_stmt.to_string() + "\n\n"
        output += "Balance Sheet:\n" + stock.balance_sheet.to_string() + "\n"
        return output
    except Exception as e:
        print(f"Error fetching financials for {ticker}: {e}")
        return f"Financial Statements for {ticker}:\nData currently unavailable due to an error."

def fetch_stock_news(ticker: str) -> str:
    """Fetch recent news articles related to the company stock of a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news

        current_year = str(datetime.datetime.now().year)
        news_summary = []
        
        for item in news_items:
            content = item.get('content', item)
            
            pub_date = content.get('pubDate', '')
            if pub_date and not pub_date.startswith(current_year):
                continue
                
            title = content.get('title', 'No title available')
            publisher_raw = content.get('provider', content.get('publisher', {}))
            publisher = publisher_raw.get('displayName', publisher_raw) if isinstance(publisher_raw, dict) else publisher_raw
            link_obj = content.get('canonicalUrl', content.get('link', {}))
            link = link_obj.get('url', link_obj) if isinstance(link_obj, dict) else link_obj
            
            news_summary.append(f"- {title} (by {publisher})\n  {link}")
            
            if len(news_summary) >= 5:
                break

        return "Recent News:\n" + "\n".join(news_summary) if news_summary else "New news data not available for the current year."
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return "Recent News:\nData currently unavailable due to an error."

