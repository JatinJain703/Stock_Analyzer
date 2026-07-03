import { useState, useEffect } from 'react'
import './App.css'

const API_BASE = "http://localhost:8000"

const loadingSteps = [
  "Identifying ticker symbol...",
  "Fetching price data and history...",
  "Scanning latest news...",
  "Pulling quarterly financials...",
  "Running analyst agent...",
  "Writing final report..."
]

const popularCompanies = ["Apple", "Tesla", "Microsoft", "Google", "Reliance Industries", "TCS"]

function App() {
  const [screen, setScreen] = useState('input')
  const [errorMessage, setErrorMessage] = useState('')
  const [companyInput, setCompanyInput] = useState('')
  const [loadingStepIndex, setLoadingStepIndex] = useState(0)
  const [resultData, setResultData] = useState(null)
  const [activeTab, setActiveTab] = useState('report')

  useEffect(() => {
    let interval;
    if (screen === 'loading') {
      setLoadingStepIndex(0);
      interval = setInterval(() => {
        setLoadingStepIndex(prev => Math.min(prev + 1, loadingSteps.length - 1))
      }, 5000);
    }
    return () => clearInterval(interval);
  }, [screen]);

  const handleAnalyze = async (companyNameOverride) => {
    const nameToAnalyze = typeof companyNameOverride === 'string' ? companyNameOverride : companyInput;
    if (!nameToAnalyze.trim()) return;
    
    setCompanyInput(nameToAnalyze);
    setScreen('loading');
    
    try {
      setErrorMessage('');
      const response = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_stock: nameToAnalyze })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        if (errorData && errorData.detail) {
          throw new Error(errorData.detail);
        } else {
          throw new Error('fetching failed');
        }
      }
      
      const data = await response.json();
      setResultData(data);
      setScreen('result');
      setActiveTab('report');
    } catch (error) {
      console.error("Analysis failed:", error);
      setErrorMessage(error.message || 'fetching failed');
      setScreen('error');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleAnalyze();
    }
  };

  return (
    <div className="app-container">
      {screen === 'input' && (
        <>
          <div className="header">
            <h1>Stock Analyzer</h1>
            <p>Enter a company name to generate an AI-powered analysis report</p>
          </div>
          <div className="input-form">
            <input 
              type="text"
              className="input-field"
              placeholder="e.g. Apple, Tesla, Reliance Industries"
              value={companyInput}
              onChange={(e) => setCompanyInput(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button className="btn-primary" onClick={handleAnalyze} disabled={!companyInput.trim()}>
              Analyze
            </button>
          </div>
          <div className="popular-chips">
            {popularCompanies.map(comp => (
              <button 
                key={comp} 
                className="chip"
                onClick={() => handleAnalyze(comp)}
              >
                {comp}
              </button>
            ))}
          </div>
        </>
      )}

      {screen === 'loading' && (
        <div className="loading-container">
          <h2 className="loading-title">Analyzing {companyInput}...</h2>
          <div className="loading-step-box">
            <div className="spinner"></div>
            <span>{loadingSteps[loadingStepIndex]}</span>
          </div>
          <div className="progress-bar">
            {loadingSteps.map((_, idx) => (
              <div 
                key={idx} 
                className={`progress-block ${idx <= loadingStepIndex ? 'active' : ''}`}
              />
            ))}
          </div>
        </div>
      )}

      {screen === 'error' && (
        <div className="error-card">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p>{errorMessage}</p>
          <button className="btn-primary" onClick={() => setScreen('input')}>
            Try again
          </button>
        </div>
      )}

      {screen === 'result' && resultData && (
        <>
          <button className="back-btn" onClick={() => setScreen('input')}>
            &larr; New analysis
          </button>
          
          <div className="result-header">
            <div className="ticker-symbol">{resultData.ticker}</div>
            <div className="ticker-name">{companyInput}</div>
          </div>
          
          <div className="tabs">
            <button 
              className={`tab-btn ${activeTab === 'report' ? 'active' : ''}`}
              onClick={() => setActiveTab('report')}
            >
              Full Report
            </button>
            <button 
              className={`tab-btn ${activeTab === 'news' ? 'active' : ''}`}
              onClick={() => setActiveTab('news')}
            >
              News Summary
            </button>
            <button 
              className={`tab-btn ${activeTab === 'research' ? 'active' : ''}`}
              onClick={() => setActiveTab('research')}
            >
              Market Research
            </button>
          </div>
          
          <div className="tab-content">
            {activeTab === 'report' && (
              <div 
                className="prose"
                dangerouslySetInnerHTML={{ __html: resultData.report_html }} 
              />
            )}
            {activeTab === 'news' && (
              <div className="plain-text-content">
                {resultData.news_summary}
              </div>
            )}
            {activeTab === 'research' && (
              <div className="plain-text-content">
                {resultData.market_research}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default App
