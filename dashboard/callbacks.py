
from dcharge.utils import parse_datalog, plot_parameter
from psidash.psidash import load_conf


conf = load_conf('dashboard.yaml')
default_layout = conf['default_layout']

datalog = parse_datalog('../data_files/DataLog-2022.11.16--18.59.38.641397.txt',
    set_time_index=False).drop(columns=['UnixTime', 'DateTime'])

discrete = parse_datalog('../data_files/DiscreteSmartLoadDataLog-2022.11.16--18.59.44.027119.txt',
    set_time_index=False).drop(columns=['UnixTime', 'DateTime'])

variable = parse_datalog('../data_files/VariableSmartLoadDataLog-2022.11.16--18.59.44.028001.txt',
    set_time_index=False).drop(columns=['UnixTime', 'DateTime'])


def camel_to_snake(s):
    return ''.join([' '+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def get_frame_opts(df):
    options = []
    for col in df.columns:
        c = col.split('[')[0]
        options.append(dict(label=camel_to_snake(c), value=col))
        
    return options


def update_parameter_options(url):
    return get_frame_opts(datalog)


def update_figure(param1, param2):
    return plot_parameter(datalog, param1, param2, default_layout)


def update_discrete_options(url):
    return get_frame_opts(discrete)

def update_discrete_figure(param1, param2):
    return plot_parameter(discrete, param1, param2, default_layout)


def update_variable_options(url):
    return get_frame_opts(variable)

def update_variable_figure(param1, param2):
    return plot_parameter(variable, param1, param2, default_layout)
