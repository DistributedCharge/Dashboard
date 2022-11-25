import pandas as pd

def parse_datalog(fname):
    lines = []
    with open(fname) as f:
        for i, line in enumerate(f):
            current = line.strip().split('\t')
            if i == 0:
                last = len(current)
                columns = current
                print('\t'.join(columns))
            else:
                if last != len(current):
                    last = len(current)
                    print(f'problem at line {i}')
                lines.append(current)
    df = pd.DataFrame(lines, columns=columns)
    df = df.replace(',','', regex=True)
    df['time'] = pd.to_datetime(df.UnixTime, unit='s')
    df.set_index('time', inplace=True)
    return df