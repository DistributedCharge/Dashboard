```python
%load_ext autoreload
%autoreload 2
```

I've placed the following files in `data_files/` (from root of this repo)

```python
ls ../data_files
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

```python
import pandas as pd
```

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
fname = '../data_files/DataLog-2022.11.16--18.59.38.641397.txt'
```

```python
import os
```

```python
from dcharge.utils import parse_datalog
```

```python
datalog = parse_datalog(os.environ['DATA_LOG'])

datalog
```

## DiscreteSmartLoadDataLog


I'm not sure where the last column gets generated

```python
discrete = parse_datalog(os.environ['DISCRETE_DATA_LOG'],
    set_time_index=False).drop(columns=['UnixTime', 'DateTime'])
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
sleep_time = 1

with open('../data_files/DataLog.txt', 'w') as f:
    for i, line in enumerate(lines):
        f.write(line)
        f.flush()
        if i > 500:
            print('.', end='')
            time.sleep(sleep_time)
```

```python

```
