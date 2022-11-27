
from dcharge.utils import parse_datalog, plot_parameter
from psidash.psidash import load_conf
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import os
from dotenv import load_dotenv
from dash.exceptions import PreventUpdate

load_dotenv('../.env')

conf = load_conf('dashboard.yaml')
default_layout = conf['default_layout']

discrete = parse_datalog(os.environ['DISCRETE_DATA_LOG'],
    set_time_index=False).drop(columns=['UnixTime', 'DateTime'])

variable = parse_datalog(os.environ['VARIABLE_DATA_LOG'],
    set_time_index=False).drop(columns=['UnixTime', 'DateTime'])


def camel_to_snake(s):
    return ''.join([' '+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def get_frame_opts(df):
    options = []
    for col in df.columns:
        c = col.split('[')[0]
        options.append(dict(label=camel_to_snake(c), value=col))
        
    return options

t0 = pd.Timestamp.now()

def sin_func(t, p=10):
    return np.sin(np.pi*t/p)

def initialize_plot_test(url):
    t_ = np.linspace(0, 100, 100)
    t = [t0 - pd.Timedelta(_, unit='s') for _ in t_]
    v = sin_func(t_)
    
    return go.Figure(
        [go.Scatter(x=t, y=v)],
        layout=go.Layout(**default_layout))

def update_plot_test(interval):
    t = pd.Timestamp.now()
    dt = (t-t0).total_seconds()
    v = sin_func(dt)
    print(t,v)
    return [dict(x=[[t]], y=[[v]]), [0]]


def update_parameter_options(url):
    """sets parameters for figures 1 and 2"""
    datalog = parse_datalog(os.environ['DATA_LOG'],
        set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
    return get_frame_opts(datalog)


def initialize_datalog_figure(param1, param2):
    """initializes figures 1 and 2"""
    datalog = parse_datalog(os.environ['DATA_LOG'],
        set_time_index=False).drop(columns=['UnixTime', 'DateTime'])

    fig = plot_parameter(datalog, param1, param2, default_layout)
    return fig, dict(range=datalog['Time'].values[[0,-1]])


def update_datalog_figure(interval, param1, param2, range_data):
    """we need to know the current state of the plot before we can update it"""
    datalog = parse_datalog(os.environ['DATA_LOG']).drop(
        columns=['UnixTime', 'DateTime'])


    data_store = dict(
        datalog=datalog['Time'].values[[0,-1]],
        discrete=discrete['Time'].values[[0,-1]],
        variable=variable['Time'].values[[0,-1]]
        )
    
    raise PreventUpdate, dict(range=datalog.index[[0,-1]])
    # return [dict(x=[[t]], y=[[v]]), [0]], data_store

    # print(range_data, interval, param1, param2)
    

    # datalog_current = parse_datalog(os.environ['DATA_LOG'],
    #     set_time_index=False).drop(columns=['UnixTime', 'DateTime'])

    # raise PreventUpdate
    # # return [dict(x=[[t]], y=[[v]]), [0]]


def update_discrete_options(url):
    return get_frame_opts(discrete)

def update_discrete_figure(param1, param2):
    return plot_parameter(discrete, param1, param2, default_layout)


def update_variable_options(url):
    return get_frame_opts(variable)

def update_variable_figure(param1, param2):
    return plot_parameter(variable, param1, param2, default_layout)
