import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from expiry_day_logic import get_trade_signal
import os

st.title("Expiry Day Mean Reversion (Live Signal Tool)")

st.markdown("""
This app generates live signals based on 9:30 AM price move vs previous day close.
Strategy logic:
- If today's 9:30 AM price is **above threshold** : SHORT  
- If it's **below -threshold** : LONG  
- Else: No Trade  
""")

today = datetime.today().date()
next_thursday = today + timedelta((3 - today.weekday()) % 7)
selected_date = st.date_input("Select Expiry Date (Thursday only)", next_thursday)

if not (selected_date.weekday() == 3):
    st.error("Please select a Thursday (expiry day).")
    st.stop()

prev_close = st.number_input("Previous Day Close", value=275.0, step=0.1)
entry_price = st.number_input("Today’s 9:30 AM Price", value=276.5, step=0.1)
threshold = st.slider("Threshold (%)", 0.1, 1.0, value=0.5, step=0.1) / 100
entry_time = "09:30:00"
exit_time = "15:15:00"

if prev_close > 0 and entry_price > 0:
    signal = get_trade_signal(prev_close, entry_price, threshold)

    if signal != "no trade":
        st.success(f"Trade Signal: **{signal.upper()}**")
        move = (entry_price - prev_close) / prev_close
        st.markdown(f"Price Move: `{move * 100:.2f}%`")

        exit_price = st.number_input("Enter exit price at 3:15 PM", value=entry_price, step=0.1)
        if exit_price > 0:
            if signal == "long":
                ret = (exit_price - entry_price) / entry_price
            elif signal == "short":
                ret = (entry_price - exit_price) / entry_price

            st.metric(label="Return", value=f"{ret*100:.2f}%")

        if st.button("Save Trade"):
            trade = {
                "date": today,
                "direction": signal,
                "entry_time": entry_time,
                "entry_price": entry_price,
                "exit_time": exit_time,
                "exit_price": exit_price,
                "return": ret
            }

            file_path = "live_trades.csv"
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df = pd.concat([df, pd.DataFrame([trade])], ignore_index=True)
            else:
                df = pd.DataFrame([trade])

            df.to_csv(file_path, index=False)
            st.success("Trade saved to live_trades.csv!")
            
    else:
        st.warning("No trade signal based on threshold.")

st.markdown("---")
st.subheader("Live Trade Log")

try:
    df_log = pd.read_csv("live_trades.csv")
    df_log['date'] = pd.to_datetime(df_log['date'])
    df_log['cum_return'] = (1 + df_log['return']).cumprod()

    st.dataframe(df_log)

except FileNotFoundError:
    st.info("No trades saved yet")
