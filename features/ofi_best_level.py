import pandas as pd

def compute_best_level_ofi_from_events(df, window='1min'):
    # Ensure numeric and sorted
    df = df.sort_values(['symbol', 'timestamp']).copy()
    df['bid_px_00'] = pd.to_numeric(df['bid_px_00'], errors='coerce')
    df['ask_px_00'] = pd.to_numeric(df['ask_px_00'], errors='coerce')
    df['bid_sz_00'] = pd.to_numeric(df['bid_sz_00'], errors='coerce')
    df['ask_sz_00'] = pd.to_numeric(df['ask_sz_00'], errors='coerce')

    # Shift for price/size deltas
    df['prev_bid_px'] = df.groupby('symbol')['bid_px_00'].shift(1)
    df['prev_bid_sz'] = df.groupby('symbol')['bid_sz_00'].shift(1)
    df['prev_ask_px'] = df.groupby('symbol')['ask_px_00'].shift(1)
    df['prev_ask_sz'] = df.groupby('symbol')['ask_sz_00'].shift(1)

    df['ofi_event'] = 0

    # Compute OFI based on rules
    bid_move_up = (df['bid_px_00'] > df['prev_bid_px'])
    bid_move_down = (df['bid_px_00'] < df['prev_bid_px'])
    ask_move_down = (df['ask_px_00'] < df['prev_ask_px'])
    ask_move_up = (df['ask_px_00'] > df['prev_ask_px'])

    df.loc[bid_move_up, 'ofi_event'] = df['bid_sz_00']
    df.loc[bid_move_down, 'ofi_event'] = -df['prev_bid_sz']
    df.loc[ask_move_down, 'ofi_event'] += df['ask_sz_00']
    df.loc[ask_move_up, 'ofi_event'] -= df['prev_ask_sz']

    # Aggregate over time windows
    result = df.groupby(['symbol', pd.Grouper(key='timestamp', freq=window)])['ofi_event'].sum().reset_index()
    result.rename(columns={'ofi_event': 'ofi_best'}, inplace=True)
    return result
