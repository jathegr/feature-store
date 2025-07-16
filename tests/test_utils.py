import os, json
import pytest
from predictive_model.src.utils import save_json, load_json, get_logger

def test_json_roundtrip(tmp_path):
    data = {'foo': 'bar'}
    p = tmp_path / "test.json"
    save_json(data, p)
    loaded = load_json(p)
    assert loaded == data

def test_logger_returns_logger():
    lg = get_logger("test")
    assert hasattr(lg, "info")
