import httplib
import json
from json import dumps

import flask

from netscaler_sentinel import app
from netscaler_sentinel.controller.utils import get_member_status, get_members


@app.route('/netscaler-sentinel/netscaler/<netscaler>/group-members/<servicegroupname>/server/<servername>')
def get_member(servername, netscaler, servicegroupname):
    port_list = _get_list(netscaler,servicegroupname,servername)
    return_list = []
    res = {}
    try:
        for port in port_list:
            result = get_member_status(servername+'-'+str(port), netscaler, servicegroupname, port)
            return_list.extend(result['servicegroupmember'])
            res =result
        res['servicegroupmember'] = return_list
        ret = flask.Response(dumps(res))
        ret.headers['Content-Type'] = 'application/json'
        if not res:
            resp = flask.Response("This resource can not be found!")
            return resp, httplib.FORBIDDEN
        else:
            return ret
    except Exception as e:
        resp = flask.Response(e.message)
        return resp, httplib.FORBIDDEN

def _get_list(netscaler, servicegroupname,server):
    result = get_members(servicegroupname,netscaler)
    ret =result['servicegroup_binding']
    lit = []
    for item in ret:
        res = item['servicegroup_servicegroupmember_binding']
        for temp in res:
            if temp['servername']==server:
                lit.append(temp['port'])
    return lit