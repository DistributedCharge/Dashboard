
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
from dcharge.utils import get_module_logger

from plotly.subplots import make_subplots



# logging.basicConfig(filename='dashboard.log', level=logging.DEBUG)


logger = get_module_logger(__name__)
logger.info("Starting Dashboard")


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


def initialize_plot(url):
    fig = go.Figure([go.Scatter(x=[],y=[])],
        layout=go.Layout(**default_layout))
    return fig


datalog_filename = f"{os.environ['DATA_PATH']}/{os.environ['DATA_LOG']}"
logger.info(f'datalog filename: {datalog_filename}')



def update_primary_params(preset):
    return preset.split('_')


def initialize_datalog_figure(param_y, param_x, data_limit):
    """initializes figures 1 and 2"""
    datalog = parse_datalog(datalog_filename, data_limit,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime']).iloc[-data_limit:]
    datalog.sort_values('Time', inplace=True)
    # logger.info('initial datalog range:', datalog.Time.values[[0,-1]])
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if isinstance(param_y, str):
        fig_ = plot_parameter(datalog, param_y, param_x, default_layout)
        fig.add_trace(fig_.data[0])
        fig.update_yaxes(title_text=param_y)
        fig.update_xaxes(title_text=param_x)
    
    # multiple variables selected
    else:
        if len(param_y) > 2:
            raise PreventUpdate
        for i, _ in enumerate(param_y):
            secondary_y = (i%2 == 0) # see if this trace is even
            fig_ = plot_parameter(datalog, _, param_x, default_layout)
            fig.add_trace(fig_.data[0], secondary_y=secondary_y)
            fig.update_yaxes(title_text=_, secondary_y=secondary_y)
            fig.update_xaxes(title_text=param_x)

    fig.update_layout(**default_layout)
    return fig


def update_from_file(fname, param1, param2, data_store, data_limit, render_last=False):
    """data_store will keep the last time interval sent to the graph

    Make sure the total number of points in the graph is <= data_limit 
    """
    if data_store is None:
        # load current datalog file
        df = parse_datalog(fname, data_limit,
            set_time_index=False).drop(
            columns=['UnixTime', 'DateTime']).iloc[-data_limit:]
        t_i, t_f = df.Time.values[[0,-1]] # extract start and end times from file
        data_store = dict(t_init=t_i, t_final=t_f)
    else:
        # load current datalog file (it may have been updated)
        df = parse_datalog(fname, data_limit,
            set_time_index=False).drop(
            columns=['UnixTime', 'DateTime'])
        t_i = pd.to_datetime(data_store['t_final']) # start at the end of previous data
        t_f = df.Time.values[-1]
        data_store = dict(t_init=t_i, t_final=t_f)

    if t_f > t_i:
        # gather new data starting at the end of the previous time series
        df.set_index('Time', inplace=True)
        df.sort_index(inplace=True)
        subset = df.loc[df.index > t_i].reset_index()
        # subset = df.loc[t_i:t_f].reset_index()
        if isinstance(param1, str):
            fig = plot_parameter(subset, param1, param2, default_layout)
            trace = fig.data[0].to_plotly_json()
            x = trace['x']
            y = trace['y']
            if render_last:
                result = [dict(x=[x], y=[y]), [0], data_limit], data_store, update_recent_table(df.iloc[[-1]])
            else:
                result = [dict(x=[x], y=[y]), [0], data_limit], data_store
            logger.info(f'##### Updating dashboard with {len(x), len(y)} points##### ')
            return result
        else:
            if len(param1) > 2:
                logger.info(f"can't update more than 2 at a time yet {param1}")
                raise PreventUpdate
            else:
                logger.info(f'updating parameters {param1}')
            x_vals = []
            y_vals = []
            trace_indices = []
            for i, _ in enumerate(param1):
                fig = plot_parameter(subset, _, param2, default_layout)
                trace = fig.data[0].to_plotly_json()
                x = trace['x']
                y = trace['y']

                # if i == 0:
                logger.info(f'appending (index, xpnts, ypnts) {i, len(x), len(y)}')
                x_vals.append(x)
                y_vals.append(y)
                trace_indices.append(i)
                # if i == 1:
                #     logger.info(f'cannot append {i, len(x), len(y)}')

            assert np.array(x_vals).shape == np.array(y_vals).shape

            logger.info(f'xvals, yvals shape, trace indices {np.array(x_vals).shape, np.array(y_vals).shape, trace_indices}')
            if render_last:
                result = ([dict(x=x_vals, y=y_vals), trace_indices, len(param1)*[data_limit]], data_store, update_recent_table(df.iloc[[-1]]))
            else:
                result = ([dict(x=x_vals, y=y_vals), trace_indices, len(param1)*[data_limit]], data_store)
            logger.info('Updating dashboard with multiple traces')
            return result

    else:
        logger.info(f'No need to update {param1}: {t_i} <= {t_f}')
        raise PreventUpdate

def initialize_tertiary_figure(preset, data_limit):
    param_1, param_2, param_3 = preset.split('_')
    logger.info('initalizing tertiary figure')
    fig = initialize_datalog_figure([param_1, param_2], param_3, data_limit)
    return fig

def update_datalog_figure(interval, param1, param2, data_limit, data_store):
    return update_from_file(datalog_filename, param1, param2, data_store, data_limit, render_last=True)

def update_secondary_figure(interval, param1, param2, data_limit, data_store):
    return update_from_file(datalog_filename, param1, param2, data_store, data_limit, render_last=False)

def update_tertiary_figure(interval, preset, data_limit, data_store):
    logger.info('updating tertiary')
    # raise PreventUpdate
    param_1, param_2, param_3 = preset.split('_')
    return update_from_file(datalog_filename, [param_1, param_2], param_3, data_store, data_limit, render_last=False)




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
    """
    Row 1: Power, Volts, Amps
    Row 2: Session time, Energy Delivered,
    Row 3: Total number of payments, Total Payment Amount, Energy Cost, Credit
    Row 4: Sale Period Number, Sale Period Time Remaining, Rate, Max Authorized Rate
    """
    row_1 = df[['Power[W]', 'Volts', 'Amps']]
    row_2 = df[['SessionTime', 'EnergyDelivered[Wh]']]
    row_3 = df[['TotalNumberOfPayments', 'TotalPaymentAmount[sats]', 'EnergyCost', 'Credit[sats]']]
    row_4 = df[['SalePeriodNumber', 'SalePeriodTimeRemaining[sec]', 'Rate[sat/kWh]', 'MaxAuthorizedRate[sat/kWh]']]

    tables = []
    for row in [row_1, row_2, row_3, row_4]:
        tables.append(dbc.Table.from_dataframe(row, striped=True, bordered=True, hover=True))
    return tables

