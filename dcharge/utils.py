import pandas as pd
import numpy as np
import plotly.graph_objs as go

def parse_datalog(fname, set_time_index=True):
    lines = []
    with open(fname) as f:
        for i, line in enumerate(f):
            current = line.strip().split('\t')
            if i == 0:
                columns = current
                ncols = len(current)
            else:
                if len(current) != ncols:
                    print(f'problem at line {i}')
                    raise IOError(f'line of length {len(current)} does not match {ncols} cols:{columns} {current}')
                lines.append(current)

    df = pd.DataFrame(lines, columns=columns)
    df = df.replace(',', '', regex=True)

    for c in columns:
        try:
            df[c] = pd.to_numeric(df[c])
            df[c].replace({-1.0: np.NaN}, inplace=True)
        except:
            pass

    df['Time'] = pd.to_datetime(df.UnixTime, unit='s')
    if set_time_index:
        df.set_index('Time', inplace=True)
    return df

def plot_parameter(df, param1, param2, layout_params):
    """plots param1 vs param2"""
    if param2 == 'Time':
        mode = 'lines'
    else:
        mode = 'markers'
    df.sort_values(param2, inplace=True)
    layout = go.Layout(
        xaxis=dict(title=param2),
        yaxis=dict(title=param1),
        **layout_params)

    fig = go.Figure(go.Scatter(
                    x=df[param2],
                    y=df[param1],
                    mode=mode),
                layout=layout)
    return fig
