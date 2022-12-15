
from dcharge.utils import parse_datalog, plot_parameter
from psidash.psidash import load_conf
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import os
from dotenv import load_dotenv
from dash.exceptions import PreventUpdate
import logging
# logging.basicConfig(filename='dashboard.log', level=logging.DEBUG)

logging.debug('Starting dashboard')


dashboard_dir = os.path.dirname(os.path.abspath(__file__))

# grab environment variables from root directory
load_dotenv(f'{dashboard_dir}/../.env')

# load the dashboard configuration file
conf = load_conf(f'{dashboard_dir}/dashboard.yaml')

default_layout = conf['default_layout']


def camel_to_snake(s):
    return ''.join([' '+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def get_frame_opts(df):
    options = []
    for col in df.columns:
        c = col.split('[')[0]
        options.append(dict(label=camel_to_snake(c), value=col))
        
    return options

def sin_func(t, p=3):
    return np.sin(np.pi*t/p)

def test_plot(t_i, t_f, p):
    t = pd.date_range(t_i, t_f, freq='50ms')
    t_0 = pd.to_datetime(t_i.date()) # midnight this morning
    t_ = (t-t_0).total_seconds()
    v = sin_func(t_,p)
    trace = go.Scatter(x=t, y=v)
    return trace

def initialize_plot(url):
    fig = go.Figure([go.Scatter(x=[],y=[])],
        layout=go.Layout(**default_layout))
    return fig

def update_plot_test(interval, period, data_store):
    if data_store is None:
        t_f = pd.Timestamp.now()
        t_i = t_f - pd.Timedelta(10, unit='s')
        data_store = dict(t_final=t_f)
        trace = test_plot(t_i, t_f, period)
    else:
        t_i = pd.to_datetime(data_store['t_final'])
        t_f = pd.Timestamp.now()
        trace = test_plot(t_i, t_f, period)
        data_store['t_final'] = t_f
    
    trace_dict = trace.to_plotly_json()
    x = trace_dict['x']
    y = trace_dict['y']

    return [dict(x=[x], y=[y]), [0]], data_store

datalog_filename = f"{os.environ['DATA_PATH']}/{os.environ['DATA_LOG']}"

def update_parameter_options(url):
    """sets parameters for figures 1 and 2"""
    
    datalog = parse_datalog(datalog_filename,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
    return get_frame_opts(datalog)


def initialize_datalog_figure(param1, param2):
    """initializes figures 1 and 2"""
    datalog = parse_datalog(datalog_filename,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
    # print('initial datalog range:', datalog.Time.values[[0,-1]])

    fig = plot_parameter(datalog, param1, param2, default_layout)
    return fig # dict(range=datalog['Time'].values[[0,-1]])


def update_from_file(fname, param1, param2, data_store):
    if data_store is None:
        # load current datalog file
        df = parse_datalog(fname,
            set_time_index=False).drop(
            columns=['UnixTime', 'DateTime'])
        t_i, t_f = df.Time.values[[0,-1]]
        data_store = dict(t_final=t_f)
    else:
        # load current datalog file (it may have been updated)
        df = parse_datalog(fname,
            set_time_index=False).drop(
            columns=['UnixTime', 'DateTime'])
        t_i = pd.to_datetime(data_store['t_final'])
        t_f = df.Time.values[-1]
        data_store = dict(t_final=t_f)

    if t_f > t_i:
        # gather new data starting at the end of the previous time series
        df.set_index('Time', inplace=True)
        subset = df.loc[t_i:t_f].reset_index()
        fig = plot_parameter(subset, param1, param2, default_layout)
        trace = fig.data[0].to_plotly_json()
        x = trace['x']
        y = trace['y']
        result = [dict(x=[x], y=[y]), [0]], data_store
        logging.debug('Updating dashboard')
        return result
    else:
        logging.debug('No need to update')
        raise PreventUpdate

def update_datalog_figure(interval, param1, param2, data_store):
    return update_from_file(datalog_filename, param1, param2, data_store)

discrete_datalog_filename = f"{os.environ['DATA_PATH']}/{os.environ['DISCRETE_DATA_LOG']}"

def update_discrete_options(url):
    df = parse_datalog(discrete_datalog_filename,
                set_time_index=False).drop(
                columns=['UnixTime', 'DateTime'])
    return get_frame_opts(df)

def initialize_discrete_figure(param1, param2):
    df = parse_datalog(discrete_datalog_filename,
                set_time_index=False).drop(
                columns=['UnixTime', 'DateTime'])
    return plot_parameter(df, param1, param2, default_layout)


def update_discrete_figure(interval, param1, param2, data_store):
    return update_from_file(discrete_datalog_filename, param1, param2, data_store)

variable_datalog_filename = f"{os.environ['DATA_PATH']}/{os.environ['VARIABLE_DATA_LOG']}"

def update_variable_options(url):
    variable = parse_datalog(variable_datalog_filename,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
    return get_frame_opts(variable)

def initialize_variable_figure(param1, param2):
    variable = parse_datalog(variable_datalog_filename,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
    return plot_parameter(variable, param1, param2, default_layout)

def update_variable_figure(interval, param1, param2, data_store):
    return update_from_file(variable_datalog_filename, param1, param2, data_store)

