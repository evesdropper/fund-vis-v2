import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, html, dcc

import api
import utils

dash.register_page(__name__)

df = pd.read_csv(api.SAVEFILE, names=["Time", "Fund"], header=None)
# print(df)

# get hourly
hourly = df["Time"].str.extract(rf'(:00)').dropna()
# print(hourly.index)

# draw time series
df_h = df.iloc[hourly.index]
diff_series = df_h["Fund"].diff()
df_h["Diff"] = diff_series
dfh_graph = df_h.dropna().drop(22)


trace = go.Scatter(x=dfh_graph["Time"], y=dfh_graph["Diff"], mode="lines+markers", name="Change in Past Hour")
fig = go.Figure([trace])

fig.update_xaxes(range=[api.START_DATE, utils.get_day()])
fig.update_yaxes(range=[0, dfh_graph["Diff"].max() * 1.2])
fig.update_layout(
    title={"text": "Tanki Fund Hourly Changes", 'x':0.5, 'xanchor': 'center'},
    xaxis_title="Time (UTC)",
    yaxis_title="Change Since Past Hour",
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
