import pandas as pd

def compute_best_level_ofi_from_events(df, window='1min'):
    df = df.sort_values(['symbol', 'timestamp']).copy()
    # Explicit numeric conversion
    for col in ['bid_px_00','bid_sz_00','ask_px_00','ask_sz_00']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    grp = df.groupby('symbol')
    df['prev_bid_px'] = grp['bid_px_00'].shift(1)
    df['prev_bid_sz'] = grp['bid_sz_00'].shift(1)
    df['prev_ask_px'] = grp['ask_px_00'].shift(1)
    df['prev_ask_sz'] = grp['ask_sz_00'].shift(1)

    def ofi_calc(r):
        if pd.isna(r.prev_bid_px):
            return 0
        # Bid logic
        if r.bid_px_00 > r.prev_bid_px:
            ob = r.bid_sz_00
        elif r.bid_px_00 == r.prev_bid_px:
            ob = r.bid_sz_00 - r.prev_bid_sz
        else:
            ob = -r.prev_bid_sz
        # Ask logic (correctly implemented)
        if r.ask_px_00 > r.prev_ask_px:
            oa = -r.prev_ask_sz
        elif r.ask_px_00 == r.prev_ask_px:
            oa = r.ask_sz_00 - r.prev_ask_sz
        else:
            oa = r.ask_sz_00
        return ob - oa

    df['ofi_event'] = df.apply(ofi_calc, axis=1)
    result = (
        df.groupby(['symbol', pd.Grouper(key='timestamp', freq=window)])
          ['ofi_event']
          .sum()
          .reset_index()
          .rename(columns={'ofi_event': 'ofi_best'})
    )
    return result
