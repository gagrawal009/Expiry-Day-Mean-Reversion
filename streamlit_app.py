import streamlit as st
import pandas as pd
import numpy as np
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
Exit happens when target return or stop loss is hit, or at 3:15 PM close.
(Intraday prices are simulated using a random walk. Can be modified to upload data)
""")

today = datetime.today().date()
next_thursday = today + timedelta((3 - today.weekday()) % 7)
selected_date = st.date_input("Select Expiry Date (Thursday only)", next_thursday)

if not (selected_date.weekday() == 3):
    st.error("Please select a Thursday (expiry day).")
    st.stop()

prev_close = st.number_input("Previous Day Close", value=275.00, step=0.1)
entry_price = st.number_input("Today’s 9:30 AM Price", value=276.5, step=0.1)
threshold = st.slider("Entry Threshold (%)", 0.1, 1.0, value=0.3, step=0.1) / 100
target_return = st.slider("Target Return (%)", 0.1, 1.0, value=0.4, step=0.1) / 100
stop_loss = st.slider("Stop Loss (%)", 0.1, 1.0, value=0.3, step=0.1) / 100

entry_time = "09:30:00"
exit_time = "15:15:00"

if prev_close > 0 and entry_price > 0:
    signal = get_trade_signal(prev_close, entry_price, threshold)

    if signal != "no trade":
        st.success(f"Trade Signal: **{signal.upper()}**")
        move = (entry_price - prev_close) / prev_close
        st.markdown(f"Price Move: `{move * 100:.2f}%`")

        times = pd.date_range("09:30", "15:15", freq="15min").time

        prices = [entry_price]

        # Simulate small random walk intraday prices
        for _ in range(1, len(times)):
            change = np.random.normal(loc=0, scale=0.05)  # small noise
            new_price = max(prices[-1] + change, 0)
            prices.append(round(new_price, 2))

        # Determine exit price/time by checking when target or stop loss is hit
        exit_price = prices[-1]
        exit_reason = "Close"

        for t, price in zip(times, prices):
            if signal == "long":
                ret = (price - entry_price) / entry_price
            else:  # signal == "short"
                ret = (entry_price - price) / entry_price

            if ret >= target_return:
                exit_price = price
                exit_time = t.strftime("%H:%M:%S")
                exit_reason = "Target Hit"
                break
            elif ret <= -stop_loss:
                exit_price = price
                exit_time = t.strftime("%H:%M:%S")
                exit_reason = "Stop Loss Hit"
                break

        # Calculate final return
        if signal == "long":
            ret = (exit_price - entry_price) / entry_price
        elif signal == "short":
            ret = (entry_price - exit_price) / entry_price

        st.metric(label="Return", value=f"{ret * 100:.2f}%")
        st.markdown(f"**Exit Time:** {exit_time}  \n**Exit Price:** {exit_price:.2f}  \n**Exit Reason:** {exit_reason}")

        if st.button("Save Trade"):
            trade = {
                "date": selected_date,
                "direction": signal,
                "entry_time": entry_time,
                "entry_price": entry_price,
                "exit_time": exit_time,
                "exit_price": exit_price,
                "return": ret,
                "exit_reason": exit_reason,
                "target": target_return,
                "stop_loss": stop_loss
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
    st.info("No trades saved yet.")
