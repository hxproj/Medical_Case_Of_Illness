import logging
import os.path
from logging.handlers import RotatingFileHandler
from gevent.wsgi import WSGIServer

from netscaler_sentinel import app

if __name__ == '__main__':
    logs = app.config['LOG']
    if not os.path.exists(logs):
        os.makedirs(logs)
    handler = RotatingFileHandler(os.path.join(logs, 'error.log'), maxBytes=1024 * 1024 * 10, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("netscaler listing %s" % app.config['CONFIG_SERVICE'])

    WSGIServer((app.config['HTTP_HOST'], app.config['HTTP_PORT']), application=app).serve_forever()
