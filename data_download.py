import yfinance as yf
import pandas as pd

def download_data(start_date, end_date):
    ticker = "NIFTYBEES.NS"  # ETF that tracks Nifty 50
    interval = "15m"
    df = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
    df = df.reset_index()
    df['date'] = df['Datetime'].dt.date
    df['time'] = df['Datetime'].dt.time
    df.to_csv("nifty_intraday_15m.csv", index=False)
    print("Saved to nifty_intraday_15m.csv")

if __name__ == "__main__":
    start = "2025-05-18"
    end = "2025-07-12"
    download_data(start, end)