
from dcharge.utils import parse_datalog, plot_parameter
from psidash.psidash import load_conf
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import os
from dotenv import load_dotenv
from dash.exceptions import PreventUpdate
import logging
import dash_bootstrap_components as dbc
import dash



# logging.basicConfig(filename='dashboard.log', level=logging.DEBUG)

logging.debug('Starting dashboard')


dashboard_dir = os.path.dirname(os.path.abspath(__file__))

# grab environment variables from root directory
load_dotenv(f'{dashboard_dir}/../.env')

# load the dashboard configuration file
conf = load_conf(f'{dashboard_dir}/dashboard.yaml')

default_layout = conf['default_layout']


def get_triggered():
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return button_id


def camel_to_snake(s):
    return ''.join([' '+c.lower() if c.isupper() else c for c in s]).lstrip('_').strip()

def get_frame_opts(df):
    options = []
    for col in df.columns:
        c = col.split('[')[0]
        options.append(dict(label=camel_to_snake(c), value=col))
        
    return options

# def sin_func(t, p=3):
#     return np.sin(np.pi*t/p)

# def test_plot(t_i, t_f, p):
#     t = pd.date_range(t_i, t_f, freq='50ms')
#     t_0 = pd.to_datetime(t_i.date()) # midnight this morning
#     t_ = (t-t_0).total_seconds()
#     v = sin_func(t_,p)
#     trace = go.Scatter(x=t, y=v)
#     return trace

def initialize_plot(url):
    fig = go.Figure([go.Scatter(x=[],y=[])],
        layout=go.Layout(**default_layout))
    return fig

# def update_plot_test(interval, period, data_store):
#     if data_store is None:
#         t_f = pd.Timestamp.now()
#         t_i = t_f - pd.Timedelta(10, unit='s')
#         data_store = dict(t_final=t_f)
#         trace = test_plot(t_i, t_f, period)
#     else:
#         t_i = pd.to_datetime(data_store['t_final'])
#         t_f = pd.Timestamp.now()
#         trace = test_plot(t_i, t_f, period)
#         data_store['t_final'] = t_f
    
#     trace_dict = trace.to_plotly_json()
#     x = trace_dict['x']
#     y = trace_dict['y']

#     return [dict(x=[x], y=[y]), [0]], data_store

datalog_filename = f"{os.environ['DATA_PATH']}/{os.environ['DATA_LOG']}"
print(f'datalog filename: {datalog_filename}')



def update_primary_params(preset):
    return preset.split('_')

def initialize_datalog_figure(param_y, param_x, data_limit):
    """initializes figures 1 and 2"""
    datalog = parse_datalog(datalog_filename, data_limit,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime']).iloc[-data_limit:]
    # print('initial datalog range:', datalog.Time.values[[0,-1]])

    fig = plot_parameter(datalog, param_y, param_x, default_layout)
    parameter_options = get_frame_opts(datalog)
    forbidden_x = ['SalePeriodNumber', 'SalePeriodTimeRemaining[sec]']
    forbidden_y = ['SessionTime', 'Time', 'SalePeriodTimeRemaining[sec]']

    parameter_options_x = [_ for _ in parameter_options if (_['value'] not in forbidden_x)]
    parameter_options_y = [_ for _ in parameter_options if (_['value'] not in forbidden_y)]
    return fig #, parameter_options_y, parameter_options_x


def update_from_file(fname, param1, param2, data_store, data_limit, last=False):
    if data_store is None:
        # load current datalog file
        df = parse_datalog(fname, data_limit,
            set_time_index=False).drop(
            columns=['UnixTime', 'DateTime']).iloc[-data_limit:]
        t_i, t_f = df.Time.values[[0,-1]]
        data_store = dict(t_final=t_f)
    else:
        # load current datalog file (it may have been updated)
        df = parse_datalog(fname, data_limit,
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
        if last:
            result = [dict(x=[x], y=[y]), [0], data_limit], data_store, update_recent_table(df.iloc[[-1]])
        else:
            result = [dict(x=[x], y=[y]), [0], data_limit], data_store
        print('Updating dashboard')
        return result
    else:
        print(f'No need to update: {t_i} <= {t_f}')
        raise PreventUpdate

def update_datalog_figure(interval, param1, param2, data_limit, data_store):
    return update_from_file(datalog_filename, param1, param2, data_store, data_limit, last=True)

def update_secondary_figure(interval, param1, param2, data_limit, data_store):
    return update_from_file(datalog_filename, param1, param2, data_store, data_limit, last=False)


discrete_datalog_filename = f"{os.environ['DATA_PATH']}/{os.environ['DISCRETE_DATA_LOG']}"

# def update_discrete_options(url):
#     df = parse_datalog(discrete_datalog_filename,
#                 set_time_index=False).drop(
#                 columns=['UnixTime', 'DateTime'])
#     return get_frame_opts(df)

def initialize_discrete_figure(param1, param2, data_limit):
    df = parse_datalog(discrete_datalog_filename, data_limit,
                set_time_index=False).drop(
                columns=['UnixTime', 'DateTime']).iloc[-data_limit:]
    parameter_options = get_frame_opts(df)
    return plot_parameter(df, param1, param2, default_layout), parameter_options, parameter_options


def update_discrete_figure(interval, param1, param2, data_limit, data_store):
    return update_from_file(discrete_datalog_filename, param1, param2, data_store, data_limit)

variable_datalog_filename = f"{os.environ['DATA_PATH']}/{os.environ['VARIABLE_DATA_LOG']}"

# def update_variable_options(url):
#     variable = parse_datalog(variable_datalog_filename,
#         set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
#     return get_frame_opts(variable)

def initialize_variable_figure(param1, param2, data_limit):
    variable = parse_datalog(variable_datalog_filename, data_limit,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime']).iloc[-data_limit:]
    parameter_options = get_frame_opts(variable)
    return plot_parameter(variable, param1, param2, default_layout), parameter_options, parameter_options

def update_variable_figure(interval, param1, param2, data_limit, data_store):
    return update_from_file(variable_datalog_filename, param1, param2, data_store, data_limit)


def update_interval(dt):
    # convert from seconds to milliseconds
    return dt*1000


def update_recent_table(df):
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table.children

