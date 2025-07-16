from fastapi import FastAPI
from pydantic import BaseModel
from feature_store.utils.schema import FEATURE_SCHEMA
from feature_store.offline.storage import read_features

app = FastAPI()

class FeatureRequest(BaseModel):
    symbol: str
    date:   str  # YYYY-MM-DD

@app.post("/features")
def get_features(req: FeatureRequest):
    df = read_features("engineered", symbols=[req.symbol], start=req.date, end=req.date)
    if df.empty:
        return {"symbol": req.symbol, "date": req.date, "features": {}}
    row = df.iloc[-1].to_dict()
    # filter out symbol & date
    features = {k: v for k, v in row.items() if k not in ["symbol", "date"]}
    return {"symbol": req.symbol, "date": req.date, "features": features}