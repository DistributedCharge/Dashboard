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
from dcharge.utils import parse_datalog
```

```python
datalog = parse_datalog(fname)

datalog
```

## DiscreteSmartLoadDataLog


I'm not sure where the last column gets generated

```python
discrete = parse_datalog('../data_files/DiscreteSmartLoadDataLog-2022.11.16--18.59.44.027119.txt',
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
variable = parse_datalog('../data_files/VariableSmartLoadDataLog-2022.11.16--18.59.44.028001.txt')
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

```python

```

```python

```
