# Stock Analyzer 

An AI-powered stock analysis platform that generates comprehensive investment reports using real-time market data. The application uses a multi-agent AI architecture (LangGraph) to research news, analyze financials, and provide definitive Buy/Hold/Sell recommendations.

## Features
- **Real-Time Data Extraction**: Fetches the latest stock price, history, and financial statements (P/E ratio, EPS, Market Cap) via Yahoo Finance.
- **AI News Reader Agent**: Scans and summarizes the most recent and relevant financial news for the requested company.
- **AI Market Researcher Agent**: Analyzes general market trends, industry comparisons, and risks/opportunities.
- **Expert Financial Analyst Agent**: Synthesizes all quantitative metrics and qualitative research to generate a comprehensive Markdown report with a definitive investment recommendation.
- **Robust Error Handling**: Automatically detects fake companies, strictly filters for current year news, and gracefully aborts if external APIs fail.
- **Modern React UI**: A sleek, responsive frontend with a dark/light mode, live loading indicators for agent progress, and styled Markdown rendering.

## Tech Stack
- **Frontend**: React, Vite, CSS Variables (No external UI libraries)
- **Backend**: Python, FastAPI
- **AI & Orchestration**: LangGraph, LangChain, Groq (Llama-3.3-70b-versatile)
- **Data APIs**: yfinance (Yahoo Finance)

---

##  How to Run Locally

### Prerequisites
- Python 3.9+
- Node.js & npm
- A [Groq API Key](https://console.groq.com/) for the AI models

### 1. Backend Setup (FastAPI & AI Agents)
Open a terminal and navigate to the root directory, then into the backend folder:
```bash
cd backend
```

Create a virtual environment and activate it:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```

Set up your environment variables by creating a `.env` file in the `backend/` folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Start the FastAPI backend server:
```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup (React UI)
Open a **new** terminal window (leave the backend running), and navigate to the frontend folder:
```bash
cd frontend
```

Install the Node modules:
```bash
npm install
```

Start the Vite development server:
```bash
npm run dev
```

Finally, open your browser and go to `http://localhost:5173` (or the port Vite provides) to use the Stock Analyzer AI!

---

## 📁 Project Structure

```
Stock_Analyzer_AI/
├── backend/
│   ├── main.py          # FastAPI entry point
│   ├── graph.py         # LangGraph parallel agent workflow
│   ├── nodes.py         # AI Agent logic and prompts
│   ├── tools.py         # yfinance data fetching tools
│   ├── state.py         # TypedDict for shared pipeline state
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx      # Main React application logic & UI
    │   ├── App.css      # Styling & CSS variables
    │   └── main.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```
