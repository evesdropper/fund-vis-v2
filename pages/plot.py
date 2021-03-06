import os, sys
import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, html, dcc

sys.path.append('../')
from fund import api, utils

path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

dash.register_page(__name__, path='/')

# data 
df = pd.read_csv(api.SAVEFILE, names=["Time", "Fund"], header=None)

unique_funds = df.sort_values("Time").drop_duplicates(subset=["Fund"])
ymax = df["Fund"].max()
checks = list(api.CHECKPOINTS.keys())


# plotting
trace = go.Scatter(x=unique_funds["Time"], y=unique_funds["Fund"], mode="lines+markers", name="Fund Entries")
fig = go.Figure([trace])

# Checklines
for check in checks:
    checkm = check * 1000000
    if checkm <= ymax:
        fig.add_hline(y=checkm, line_color="green", annotation_text=f"Achieved: {api.CHECKPOINTS[check]}")
    else: 
        fig.add_hline(y=checkm, line_color="red", annotation_text=f"Upcoming: {api.CHECKPOINTS[check]}")

# Notes
fig.add_vrect(x0="2022-07-04 02:00", x1="2022-07-04 17:33", fillcolor="red", annotation_text="Sourced from Observations", opacity=0.2, line_width=0)

# general
fig.update_xaxes(range=[api.START_DATE, utils.get_day()])
fig.update_yaxes(range=[0, 1.2 * ymax])
fig.update_layout(
    title={"text": "Tanki Fund over Time", 'x':0.5, 'xanchor': 'center'},
    xaxis_title="Time (UTC)",
    yaxis_title="Amount in Tanki Fund",
    legend_title="Legend",
    showlegend = True,
)
# fig.show()

layout = html.Div(children=[

    html.Center(children=[
    dcc.Graph(
        id='Tonk Fund',
        figure=fig,
        style = {'display': 'inline-block', 'width': '1080px', 'height': '540px', 'padding': 'auto'}
    )
    ]),

])
