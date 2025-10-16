import pandas as pd

def load_market_data(file_path: str) -> pd.Series:
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp').sort_index()
    df['price'] = pd.to_numeric(df['price'], errors='coerce').astype(float)
    return df
