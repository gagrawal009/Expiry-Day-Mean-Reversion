#Strategy Idea: Expiry-Day Mean Reversion

##Rationale:
On expiry days, the NIFTY 50 index often experiences sharp opening moves due to option unwinding and volatility risk premiums. These moves tend to mean-revert during the day.

Logic:

If price at 9:30 AM is:
- More than +0.3% above previous close : short
- More than -0.3% below previous close : long
- Otherwise : no trade

Exit is at 3:15 PM

##Files Explained

- data_download.py - Downloads last 60 day NIFTYBEES intraday data (set dates for last 60 days)
- expiry_day_logic.py - Implements trade logic and generates backtest signals
- data_cleaning_and_analysis.ipynb - Clean and Analyse the NIFTYBEES data
- strategy_analysis.ipynb - Inspect expiry behavior and analyse strategy
- backtest_results.ipynb - Analyzes historical trades and performance             
- streamlit_app.py - Live tool to generate trade signals using current data
- nifty_intraday_15m.csv- Raw price data for NIFTYBEES downloaded from data_download.py
- nifty_intraday_15m_cleaned.csv- Cleaned intraday price data for NIFTY 
- expiry_trades.csv - Stores all valid backtest trades                       
- live_trades.csv - Logs trades made using the Streamlit app               

##How to Run
1. Install Requirements
pip install -r requirements.txt

3. Run Backtest & Data/Strategy Analysis

# Open and run these notebooks:
data_cleaning_and_analysis.ipynb
strategy_analysis.ipynb
backtest_results.ipynb

3. Run the Live Signal App
streamlit run streamlit_app.py

