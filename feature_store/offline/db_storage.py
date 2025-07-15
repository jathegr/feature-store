import pandas as pd
from sqlalchemy import create_engine
from feature_store.config import DB_URL

engine = create_engine(DB_URL, echo=False)

def write_features_db(df: pd.DataFrame, table_name: str):
    """
    Append or create feature table in SQL database.
    """
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

def read_features_db(
    table_name: str,
    symbols: list[str] = None,
    start: str = None,
    end: str = None
) -> pd.DataFrame:
    """
    Query feature table with optional filters.
    """
    sql = f"SELECT * FROM {table_name}"
    conds = []
    if symbols:
        syms = ",".join(f"'{s}'" for s in symbols)
        conds.append(f"symbol IN ({syms})")
    if start:
        conds.append(f"date >= '{start}'")
    if end:
        conds.append(f"date <= '{end}'")
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    return pd.read_sql(sql, engine)