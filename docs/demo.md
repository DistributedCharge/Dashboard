```python
%load_ext autoreload
%autoreload 2
```

I've placed the following files in `data_files/` (from root of this repo)

```python
ls ../Plots/InputData
```

```
DataLog-2022.11.16--18.59.38.641397.txt
DiscreteSmartLoadDataLog-2022.11.16--18.59.44.027119.txt
VariableSmartLoadDataLog-2022.11.16--18.59.44.028001.txt
```

```python
from dotenv import load_dotenv
load_dotenv('../.env')
```

```python
import plotly.graph_objs as go
```

```python
import pandas as pd
```

```python
import numpy as np
```

## parsing data log


Available columns in datalog file

* UnixTime
* DateTime
* SessionTime
* SalePeriodTimeRemaining[sec]
* SalePeriodNumber
* Power[W]
* Volts
* Amps
* EnergyDelivered[Wh]
* Rate[sat/Wh]
* MaxAuthorizedRate[sat/Wh]
* EnergyCost
* TotalPaymentAmount[sats]
* TotalNumberOfPayments

```python
# fname = '../data_files/DataLog-2022.11.16--18.59.38.641397.txt'
```

```python
pwd
```

```python
import os
```

```python
from dcharge.utils import parse_datalog
```

```python
from dcharge.dashboard.callbacks import datalog_filename
from dcharge.utils import tail
```

```python
from dcharge.dashboard.callbacks import initialize_datalog_figure, get_frame_opts, default_layout
```

```python

```

```python
from plotly.subplots import make_subplots

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
                    name=param1,
                    mode=mode),
                layout=layout)
    return fig

def initialize_datalog_figure(param_y, param_x, data_limit):
    """initializes figures 1 and 2"""
    datalog = parse_datalog(datalog_filename, data_limit,
        set_time_index=False).drop(columns=['UnixTime', 'DateTime']).iloc[-data_limit:]
    # print('initial datalog range:', datalog.Time.values[[0,-1]])
    if isinstance(param_y, str):
        fig = plot_parameter(datalog, param_y, param_x, default_layout)
        return fig
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for i, _ in enumerate(param_y):
        secondary_y = (i%2 == 0) # see if this trace is even
        fig_ = plot_parameter(datalog, _, param_x, default_layout)
        fig.add_trace(fig_.data[0], secondary_y=secondary_y)
        fig.update_yaxes(title_text=_, secondary_y=secondary_y)

    fig.update_layout(**default_layout)
    return fig

```

```python
fig = initialize_datalog_figure('Power[W]', 'Time', 100)

fig
```

```python
fig = initialize_datalog_figure(['Power[W]', 'Volts'], 'Time', 100)
fig
```

```python
from omegaconf import OmegaConf
```

```python
OmegaConf.
```

```python
import yaml
```

```python
print(yaml.dump(optx))
```

```python
time
session time
sale period time remaining
```

```python
datalog_filename
```

```python
fname = '../data_files/DataLog.txt'
```

```python
data_limit = 10
```

```python
set_time_index=False
```

```python
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

```

```python
df.columns
```

```python
def assign_credit(df):
    return df.assign(Credit=df['TotalPaymentAmount[sats]'] - df['EnergyCost'])
```

```python
df.assign(cost=df)
```

```python
df
```

```python
datalog = parse_datalog(fname, data_limit=10)

datalog
```

## DiscreteSmartLoadDataLog


I'm not sure where the last column gets generated

```python
discrete = parse_datalog(f"../data_files/{os.environ['DISCRETE_DATA_LOG']}", data_limit=100,
    set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
```

```python
discrete
```

```python
discrete.columns
```

```python
discrete['PercentLoad[%]']
```

* UnixTime
* DateTime
* Rate[sat/Wh]
* PercentLoad[%]


## VariableSmartLoadDataLog

```python
variable = parse_datalog(os.environ['VARIABLE_DATA_LOG'])
```

```python
variable.head()
```

## Visualization

```python
import plotly.graph_objs as go
```

```python
def plot_param(ser):
    return go.Scatter(x=ser.index, y=ser)
```

```python
traces = []
traces.append(plot_param(datalog['EnergyCost']))

go.Figure(traces)
```

```python
datalog.columns
```

```python
datalog['SalePeriodTimeRemaining[sec]']
```

## Test data


We'll rewrite the data log line by line so the dashboard can pull new data in real time.

```python
import os
os.environ['DATA_LOG']
```

```python
import os
with open(os.environ['DATA_LOG'], 'r') as f:
    lines = f.readlines()
```

```python
int(len(lines)/2)
```

```python
import time
```

```python
sleep_time = 1 # seconds

with open('../data_files/DataLog.txt', 'w') as f:
    for i, line in enumerate(lines):
        f.write(line)
        f.flush()
        if i > 500:
            print('.', end='')
            time.sleep(sleep_time)
```

```python
from dash import dcc
```

```python
dcc.Graph?
```

```python
import pandas as pd
```

```python
t0 = pd.Timestamp.now()
```

```python
tf = pd.Timestamp.now()
```

```python
t = pd.date_range(t0, tf, freq='100ms')
```

```python
t
```

```python
import plotly.graph_objs as go
```

```python
trace = go.Scatter(x=[1,2,3], y=[4,5,5])
```

```python
trace.x
```

```python
t0 = pd.Timestamp.now()
```

```python
t0_dt = t0.to_datetime64()
```

```python
int(t0_dt)
```

```python

```

```python
trace.to_plotly_json()
```

```python
pd.date_range("2018-01-01", periods=3, freq="H")
```
