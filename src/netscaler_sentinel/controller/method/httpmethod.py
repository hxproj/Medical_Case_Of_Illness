from methoddefine import jsonget
from methoddefine import jsonput
from methoddefine import netscalerget


def httprequest(method, url, **kwargs):
    if method == 'netscalerget':
        return netscalerget(url, **kwargs)
    elif method == 'jsonget':
        return jsonget(url, **kwargs)
    elif method == 'jsonput':
        return jsonput(url, **kwargs)
