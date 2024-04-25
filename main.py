import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime

### from streamlit_autorefresh import st_autorefresh

from functions import get_n_rows, get_data

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('global.minCachedUpdateInterval', 600)

st.session_state.horizontal = True
st.set_page_config(layout="wide")

data_path="../gas.csv"

ETH_COLOR = '#C9B3F4'
LINEA_COLOR = '#61DFFF'

MIN_MAX_RANGE = (datetime.datetime(2024,5,1), # beginning of the tracking history, replace with your own
                 datetime.datetime.now()+datetime.timedelta(2))
PRE_SELECTED_DATES = (datetime.datetime.now()-datetime.timedelta(8), 
                 datetime.datetime.now()+datetime.timedelta(1))
#observations_per_day = 24*60*60 / 30

now = datetime.datetime.now()

### App start ##
#st.title("Gas")

df_latest = get_data(1)
latest_mainnet_gas = round(df_latest.iloc[-1, 1], 1)
#st.write(f'Latest gas in mainnet')

subcol1, subcol2 = st.columns([0.3, 0.7])
with subcol1:
    st.markdown(
    f"""
    <div style="background-color:#454545;padding:10px;border-radius:10px;">
    <p>Latest gas price in ETH mainnet:</p>
    <h2 style="color:{ETH_COLOR.lower()};">{latest_mainnet_gas} Gwei</h2>
    <p>Last update time: {now.strftime('%d %b, %H:%M:%S')}</p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown('➡️ Press `R` to update (NOT F5!)')
    st.markdown('Reload if you get an error')

with subcol2:
    #st.markdown('---')

### Buttons ###
    st.subheader("Chart time range")
    period = st.radio(
            #"Set the time range",
            "Select option",
            ["Today", "Last week", "Last month", "All (since 21.02.2024)"],
            horizontal=st.session_state.horizontal,
        )

# if period == 'Today':
#     time_range = (datetime.datetime.now().date(),
#                 datetime.datetime.now().date()+datetime.timedelta(1))
    
# elif period == 'Last week':
#     time_range = (datetime.datetime.now()-datetime.timedelta(7),
#                  datetime.datetime.now()+datetime.timedelta(0.5))

# elif period == 'Last month':
#     time_range = (datetime.datetime.now(),
#                  datetime.datetime.now().date()+datetime.timedelta(0.5))

# elif period == "All (since 21.02.2024)":
#     time_range = MIN_MAX_RANGE

n_rows = get_n_rows(period)
df = get_data(n_rows)

fig = make_subplots(rows=2, cols=1, 
                    shared_xaxes=True,
                    subplot_titles=("Mainnet", 
                                    "Linea"),
                    )

# fig.add_layout_image(
#     dict(
#         source="./icons/eth_logo_fullscale.jpg",
#         #xref="paper", yref="paper",
#         #x=1, y=1.05,
#         #sizex=0.2, sizey=0.2,
#         xanchor="right", yanchor="bottom"
#     )
# )


fig.update_xaxes(showgrid=True, row=1, col=1)
fig.update_xaxes(showgrid=True, row=2, col=1)

fig.update_layout(
    height=700, width=1200, 
    showlegend=False,
    xaxis_showticklabels=True, 
    xaxis2_showticklabels=True,
                )

fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['mainnet'],
    mode='lines', name='Mainnet', 
    line=dict(color=ETH_COLOR),
    hovertemplate ='<b>%{x|%d %b %H:%m:%S}</b><br><br>%{y} Gwei<extra></extra>',
    ),
    row=1, col=1)

fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['linea'],
    mode='lines', name='Linea', 
    line=dict(color=LINEA_COLOR),
    hovertemplate ='<b>%{x|%d %b %H:%m:%S}</b><br><br>%{y} Gwei<extra></extra>',
    ),
    row=2, col=1
    )
title = {
        'font_size': 24,
        'x': 0.05,
        'xanchor': 'left',
        'yanchor': 'top'}

fig.update_traces(#title=title, 
                  row=1, col=1)
fig.update_traces(
    #title=title,
    #hovertemplate = f"%{df.timestamp.astype(str)} <br>Gas price: %{df.linea.astype(str)} Gwei",
    row=2, col=1)

fig.update_annotations(
   font_size=24,  # Set title font size
   x=0.05,  # Align title to the left
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

### st_autorefresh(interval=5 * 60 * 1000, key="datarefresh")

