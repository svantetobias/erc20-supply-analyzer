import argparse
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("csv_file", help="The CSV file generated with erc20-build-supply-data.py")
args = parser.parse_args()

df = pd.read_csv(args.csv_file)

trace_high = go.Scatter(
    x=df.timestamp,
    y=df['supply'],
    name = "Supply",
    line = dict(color = '#17BECF'),
    opacity = 0.8)

data = [trace_high]

layout = dict(
    title=f"Supply Over Time ({args.csv_file})",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
py.plot(fig, filename = f"supply-over-time-graph-{args.csv_file}.html")