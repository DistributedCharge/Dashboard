
from dcharge.utils import parse_datalog
import plotly.graph_objs as go
from psidash.psidash import load_conf

fname = '../data_files/DataLog-2022.11.16--18.59.38.641397.txt'

conf = load_conf('dashboard.yaml')


datalog = parse_datalog(fname).drop(columns=['UnixTime', 'DateTime'])


def camel_to_snake(s):
    return ''.join([' '+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def update_parameter_options(url):
    options = []
    for col in datalog.columns:
        c = col.split('[')[0]
        options.append(dict(label=camel_to_snake(c), value=col))
        
    return options, options[-1]['value']

def update_primary_figure(parameter):
    ser = datalog[parameter]

    layout = go.Layout(yaxis=dict(title=parameter), **conf['default_layout'])

    return go.Figure(go.Scatter(x=ser.index, y=ser), layout=layout)

