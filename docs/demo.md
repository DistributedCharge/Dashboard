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
fname = '../Plots/InputData/DataLog.txt'
```

```python
import os
```

```python
from dcharge.utils import parse_datalog
```

```python
import mmap
import os


# def tail(f, window=20):
#     """Returns the last `window` lines of file `f` as a list.
#     """
#     if window == 0:
#         return []

#     BUFSIZ = 1024
#     f.seek(0, 2)
#     remaining_bytes = f.tell()
#     size = window + 1
#     block = -1
#     data = []

#     while size > 0 and remaining_bytes > 0:
#         if remaining_bytes - BUFSIZ > 0:
#             # Seek back one whole BUFSIZ
#             f.seek(block * BUFSIZ, 2)
#             # read BUFFER
#             bunch = f.read(BUFSIZ)
#         else:
#             # file too small, start from beginning
#             f.seek(0, 0)
#             # only read what was not read
#             bunch = f.read(remaining_bytes)

#         bunch = bunch.decode('utf-8')
#         data.insert(0, bunch)
#         size -= bunch.count('\n')
#         remaining_bytes -= BUFSIZ
#         block -= 1

#     return ''.join(data).splitlines()[-window:]

# def parse_datalog(fname, data_limit, set_time_index=False):

#     lines = []
#     with open(fname, 'rb') as f:
#         line = f.readline().decode("utf-8")
#         columns = line.strip().split('\t')
#         ncols = len(columns)
#         lines = tail(f, data_limit)
        
#     lines = [line.strip().split('\t') for line in lines]

#     df = pd.DataFrame(lines, columns=columns)
#     df = df.replace(',', '', regex=True)

#     for c in columns:
#         try:
#             df[c] = pd.to_numeric(df[c])
#             df[c].replace({-1.0: np.NaN}, inplace=True)
#         except:
#             pass

#     df['Time'] = pd.to_datetime(df.UnixTime, unit='s')
#     if set_time_index:
#         df.set_index('Time', inplace=True)
#     return df

datalog = parse_datalog(fname, data_limit=500)

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
