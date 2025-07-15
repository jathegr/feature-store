# Feature Store

This module provides:

- Offline ingestion of raw market data.
- Transform functions to compute rolling and technical features.
- Storage layer persisting features as Parquet.
- Online API to serve feature vectors for scoring.
- Utilities for caching and schema definitions.