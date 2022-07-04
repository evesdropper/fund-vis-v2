# necessary imports
import os, sys
import pandas as pd
import numpy as np
import plotly.express as px

# random stuff
CWD = os.getcwd()
DATA = os.path.join(CWD, "fund.csv")

# get data
df = pd.read_csv(DATA)

# data cleaning
date_series = df["Elapsed Time"]

# figure 
fig = px.scatter(df, x="Elapsed Time", y="Fund")
fig.show()
