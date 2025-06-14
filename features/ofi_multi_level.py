import pandas as pd

def compute_multi_level_ofi_from_snapshots(df):
    results = []

    grouped = df.groupby(['symbol', 'timestamp'], sort=False)
    prev_row = {}

    for (symbol, timestamp), group in grouped:
        row = group.iloc[0]
        ofi_row = {'symbol': symbol, 'timestamp': timestamp}

        for level in range(10):
            bid_px_col = f'bid_px_{level:02d}'
            ask_px_col = f'ask_px_{level:02d}'
            bid_sz_col = f'bid_sz_{level:02d}'
            ask_sz_col = f'ask_sz_{level:02d}'

            ofi = 0

            # Check if previous row exists for comparison
            if symbol in prev_row:
                prev = prev_row[symbol]

                # Bid side
                if row[bid_px_col] > prev[bid_px_col]:
                    ofi += row[bid_sz_col]
                elif row[bid_px_col] < prev[bid_px_col]:
                    ofi -= prev[bid_sz_col]

                # Ask side
                if row[ask_px_col] < prev[ask_px_col]:
                    ofi += row[ask_sz_col]
                elif row[ask_px_col] > prev[ask_px_col]:
                    ofi -= prev[ask_sz_col]

            # Store result
            ofi_row[f'ofi_{level+1}'] = ofi

        prev_row[symbol] = row
        results.append(ofi_row)

    ofi_df = pd.DataFrame(results)
    return ofi_df
