from sklearn.decomposition import PCA
import numpy as np

def compute_integrated_ofi(multi_ofi_df):
    feature_cols = [col for col in multi_ofi_df.columns if col.startswith('ofi_')]
    X = multi_ofi_df[feature_cols].fillna(0).values

    print("OFI matrix preview (for PCA):")
    print(multi_ofi_df[feature_cols].describe())

    # Check for zero variance
    total_variance = np.var(X, axis=0).sum()
    if total_variance == 0:
        print("⚠️ All OFI features are constant or zero. Skipping PCA.")
        multi_ofi_df['ofi_integrated'] = 0
        weights = np.zeros(len(feature_cols))
        return multi_ofi_df, weights

    # PCA
    pca = PCA(n_components=1)
    principal = pca.fit_transform(X)
    weights = pca.components_[0]
    weights /= np.sum(np.abs(weights))  # normalize for interpretation

    multi_ofi_df['ofi_integrated'] = principal.flatten()
    return multi_ofi_df, weights
