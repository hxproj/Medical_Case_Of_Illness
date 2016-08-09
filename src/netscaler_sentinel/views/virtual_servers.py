import flask
import httplib
from netscaler_sentinel import app
from json import dumps
from netscaler_sentinel.controller.utils import get_load_balance


@app.route('/netscaler-sentinel/netscaler/<netscaler>/virtual-servers')
def get_virtual_servers(netscaler):
    try:
        result = get_load_balance(netscaler + '-load_balance')
        ret = flask.Response(dumps(result))
        ret.headers['Content-Type'] = 'application/json'
        if not result:
            resp = flask.Response("This resource can not be found!")
            resp.headers['Content-Type'] = 'application/json'
            return resp, httplib.FORBIDDEN
        else:
            return ret
    except Exception as e:
        resp = flask.Response(e.message)
        return resp, httplib.FORBIDDEN
