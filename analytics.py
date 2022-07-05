import os, sys
from pathlib import Path
import datetime
import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.dates as mdates

import api
import utils

CWD = os.getcwd()
print(type(CWD))
cwd_path = Path(CWD)
PARENT = str(cwd_path.parent.absolute()) # docs/tonk
NEXT_DIR = os.path.join(PARENT, "tanki-fund")
print(NEXT_DIR)

# data
df = pd.read_csv(api.SAVEFILE, names=["Time", "Fund"], header=None)

print(api.START_DATE, api.START_DATE + datetime.timedelta(days=1))

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
        return np.round(m * mdates.date2num(api.START_DATE + datetime.timedelta(days=35)) + b, -3)

print(predict(x=True))
print(api.scrape)

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