import pandas as pd
from collections import deque
from io import StringIO
import datetime

def get_n_rows(period): 
    now = datetime.datetime.now()

    if period == 'Today':
        start = datetime.datetime.combine(now.date(), datetime.datetime.min.time())
        seconds_since_midnight = (now - start).total_seconds()
        n_rows = seconds_since_midnight / 20
        return int(n_rows)
    
    elif period == 'Last week':
        seconds_in_week = 7*24*60*60
        n_rows = seconds_in_week / 20
        return int(n_rows)
    
    elif period == 'Last month':
        return 30*24*60*3 # roughly 3 readings per minute
    
    elif 'All' in period:
        return 99999999999 # deque accounts for too large numbers!
    else:
        return 10000
    
def get_data(n_rows):
    with open('../gas.csv', 'r') as f:
        q = deque(f, n_rows)  
    df = pd.read_csv(StringIO(''.join(q)), 
                     header=None, usecols=[1,2,3], parse_dates=['timestamp'],
                     names=['timestamp', 'mainnet', 'linea'])
    return df