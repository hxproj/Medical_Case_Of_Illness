import flask

from netscaler_sentinel import app
from netscaler_sentinel.controller.utils import get_netscaler_from_config


@app.route('/netscaler-sentinel/netscaler', methods=['GET'])
def get_net_scaler():
    result = get_netscaler_from_config()
    ret = flask.Response(result)
    ret.headers['Content-Type'] = 'application/json'
    return ret
