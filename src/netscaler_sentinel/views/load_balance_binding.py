from netscaler_sentinel import app
import flask
import httplib
from json import dumps

from netscaler_sentinel.controller.utils import get_load_balance_bindings


@app.route('/netscaler-sentinel/netscaler/<netscaler>/virtual-server/<virtual_server>/load-balance-binding')
def get_load_balance_binding(netscaler, virtual_server):
    try:
        result = get_load_balance_bindings(virtual_server, netscaler)
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
