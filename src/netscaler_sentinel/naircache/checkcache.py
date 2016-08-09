import json

from netscaler_sentinel import app
from netscaler_sentinel.controller.method.httpmethod import httprequest
from netscaler_sentinel.naircache.cache import getcache, savecache


def get_user_and_passwd(netscaler):
    configurl = app.config['CONFIG_SERVICE'] + app.config['CONFIG_SYSTEM'] + '/' + app.config['CONFIG_NAME']
    response = httprequest('jsonget', configurl)
    tmp = response.json()
    resultlist = json.loads(tmp['configValue'])['netscalers']
    for item in resultlist:
        if (item['IP'] == netscaler):
            return item['User'], item['Passwd']
    raise Exception('Can\'t find this server')


def check_cache(func):
    def inner(*args, **kwargs):
        cache_key = args[0]
        cache = getcache(cache_key)
        if cache:
            return cache

        new_cache = func(*args, **kwargs)
        length = len(args)
        expiretime = 0
        if length == 1:
            expiretime = app.config['GROUP_EXPIRE_TIME']
        elif length == 2:
            if func.__name__=='get_members':
                expiretime = app.config['GROUP_MEMBERS_EXPIRE_TIME']
            elif func.__name__=='get_service_status':
                expiretime = app.config['SERVICE_EXPIRE_TIME']
            elif func.__name__=='get_load_balance_bindings':
                expiretime = app.config['LOAD_BALANCE_BINDING_EXPIRE_TIME']
        elif length == 4:
            expiretime = app.config['MEMBER_EXPIRE_TIME']
        if new_cache:
            savecache(cache_key, new_cache, expiretime=expiretime)
        return new_cache

    return inner
