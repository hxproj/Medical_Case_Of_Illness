from json import dumps

import flask
import httplib
from netscaler_sentinel import app
from netscaler_sentinel.controller.utils import get_members



@app.route('/netscaler-sentinel/netscaler/<netscaler>/group-members/<servicegroupname>', methods=['GET'])
def get_service_group_members(netscaler, servicegroupname):
    try:
        result = get_members(servicegroupname, netscaler)
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
