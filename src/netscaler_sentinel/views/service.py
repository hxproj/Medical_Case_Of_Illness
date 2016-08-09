import flask
import httplib
from netscaler_sentinel import app
from json import dumps

from netscaler_sentinel.controller.utils import get_service_status


@app.route('/netscaler-sentinel/netscaler/<netscaler>/service/<service_name>')
def get_service(service_name,netscaler):
    try:
        result = get_service_status(service_name+'_-status', netscaler)
        ret = flask.Response(dumps(result))
        ret.headers['Content-Type'] = 'application/json'
        if not result:
            resp = flask.Response("This resource can not be found!")
            return resp, httplib.FORBIDDEN
        else:
            return ret
    except Exception as e:
        resp = flask.Response(e.message)
        return resp, httplib.FORBIDDEN