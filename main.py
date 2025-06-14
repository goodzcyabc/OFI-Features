from data.loader import load_orderbook
from features.ofi_multi_level import compute_multi_level_ofi_from_snapshots
from features.ofi_best_level import compute_best_level_ofi_from_events
from features.ofi_integrated import compute_integrated_ofi
from features.ofi_cross_asset import compute_cross_asset_ofi

def main():
    df = load_orderbook("first_25000_rows.csv")

    # Multi-Level OFI
    multi_ofi = compute_multi_level_ofi_from_snapshots(df)
    print("\nMulti-Level OFI computed.")
    print(multi_ofi.head())

    # Best-Level OFI
    best_ofi_df = compute_best_level_ofi_from_events(df)
    print("\nBest-Level OFI:")
    print(best_ofi_df.head())

    # Integrated OFI
    integrated_df, weights = compute_integrated_ofi(multi_ofi)
    print("\nIntegrated OFI PCA Weights:", weights)
    print("\nIntegrated OFI Preview:")
    print(integrated_df[['symbol', 'timestamp', 'ofi_integrated']].head())


    # Cross-Asset OFI
    lasso_results = compute_cross_asset_ofi(integrated_df)
    if not lasso_results:
        print("Only one symbol in data — skipping cross-asset OFI.")
        print("Skipping cross-asset OFI output (not enough symbols).")
    else:
        for sym, result in lasso_results.items():
            print(f"\nTop cross-impact coefficients for {sym}:")
            sorted_coefs = sorted(result['coefs'].items(), key=lambda x: abs(x[1]), reverse=True)
            print(sorted_coefs[:5])

if __name__ == "__main__":
    main()