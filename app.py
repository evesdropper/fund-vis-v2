import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, html, dcc

from fund import api, utils

app = Dash(__name__, use_pages=True)
app.title = 'Tanki Fund Tracker' 
server = app.server

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

app.layout = html.Div([
	html.H1('Tanki Fund Tracker'),
    html.H2('2022 - Summer Major'),
    html.P(f'Site Status: {api.scrape(checkstatus=True)}'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
	dash.page_container,
    html.Center("Made by Person_Random."),
])

if __name__ == '__main__':
    app.run_server(debug=True)