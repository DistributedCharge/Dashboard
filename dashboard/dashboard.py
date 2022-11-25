# #basic script to locally run the dashboard.

import flask
from psidash.psidash import load_conf, load_dash, load_components
from psidash.psidash import get_callbacks, assign_callbacks
from dotenv import load_dotenv

load_dotenv('../.env') # grab environment variables from root directory

import os



conf = load_conf('dashboard.yaml')

server = flask.Flask(__name__) # define flask app.server

conf['app']['server'] = server

app = load_dash(__name__, conf['app'], conf.get('import'))

app.layout = load_components(conf['layout'], conf.get('import'))

application = app.server

if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])

run_server_opts = conf['app.run_server']

if __name__ == '__main__':
    app.run_server(**run_server_opts)

