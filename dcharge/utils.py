import pandas as pd
import numpy as np
import plotly.graph_objs as go


import mmap
import os

import mmap
import os


def tail(f, window=20):
    """Returns the last `window` lines of file `f` as a list.
    """
    if window == 0:
        return []

    BUFSIZ = 1024
    f.seek(0, 2)
    remaining_bytes = f.tell()
    size = window + 1
    block = -1
    data = []

    while size > 0 and remaining_bytes > 0:
        if remaining_bytes - BUFSIZ > 0:
            # Seek back one whole BUFSIZ
            f.seek(block * BUFSIZ, 2)
            # read BUFFER
            bunch = f.read(BUFSIZ)
        else:
            # file too small, start from beginning
            f.seek(0, 0)
            # only read what was not read
            bunch = f.read(remaining_bytes)

        bunch = bunch.decode('utf-8')
        data.insert(0, bunch)
        size -= bunch.count('\n')
        remaining_bytes -= BUFSIZ
        block -= 1

    return ''.join(data).splitlines()[-window:]

def assign_credit(df):
    return df.assign(**{'Credit[sats]': df['TotalPaymentAmount[sats]'] - df['EnergyCost']})

def convert_to_sats_per_kWh(df):
    """unit conversion for power
    also converts results to int
    """
    for _ in df.columns:
        old_unit = '[sat/Wh]'
        new_unit = '[sat/kWh]'
        varname = _.split(old_unit)[0]
        if old_unit in _:
            df[_] = (1000*df[_]).astype(int)
            df.rename(columns={_: f'{varname}{new_unit}'}, inplace=True)
    return df

def parse_datalog(fname, data_limit, set_time_index=False):

    lines = []
    with open(fname, 'rb') as f:
        line = f.readline().decode("utf-8")
        columns = line.strip().split('\t')
        ncols = len(columns)
        lines = tail(f, data_limit)
        
    lines = [line.strip().split('\t') for line in lines]

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

    df = assign_credit(df)

    df = convert_to_sats_per_kWh(df)

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
