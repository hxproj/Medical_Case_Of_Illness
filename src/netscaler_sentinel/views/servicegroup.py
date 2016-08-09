from json import dumps
import httplib

import flask

from netscaler_sentinel import app
from netscaler_sentinel.controller.utils import get_groups



@app.route('/netscaler-sentinel/netscaler/<string:netscaler>/service-group', methods=['GET'])
def get_service_groups(netscaler):
    try:
        result = get_groups(netscaler)
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
