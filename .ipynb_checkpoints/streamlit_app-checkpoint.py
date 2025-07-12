import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Nifty Expiry Day Signal", layout="centered")

st.title("Expiry Day Mean Reversion (Live Signal Tool)")

st.markdown("""
This app generates live signals based on 9:30 AM price move vs previous day close.
Strategy logic:
- If today's 9:30 AM price is **+0.5% above** : SHORT  
- If it's **-0.5% below** : LONG  
- Else: No Trade  
""")

today = st.date_input("Trade Date", value=datetime.today())
prev_close = st.number_input("Previous Day Close", value=275.0, step=0.1)
price_930 = st.number_input("Today’s 9:30 AM Price", value=276.5, step=0.1)

signal = "No Trade"
direction = None
entry_price = price_930
entry_time = "09:30:00"
exit_time = "15:15:00"

if prev_close > 0:
    move = (price_930 - prev_close) / prev_close
    st.markdown(f"Price Move: `{move * 100:.2f}%`")

    if move >= 0.005:
        signal = "GO SHORT"
        direction = "short"
        st.success("Signal: GO SHORT")
    elif move <= -0.005:
        signal = "GO LONG"
        direction = "long"
        st.success("Signal: GO LONG")
    else:
        st.warning("No Trade: Move not significant")
else:
    st.error("Invalid Previous Close")


if direction:
    exit_price = st.number_input("Enter Exit Price (e.g. at 3:15 PM)", value=price_930, step=0.1)

    if direction == "long":
        trade_return = (exit_price - entry_price) / entry_price
    else:
        trade_return = (entry_price - exit_price) / entry_price

    st.markdown(f"**Return:** `{trade_return*100:.3f}%`")

    if st.button("Save Trade"):
        trade = {
            "date": today,
            "direction": direction,
            "entry_time": entry_time,
            "entry_price": entry_price,
            "exit_time": exit_time,
            "exit_price": exit_price,
            "return": trade_return
        }

        file_path = "live_trades.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame([trade])], ignore_index=True)
        else:
            df = pd.DataFrame([trade])

        df.to_csv(file_path, index=False)
        st.success("Trade saved to live_trades.csv!")

st.markdown("---")
st.subheader("Live Trade Log")

try:
    df_log = pd.read_csv("live_trades.csv")
    df_log['date'] = pd.to_datetime(df_log['date'])
    df_log['cum_return'] = (1 + df_log['return']).cumprod()

    st.dataframe(df_log)

except FileNotFoundError:
    st.info("No trades saved yet.")
