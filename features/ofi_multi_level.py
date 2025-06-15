import pandas as pd

def compute_multi_level_ofi_from_snapshots(df, max_levels=10):
    df = df.sort_values(['symbol', 'timestamp']).reset_index(drop=True)
    prev = {}
    records = []

    for _, row in df.iterrows():
        sym = row['symbol']
        ts = row['timestamp']
        prev_row = prev.get(sym)
        ofi = {'symbol': sym, 'timestamp': ts}

        for m in range(max_levels):
            bp = f'bid_px_{m:02d}'
            bs = f'bid_sz_{m:02d}'
            ap = f'ask_px_{m:02d}'
            az = f'ask_sz_{m:02d}'

            if prev_row is None:
                ofi[f'ofi_{m+1}'] = 0
                continue

            bp_t, bp_p = row[bp], prev_row[bp]
            bs_t, bs_p = row[bs], prev_row[bs]

            ap_t, ap_p = row[ap], prev_row[ap]
            az_t, az_p = row[az], prev_row[az]

            # Bid-side OFI
            if bp_t > bp_p:
                ob = bs_t
            elif bp_t == bp_p:
                ob = bs_t - bs_p
            else:
                ob = -bs_p

            # Ask-side OFI
            if ap_t > ap_p:
                oa = -az_p
            elif ap_t == ap_p:
                oa = az_t - az_p
            else:
                oa = az_t

            ofi[f'ofi_{m+1}'] = ob - oa

        prev[sym] = row
        records.append(ofi)

    return pd.DataFrame(records)
