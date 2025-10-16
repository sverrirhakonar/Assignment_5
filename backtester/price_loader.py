from datetime import datetime
import pandas as pd

# Space Complexity: O(N) where N is the number of data rows in the csv file.
# The function stores every parsed MarketDataPoint object in the data_points list,
# so memory usage grows linearly with the number of rows.
def load_market_data(file_path):
    '''Function that loads the market data to a list of MarketDataPoints '''
    data_points = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = pd.read_csv(file_path, header=True)
        #print(reader)
        
    return reader


print(load_market_data('market_data.csv'))
