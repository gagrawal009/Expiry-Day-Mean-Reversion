# Expiry-Day Mean Reversion Strategy

## Strategy Idea

On expiry days, the NIFTY 50 index often experiences sharp opening moves due to option unwinding and volatility risk premiums. These moves tend to **mean-revert** during the day.

### Strategy Logic

- If the 9:30 AM price is:
  - More than **+0.3% above** the previous close → Take a **short** position
  - More than **-0.3% below** the previous close → Take a **long** position
  - Otherwise → **No trade**
- Exit all trades at **3:15 PM**

## Project Files

- `data_download.py` – Downloads last 60 days of 15-minute NIFTYBEES intraday data
- `expiry_day_logic.py` – Implements the mean-reversion trade logic and signal generator
- `data_cleaning_and_analysis.ipynb` – Cleans and visualizes the raw NIFTYBEES data
- `strategy_analysis.ipynb` – Explores expiry day behavior and signal distribution
- `backtest_results.ipynb` – Analyzes trade results and calculates performance metrics
- `streamlit_app.py` – Live tool to generate signals and simulate trades interactively
- `nifty_intraday_15m.csv` – Raw intraday data from yfinance
- `nifty_intraday_15m_cleaned.csv` – Cleaned version of intraday dataset
- `expiry_trades.csv` – Contains historical trades generated from backtest logic
- `live_trades.csv` – Stores live trades taken via the Streamlit app

## How to Run the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Backtest & Analysis

Open and run the following Jupyter notebooks in order:
1. `data_cleaning_and_analysis.ipynb`
2. `strategy_analysis.ipynb`
3. `backtest_results.ipynb`

### 3. Launch the Live Signal App
Interactive Streamlit App: Visualize strategy signals, P&L, and tweak threshold to explore how the mean-reversion logic performs across different expiry days.
```bash
streamlit run streamlit_app.py
```
