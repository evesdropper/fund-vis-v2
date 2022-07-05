import os, sys
from pathlib import Path
import datetime
import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.dates as mdates
import dash
from dash import Dash, html, dcc

import api as api
import utils

dash.register_page(__name__)

CWD = os.getcwd()
# print(type(CWD))
cwd_path = Path(CWD)
PARENT = str(cwd_path.parent.absolute()) # docs/tonk
NEXT_DIR = os.path.join(PARENT, "tanki-fund")
# print(NEXT_DIR)

# data
df = pd.read_csv(api.SAVEFILE, names=["Time", "Fund"], header=None)
hourly = df["Time"].str.extract(rf'(:00)').dropna()
cur_time, cur_fund = api.scrape()

# diffing
df_h = df.iloc[hourly.index]
diff_series = df_h["Fund"].diff(periods=24)
df_h["Diff"] = diff_series
dfh_upd = df_h.dropna()

# Daily Updates
def get_daily(last=False):
    daily = {}
    start, day = api.START_DATE, 1
    while start < min(api.START_DATE + datetime.timedelta(days=35), datetime.datetime.strptime(df.iloc[-1, 0], "%Y-%m-%d %H:%M")):
        start = start + datetime.timedelta(days=1)
        start_str = start.strftime("%Y-%m-%d") 
        cur_day = df["Time"].str.extract(rf'({start_str} 01:[45]\d|{start_str} 02:[01]\d)').dropna()
        if cur_day.empty:
            break
        cur_day_t = pd.to_datetime(cur_day[0], format="%Y-%m-%d %H:%M")
        ref_time = api.START_DATE + datetime.timedelta(days=day)
        minidx = abs(ref_time - cur_day_t).idxmin()
        daily[day] = df.loc[minidx, "Fund"] - daily.get(day-1, 0)
    if last:
        return daily[day]
    return daily

def regression(log=None):
    """
    Regression
    """
    x, y = mdates.datestr2num(df["Time"].to_numpy()), df["Fund"].to_numpy()
    r = np.corrcoef(x, y)[0, 1]
    m = r * (np.std(y) / np.std(x))
    b = np.mean(y) - m * np.mean(x)
    return m, b

def predict(x=False, y=False):
    m, b = regression()
    if x:
        return np.round(m * mdates.date2num(api.START_DATE + datetime.timedelta(days=35)) + b, -3) / 10 ** 6


# format
def generate_overview():
    """
    Function to generate overview analytics.
    """
    return ""


"""
<p className={styles.description}>Last Updated: {api.scrape}</p>
<div className={styles.grid}>
    <div className={styles.card}>
        <h2>X</h2>
        <p>Total Amount in Tanki Fund (Stage Y)</p>
    </div>
    <div className={styles.card}>
        <h2>X</h2>
        <p>Increase in the past 24 hours (Up/down Z percent)</p>
    </div>
    <div className={styles.card}>
        <h2>X</h2>
        <p>Projected Amount Tanki Fund (Will reach Y reward)</p>
    </div>
</div>
"""

# Dash Layout (Results)
layout = html.Div(children=[
    dcc.Markdown(f'''

    ## Analytics

    As of right now, analytics are under development. Stay tuned for the coming features!
    * At-a-glance analytics (e.g. final fund value, next checkpoint).
    * Prediction models and explanations.
    * Chart for daily changes.

    And much more (if time allows). All of this is made to help you make a more informed decision on whether or not to buy in the Tanki Fund. Thanks for sticking around!

    ## At a Glance
    Last Updated: {cur_time.strftime("%Y-%m-%d %H:%M")}

    ### Current Fund
    {int(cur_fund.replace(",", "")) / 10 ** 6}M Tankoins

    ### Increase in past 24H*
    {int(dfh_upd.iloc[-1, 2]) / 10 ** 3}K Tankoins

    ### Final Fund Prediction**
    {predict(x=True)}M Tankoins

    #### Notes:
    * Increase in past 24H is calculated using the hourly plots. Daily increase table coming soon.
    * Final predictions may not be accurate as the fund has just started.
    ''')


])