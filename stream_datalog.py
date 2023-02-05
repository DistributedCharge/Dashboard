# This utility simulates the dcharge monitor service by writing to the same datalog monitored by the dashboard
import os

from dotenv import load_dotenv
import time

load_dotenv()

data_path = os.environ['DATA_PATH']
read_data_path = os.environ['READ_DATA_PATH']
write_datalog = f"{data_path}/{os.environ['DATA_LOG']}"
read_datalog = f"{read_data_path}/{os.environ['READ_DATA_LOG']}"


with open(read_datalog, 'r') as f:
    datalog_lines = f.readlines()

read_discrete_datalog = f"{read_data_path}/{os.environ['READ_DISCRETE_DATA_LOG']}"
write_discrete_datalog = f"{data_path}/{os.environ['DISCRETE_DATA_LOG']}"


with open(read_discrete_datalog, 'r') as f:
    discrete_datalog_lines = f.readlines()


read_variable_datalog = f"{read_data_path}/{os.environ['READ_VARIABLE_DATA_LOG']}"
write_variable_datalog = f"{data_path}/{os.environ['VARIABLE_DATA_LOG']}"

with open(read_variable_datalog, 'r') as f:
    variable_datalog_lines = f.readlines()


sleep_time = int(os.environ.get('SLEEP_TIME', 1)) # seconds

datalog_header = "UnixTime\tDateTime\tSessionTime\tSalePeriodTimeRemaining[sec]\tSalePeriodNumber\tPower[W]\tVolts\tAmps\tEnergyDelivered[Wh]\tRate[sat/Wh]\tMaxAuthorizedRate[sat/Wh]\tEnergyCost\tTotalPaymentAmount[sats]\tTotalNumberOfPayments\n"
discrete_datalog_header = 'UnixTime\tDateTime\tRate[sat/Wh]\tPercentLoad[%]\tUnknown\n'
variable_datalog_header = 'UnixTime\tDateTime\tRate[sat/Wh]\tPercentLoad[%]\tUnknown1\tUnknown2\tUnknown3\n'

with open(write_datalog, 'w') as f, open(write_discrete_datalog, 'w') as g, open(write_variable_datalog, 'w') as h:
    f.write(datalog_header)
    g.write(discrete_datalog_header)
    h.write(variable_datalog_header)

    len_datalog = len(datalog_lines)
    len_discrete = len(discrete_datalog_lines)
    len_variable = len(variable_datalog_lines)
    max_lines = max([len_datalog, len_discrete, len_variable])

    for i in range(max_lines):
        if i < len_datalog:
            datalog_line = datalog_lines[i]
            f.write(datalog_line)
            f.flush()
        if i < len_discrete:
            discrete_line = discrete_datalog_lines[i]
            g.write(discrete_line)
            g.flush()
        if i < len_variable:
            variable_line = variable_datalog_lines[i]
            h.write(variable_line)
            h.flush()
        if i%10 == 0:
            print(f'wrote {i}:\n{datalog_line}\n{discrete_line}\n{variable_line}')
        if i > 100:
            print('.', end='')
            time.sleep(sleep_time)
        print()


