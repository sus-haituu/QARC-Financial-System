import os
import re
from dotenv import load_dotenv

# Patch supabase SDK to accept the newer sb_publishable key format
import supabase._sync.client as _sync_client
_original_init = _sync_client.SyncClient.__init__

def _patched_init(self, supabase_url, supabase_key, options=None):
    """Patch to bypass JWT-only key validation for sb_publishable keys."""
    _orig_match = re.match
    def _permissive_match(pattern, string, flags=0):
        if r"[A-Za-z0-9-_=]" in pattern and string.startswith("sb_"):
            return True
        return _orig_match(pattern, string, flags)
    re.match = _permissive_match
    try:
        _original_init(self, supabase_url, supabase_key, options)
    finally:
        re.match = _orig_match

_sync_client.SyncClient.__init__ = _patched_init

from supabase import create_client, Client


class SupabaseManager:
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Supabase URL and Key must be defined in the .env file.")
        self.client: Client = create_client(url, key)
        
    def fetch_latest_market_data(self, limit: int = 90):
        """Fetch the latest market data rows from the cloud, returning ascending chronological order."""
        response = self.client.table("market_data").select("*").order("date", desc=True).limit(limit).execute()
        data = response.data
        if data:
            data.reverse()  # Reverse to ascending order
        return data
        
    def save_ai_memory(self, analysis_text: str):
        """Save analysis to the ai_memories table."""
        data = {"content": analysis_text}
        response = self.client.table("ai_memories").insert(data).execute()
        return response.data


# Global instance of SupabaseManager
supabase_manager = SupabaseManager()


def get_market_analysis():
    """
    Replaces the CSV loading logic by directly fetching the latest 90 rows 
    from the cloud using SupabaseManager.
    """
    print("Fetching the latest 90 past days of market data from Supabase...")
    data = supabase_manager.fetch_latest_market_data(limit=90)
    return data


def save_prediction_memory(analysis_text: str):
    """
    Allows the Llama-3 model (or any logic) to save its final analysis 
    into the ai_memories table for persistence.
    """
    print("Saving AI analysis to Supabase memories...")
    return supabase_manager.save_ai_memory(analysis_text)

def run_prediction():
    """
    Main prediction pipeline:
    1. Fetch Supabase market data.
    2. Run the LSTM model.
    3. Run Llama-3 strategy assessment.
    4. Save the strategy to the ai_memories table.
    """
    print("Running full prediction pipeline...")
    # 1. Fetch data
    market_data = get_market_analysis()
    
    # 2. Run LSTM (Mocked for now until model inference is merged)
    lstm_projected_price = 155.42 
    
    # 3. Compile Strategy (Mocked Llama-3 output)
    strategy_report = f"Based on the last {len(market_data)} days of data and an LSTM projection of ${lstm_projected_price}, the QARC AI recommends a HOLD position."
    
    # 4. Save to memories
    save_prediction_memory(strategy_report)
    
    return {
        "lstm_prediction": lstm_projected_price,
        "llama_strategy": strategy_report,
        "data_points_analyzed": len(market_data)
    }

if __name__ == "__main__":
    result = run_prediction()
    print("Pipeline result:", result)