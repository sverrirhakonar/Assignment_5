from datetime import datetime
import pandas as pd

def load_market_data(file_path: str) -> pd.DataFrame:
    """Load market data CSV into a pandas DataFrame."""
    df = pd.read_csv(file_path).set_index('timestamp')   # pandas handles opening/closing
    return df

print(load_market_data('market_data.csv'))