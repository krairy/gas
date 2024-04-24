# Live gas tracker
A system that records the gas price (in Gwei) on the mainnet and has the Streamlit frontend. 

## How to use
This is built on `web3.py` library and the single function that does the magic is `w3.get_gas_price()`,
Note that this workes for Ethereum Mainnet and for some L2 and some other L1s (Avalanche, BSC) - but doesn't work for chains like Scroll, Base and Optimism. Hit me up if you have ideas
### Set up

1. Install Python
2. `pip -m venv .venv`
3. Activate the virtual environment
   On Linux/MacOs: 
  - `source .venv/bin/activate`
  On Windows:
  - `.venv/Scripts/Activate.ps1`
4. Install requirements:
`pip install -r requirements.txt`

And you are set!

Start the gas fetcher:
`python gas_fetcher.py`

Start the visualization app:
`streamlit run main.py`

### Adding other networks and configuration

Coming thooon...
   

## How to use the data
✔️Optimize your transaction costs

✔️Hunt Sybils!
