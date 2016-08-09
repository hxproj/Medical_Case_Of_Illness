import httplib
from json import loads, dumps

from netscaler_sentinel import app
from netscaler_sentinel.controller.method.httpmethod import httprequest


def savecache(key, value, expiretime):
    url = app.config['NAIR_ADDRESS']
    database = app.config['NAIR_DATABASE_NAME']
    body = {"Database": database, "Key": key, "Value": dumps(value), "ExpireTime": expiretime}
    response = httprequest('jsonput', url, json=body)


def getcache(key):
    url = app.config['NAIR_ADDRESS']
    database = app.config['NAIR_DATABASE_NAME']
    url = url + '/' + database + '/' + key
    result = httprequest('jsonget', url)
    if result.status_code == 200:
        tmp = result.json()
        return loads(tmp['Value'])
    else:
        return False
