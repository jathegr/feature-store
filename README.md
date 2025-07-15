# Feature Store

This repository contains a modular feature store for ingesting, transforming, and serving OHLCV-based financial features. It supports Parquet & SQL persistence, iCloud Drive caching, backfill routines, and real-time updates.

## Daily Scripts
- Build: `scripts/build_feature_store.py`
- Backfill: `scripts/backfill_feature_store.py`
- Realtime: `scripts/realtime_update.py`

## Setup
- Python 3.10+
- Install dependencies:
  ```bash
  pip install -r requirements.txt

---

## ⏰ 5. Add GitHub Actions Workflow

Create this file:  
`.github/workflows/daily-tasks.yml`

```yaml
name: Daily Feature Store Jobs

on:
  schedule:
    - cron: '0 2 * * *'  # 2am UTC daily

jobs:
  run-jobs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install requests pandas numpy pyarrow sqlalchemy psycopg2-binary

      - name: Run build script
        run: python feature_store/scripts/build_feature_store.py

      - name: Run backfill
        run: python feature_store/scripts/backfill_feature_store.py

      - name: Run realtime update
        run: python feature_store/scripts/realtime_update.py