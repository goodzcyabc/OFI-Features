# 📊 OFI-Features Extraction & Analysis

This project implements **Order Flow Imbalance (OFI)** feature computation from order book snapshot data, inspired by the paper:  
📄 _"Cross-impact of order flow imbalance in equity markets"_.

## 🧩 Project Structure

```bash
.
├── main.py                      # Main script to run OFI feature extraction
├── data/
│   └── loader.py               # Loads and preprocesses the orderbook data
├── features/
│   ├── ofi_best_level.py       # Computes best-level (Level 1) OFI per timestamp
│   ├── ofi_multi_level.py      # Computes multi-level OFI from snapshots
│   ├── ofi_integrated.py       # Aggregates multi-level OFI using PCA
│   └── ofi_cross_asset.py      # Computes cross-asset OFI using Lasso regression
├── first_25000_rows.csv        # Sample dataset (10-level order book snapshots)
```

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> Requirements include:
> - pandas
> - numpy
> - scikit-learn

### 2. Run the project

```bash
python main.py
```

You should see console output for:

- Multi-Level OFI
- Best-Level OFI
- Integrated OFI (via PCA)
- Cross-Asset OFI (skipped if only 1 symbol present)

## 📌 Feature Descriptions

### 🔹 Best-Level OFI (Level 1)
Computed using changes in **bid1/ask1** prices and sizes between events. Returns:
```csv
timestamp, symbol, ofi_best
```

### 🔹 Multi-Level OFI
Looped over 10 levels of the order book snapshot. For each timestamp:
```csv
timestamp, symbol, ofi_1, ofi_2, ..., ofi_10
```

### 🔹 Integrated OFI
Principal Component Analysis (PCA) is applied to `[ofi_1 ... ofi_10]`, yielding a single `ofi_integrated` feature per timestamp.

### 🔹 Cross-Asset OFI
Uses Lasso regression to regress each symbol’s integrated OFI against others:
```python
# output
{ 'AAPL': {
    'coefs': {'MSFT': 0.12, 'GOOG': -0.05, ...},
    'r2_score': 0.73
  }
}
```

## 📈 Sample Output

```text
✅ Multi-Level OFI computed.
✅ Best-Level OFI:
  symbol  timestamp                ofi_best
  AAPL    2024-10-21T11:54:00Z     200
  ...
✅ Integrated OFI PCA Weights:
  [0.02, 0.06, ..., 0.07]
⚠️ Only one symbol — skipping cross-asset OFI