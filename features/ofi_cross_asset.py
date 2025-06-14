from sklearn.linear_model import LassoCV

def compute_cross_asset_ofi(integrated_df):
    symbols = integrated_df['symbol'].unique()
    print("Symbols:", symbols)

    if len(symbols) <= 1:
        print("Only one symbol in data — skipping cross-asset OFI.")
        return {}

    pivot_df = integrated_df.pivot(index='timestamp', columns='symbol', values='ofi_integrated').fillna(0)

    lasso_models = {}
    for sym in symbols:
        y = pivot_df[sym]
        X = pivot_df.drop(columns=[sym])

        if X.shape[1] == 0:
            print(f"Not enough other symbols to predict {sym}, skipping.")
            continue

        model = LassoCV(cv=5, random_state=42).fit(X, y)
        lasso_models[sym] = {
            'model': model,
            'coefs': dict(zip(X.columns, model.coef_)),
            'intercept': model.intercept_
        }

    return lasso_models
