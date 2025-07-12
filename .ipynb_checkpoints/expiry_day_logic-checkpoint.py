import pandas as pd
from datetime import time

def generate_expiry_day_trades(df, entry_threshold=0.005, exit_time_str='15:15:00'):

    trades = []
    df = df.copy()
    df['weekday'] = pd.to_datetime(df['date']).dt.weekday  
    expiry_days = sorted(df[df['weekday'] == 3]['date'].unique())  # Thursdays only

    for expiry_day in expiry_days:
        day_df = df[df['date'] == expiry_day].sort_values('Datetime')
        prev_day = expiry_day - pd.Timedelta(days=1)

        prev_day_df = df[df['date'] < expiry_day]
        if prev_day_df.empty:
            continue  
                
        prev_close = prev_day_df.sort_values('Datetime').iloc[-1]['Close']

        entry_row = day_df[day_df['time'].astype(str) == "09:30:00"]
        exit_row = day_df[day_df['time'].astype(str) == exit_time_str]

        if entry_row.empty or exit_row.empty:
            continue

        entry_price = float(entry_row['Close'].values[0])
        exit_price = float(exit_row['Close'].values[0])
        move = (entry_price - prev_close) / prev_close

        if move >= entry_threshold:
            direction = 'short'
            ret = (entry_price - exit_price) / entry_price
        elif move <= -entry_threshold:
            direction = 'long'
            ret = (exit_price - entry_price) / entry_price
        else:
            continue  # no trade

        trades.append({
            'date': expiry_day,
            'direction': direction,
            'entry_time': '09:30:00',
            'entry_price': entry_price,
            'exit_time': exit_time_str,
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