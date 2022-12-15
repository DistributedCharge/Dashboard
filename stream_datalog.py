# This utility simulates the dcharge monitor service by writing to the same datalog monitored by the dashboard
import os

from dotenv import load_dotenv
import time

load_dotenv()

data_path = os.environ['DATA_PATH']
read_data_path = os.environ['READ_DATA_PATH']
write_datalog = f"{data_path}/{os.environ['DATA_LOG']}"
read_datalog = f"{read_data_path}/{os.environ['READ_DATA_LOG']}"

# write_discrete_datalog = f"{data_path}/{os.environ['DISCRETE_DATA_LOG']}"
# read_discrete_datalog = f"{read_data_path}/{os.environ['READ_DISCRETE_DATA_LOG']}"

# write_variable_datalog = f"{data_path}/{os.environ['VARIABLE_DATA_LOG']}"
# read_variable_datalog = f"{read_data_path}/{os.environ['READ_VARIABLE_DATA_LOG']}"

with open(read_datalog, 'r') as f:
    datalog_lines = f.readlines()

# with open(read_discrete_datalog, 'r') as f:
#     discrete_datalog_lines = f.readlines()

# with open(read_variable_datalog, 'r') as f:
#     variable_datalog_lines = f.readlines()

# try:
#     assert len(datalog_lines) == len(discrete_datalog_lines)
#     assert len(datalog_lines) == len(variable_datalog_lines)
# except:
#     print([len(_) for _ in (datalog_lines, discrete_datalog_lines, variable_datalog_lines)])
#     raise

sleep_time = 1 # seconds

datalog_header = "UnixTime\tDateTime\tSessionTime\tSalePeriodTimeRemaining[sec]\tSalePeriodNumber\tPower[W]\tVolts\tAmps\tEnergyDelivered[Wh]\tRate[sat/Wh]\tMaxAuthorizedRate[sat/Wh]\tEnergyCost\tTotalPaymentAmount[sats]\tTotalNumberOfPayments\n"

with open(write_datalog, 'w') as f:
    f.write(datalog_header)
    for i, line in enumerate(datalog_lines):
        if i%10 == 0:
            print(f'writting {i}: {line}')
        f.write(line)
        f.flush()
        if i > 100:
            print('.', end='')
            time.sleep(sleep_time)
        print()


