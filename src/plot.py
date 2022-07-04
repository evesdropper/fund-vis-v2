import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import api
import utils 

df = pd.read_csv(api.SAVEFILE, names=["Time", "Fund"], header=None)
ymax = df["Fund"].max()
checks = list(api.CHECKPOINTS.keys())

# plotting

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Time"], y=df["Fund"], mode="lines+markers", name="Fund Entries"))

# Checklines
for check in checks:
    checkm = check * 1000000
    if checkm <= ymax:
        fig.add_hline(y=checkm, line_color="green", annotation_text=f"Achieved: {api.CHECKPOINTS[check]}")
    else: 
        fig.add_hline(y=checkm, line_color="red", annotation_text=f"Upcoming: {api.CHECKPOINTS[check]}")

fig.update_xaxes(range=[api.START_DATE, utils.get_day()])
fig.update_yaxes(range=[0, 1.2 * ymax])
fig.update_layout(
    title={"text": "Tanki Fund over Time", 'x':0.5, 'xanchor': 'center'},
    xaxis_title="Time (UTC)",
    yaxis_title="Amount in Tanki Fund",
    legend_title="Legend",
)
fig.show()