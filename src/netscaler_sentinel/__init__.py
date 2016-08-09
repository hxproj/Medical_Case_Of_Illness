import os

from flask import Flask

__version__ = '0.0.1'
__author__ = 'Craig.C.Li'

app = Flask(__name__)

from netscaler_sentinel import views

app.config.from_object('config.default')
key = 'ENV'
if key not in os.environ:
    os.environ[key] = 'development'

env = os.environ.get(key)
app.config.from_object('config.{0}'.format(env.lower()))
app.config['VERSION'] = __version__
