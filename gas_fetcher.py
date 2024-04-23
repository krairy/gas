from web3 import Web3
import time
from datetime import datetime
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

rpc_urls = {'eth': 'https://eth.drpc.org',
            'linea': 'https://1rpc.io/linea',
            'avax': 'https://avax.meowrpc.com'}

eth = Web3(Web3.HTTPProvider(rpc_urls['eth']))
linea = Web3(Web3.HTTPProvider(rpc_urls['linea']))
avax = Web3(Web3.HTTPProvider(rpc_urls['avax']))

#assert eth.is_connected()
#assert linea.is_connected()
#assert avax.is_connected()

while not eth.is_connected() & linea.is_connected():
    eth = Web3(Web3.HTTPProvider(rpc_urls['eth']))
    linea = Web3(Web3.HTTPProvider(rpc_urls['linea']))
    avax = Web3(Web3.HTTPProvider(rpc_urls['avax']))

df = pd.read_csv('gas.csv', index_col=0, parse_dates=[1])
#df.drop_duplicates(subset=['timestamp', 'linea'], inplace=True)
df = df.sort_values('timestamp')

i=0
while True:
    try:
        mainnet_gp = eth.eth.gas_price
        linea_gp = linea.eth.gas_price
        avax_gp = avax.eth.gas_price
    except:
        time.sleep(30)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row = [now] + [round(wei/1e9, 4) for wei in 
                        (mainnet_gp, linea_gp, avax_gp)]
    df = pd.concat((df, pd.DataFrame([row], columns=df.columns))).reindex()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reindex()
    df.to_csv('gas.csv')
    i+=1
    time.sleep(20)