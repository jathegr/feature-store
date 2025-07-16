#!/usr/bin/env python3
"""
Launcher for the predictive_model test suite.
Usage: python test_predictive_model.py
"""

import os
import sys
import pytest

HERE     = os.path.dirname(__file__)
PKG_SRC  = os.path.join(HERE, "predictive_model", "src")
PKG_ROOT = HERE  # so feature_store/ is importable

# Prepend both paths
for p in (PKG_SRC, PKG_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

if __name__ == "__main__":
    sys.exit(pytest.main([
        "tests",
        "--maxfail=1",
        "--disable-warnings",
        "-q",
    ]))
