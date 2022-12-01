import os

from dotenv import load_dotenv
import time

load_dotenv()

fname = os.environ['DATA_LOG']

with open('/Users/asherp/git/schroder/dc-dashboard/data_files/DataLog-2022.11.16--18.59.38.641397.txt', 'r') as f:
    lines = f.readlines()

sleep_time = 1 # seconds

with open(fname, 'w') as f:
    for i, line in enumerate(lines):
        if i%10 == 0:
            print(f'writting {i}: {line}')
        f.write(line)
        f.flush()
        if i > 500:
            print('.', end='')
            time.sleep(sleep_time)


