
from dcharge.utils import parse_datalog, plot_parameter
from psidash.psidash import load_conf
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import os
from dotenv import load_dotenv
from dash.exceptions import PreventUpdate

dashboard_dir = os.path.dirname(os.path.abspath(__file__))

# grab environment variables from root directory
load_dotenv(f'{dashboard_dir}/../.env')

# load the dashboard configuration file
conf = load_conf(f'{dashboard_dir}/dashboard.yaml')

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
    print('initial datalog range:', datalog.Time.values[[0,-1]])

    fig = plot_parameter(datalog, param1, param2, default_layout)
    return fig # dict(range=datalog['Time'].values[[0,-1]])


def update_datalog_figure(interval, param1, param2, range_data, fig_state):
    """we need to know the current state of the plot before we can update it"""
    # raise PreventUpdate
    datalog = parse_datalog(os.environ['DATA_LOG'],
        set_time_index=False).drop(
        columns=['UnixTime', 'DateTime'])

    if fig_state is not None:
        fig_data = fig_state['data']
        if fig_data is not None:
            fig_x = fig_data[0]['x']
            fig_y = fig_data[0]['y']
            print('fig x:', type(fig_x[0]), fig_x[::50])
            print('fig y:', type(fig_y[0]), fig_y[::50])


    if range_data is not None:
        range_ = pd.to_datetime(range_data['range'])
    
        last_time_prev = range_[-1]
        last_time = datalog.Time.values[-1]

        if last_time > last_time_prev:
            print('update!!', last_time, last_time_prev)

            # gather new data starting at the end of the previous time series
            datalog.set_index('Time', inplace=True)
            subset = datalog.loc[last_time_prev:]
            print(subset.index.dtype)

            # return time to a column in case that's what we want to plot
            subset.reset_index(inplace=True) 
            p1 = subset[param1].values[-1]
            p2 = subset[param2].values[-1]
            print(f'{param1}: {p1}, {param2}: {p2}')

            return [dict(x=[[p2]], y=[[p1]]), [0], 10000000], dict(range=datalog.index[[0,-1]])
        else:
            print('no need to update')
            raise PreventUpdate

    raise PreventUpdate

    # return [dict(), [0]], dict(range=datalog.Time.values[[0,-1]])




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
