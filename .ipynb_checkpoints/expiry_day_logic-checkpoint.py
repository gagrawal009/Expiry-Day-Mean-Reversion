import pandas as pd
from datetime import time

def generate_expiry_day_trades(df, entry_threshold=0.005, exit_time_str='15:15:00', target_return=0.004, stop_loss=0.003):
    trades = []
    df = df.copy()
    df['weekday'] = pd.to_datetime(df['date']).dt.weekday
    expiry_days = sorted(df[df['weekday'] == 3]['date'].unique())  # Thursdays

    for expiry_day in expiry_days:
        day_df = df[df['date'] == expiry_day].sort_values('Datetime')

        prev_day_df_all = df[df['date'] < expiry_day]
        if prev_day_df_all.empty or day_df.empty:
            continue

        prev_day = prev_day_df_all['date'].max()
        prev_day_df = df[df['date'] == prev_day].sort_values('Datetime')
        prev_close = prev_day_df.iloc[-1]['Close']

        # Entry logic
        entry_row = day_df[day_df['time'].astype(str) == "09:30:00"]
        if entry_row.empty:
            continue

        entry_price = float(entry_row['Close'].values[0])
        move = (entry_price - prev_close) / prev_close

        if move >= entry_threshold:
            direction = 'short'
        elif move <= -entry_threshold:
            direction = 'long'
        else:
            continue  # No trade

        exit_price = None
        exit_time = None
        #Exit logic
        for _, row in day_df.iterrows():
            current_price = row['Close']
            current_time = row['time']

            if direction == 'long':
                ret = (current_price - entry_price) / entry_price
            elif direction == 'short':
                ret = (entry_price - current_price) / entry_price

            if ret >= target_return:
                exit_price = current_price
                exit_time = current_time
                break
            elif ret <= -stop_loss:
                exit_price = current_price
                exit_time = current_time
                break

        if exit_price is None:
            final_row = day_df[day_df['time'].astype(str) == exit_time_str]
            if final_row.empty:
                continue
            exit_price = float(final_row['Close'].values[0])
            exit_time = exit_time_str

            if direction == 'long':
                ret = (exit_price - entry_price) / entry_price
            elif direction == 'short':
                ret = (entry_price - exit_price) / entry_price

        trades.append({
            'date': expiry_day,
            'direction': direction,
            'entry_time': '09:30:00',
            'entry_price': entry_price,
            'exit_time': exit_time,
            'exit_price': exit_price,
            'return': ret
        })

    return pd.DataFrame(trades)


def get_trade_signal(prev_close, entry_price, threshold=0.005):

    move = (entry_price - prev_close) / prev_close
    if move >= threshold:
        return 'short'
    elif move <= -threshold:
        return 'long'
    else:
        return 'no trade'