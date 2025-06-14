import pandas as pd

def load_orderbook(filepath):
    df = pd.read_csv(filepath)
    df.rename(columns={'ts_event': 'timestamp'}, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by=['symbol', 'timestamp']).reset_index(drop=True)
    return df
