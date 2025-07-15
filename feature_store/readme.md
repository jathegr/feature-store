# 🧠 Feature Store for Financial Analytics

This repository powers a daily-updated feature store for stock and crypto analytics, using OHLCV data and technical indicators to prepare robust datasets for predictive modeling.

---

## 🔄 Pipeline Overview

- 🏦 **Ingest**: Fetch bulk EOD data via Marketstack API (with multi-key rotation)
- 🧼 **Preprocess**: Clean gaps, deduplicate, and cap outliers
- 📊 **Transform**: Compute Bollinger Bands, RSI, MACD, rolling stats, and ratios
- 💾 **Store**: Persist features as partitioned Parquet (symbol/date)
- ☁️ **Cache**: Use iCloud Drive to store intermediate results across devices
- 🕒 **Automate**: GitHub Actions run build/backfill/realtime daily at 02:00 UTC
- 🔁 **Backfill**: Fill missing historical dates incrementally
- 📈 **Realtime**: Append latest features daily via `realtime_update.py`

---

## 🛠️ Setup

```bash
git clone https://github.com/jathegr/feature-store.git
cd feature-store
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt