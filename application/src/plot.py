import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, html, dcc

from . import api
from . import utils

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server, routes_pathname_prefix="/track")

    # data 
    df = pd.read_csv(api.SAVEFILE, names=["Time", "Fund"], header=None)
    ymax = df["Fund"].max()
    checks = list(api.CHECKPOINTS.keys())

    # plotting
    trace = go.Scatter(x=df["Time"], y=df["Fund"], mode="lines+markers", name="Fund Entries")
    fig = go.Figure([trace])

    # Checklines
    for check in checks:
        checkm = check * 1000000
        if checkm <= ymax:
            fig.add_hline(y=checkm, line_color="green", annotation_text=f"Achieved: {api.CHECKPOINTS[check]}")
        else: 
            fig.add_hline(y=checkm, line_color="red", annotation_text=f"Upcoming: {api.CHECKPOINTS[check]}")

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

    dash_app.layout = html.Div(children=[
        dcc.Graph(
            id='Tonk Fund',
            figure=fig,
            style = {'display': 'inline-block', 'width': '80%'}
        )
    ])
    return dash_app.server