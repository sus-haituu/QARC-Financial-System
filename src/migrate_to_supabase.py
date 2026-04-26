import os
import re
import pandas as pd
from dotenv import load_dotenv

# Patch supabase SDK to accept the newer sb_publishable key format
import supabase._sync.client as _sync_client
_original_init = _sync_client.SyncClient.__init__

def _patched_init(self, supabase_url, supabase_key, options=None):
    """Patch to bypass JWT-only key validation for sb_publishable keys."""
    # Temporarily replace re.match to accept non-JWT keys
    _orig_match = re.match
    def _permissive_match(pattern, string, flags=0):
        if r"[A-Za-z0-9-_=]" in pattern and string.startswith("sb_"):
            return True  # Accept sb_publishable keys
        return _orig_match(pattern, string, flags)
    re.match = _permissive_match
    try:
        _original_init(self, supabase_url, supabase_key, options)
    finally:
        re.match = _orig_match

_sync_client.SyncClient.__init__ = _patched_init

from supabase import create_client, Client

def get_supabase_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase URL and Key must be defined in the .env file.")
    return create_client(url, key)

def migrate_data():
    supabase = get_supabase_client()
    
    csv_path = "data/NSE_CPSEETF - ML Training Data.csv.csv"
    if not os.path.exists(csv_path):
        csv_path = "../data/NSE_CPSEETF - ML Training Data.csv.csv"
        
    print(f"Reading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Rename columns to match the Supabase table schema
    df = df.rename(columns={
        "Date": "date",
        "Close": "close_price",
        "Relative Strength Index (RSI)": "rsi",
        "MACD Line": "macd"
    })
    
    # Convert date strings (M/D/YYYY) to ISO format for TIMESTAMPTZ
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%dT00:00:00+00:00")
    
    # Select only the specified columns
    data_to_upload = df[["date", "close_price", "rsi", "macd"]]
    
    # Convert dataframe to a list of dicts
    records = data_to_upload.where(pd.notnull(data_to_upload), None).to_dict(orient="records")
    
    print(f"Uploading {len(records)} records to Supabase 'market_data' table...")
    
    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        response = supabase.table("market_data").insert(batch).execute()
        print(f"  Uploaded batch {i//batch_size + 1} ({len(batch)} rows)")
        
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_data()
