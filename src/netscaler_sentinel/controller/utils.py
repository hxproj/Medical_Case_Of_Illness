import httplib
import json

from netscaler_sentinel import app
from netscaler_sentinel.controller.method.httpmethod import httprequest
from netscaler_sentinel.naircache.checkcache import check_cache


def get_netscaler_from_config():
    configurl = app.config['CONFIG_SERVICE'] + app.config['CONFIG_SYSTEM'] + '/' + app.config['CONFIG_NAME']
    response = httprequest('jsonget', configurl)
    tmp = response.json()
    resultlist = json.loads(tmp['configValue'])['netscalers']
    netscalerIPlist = []
    for item in resultlist:
        tempdict = {'ip': item['IP']}
        netscalerIPlist.append(tempdict)
    result = {"netscalers": netscalerIPlist}
    return json.dumps(result)


def get_user_and_passwd(netscaler):
    configurl = app.config['CONFIG_SERVICE'] + app.config['CONFIG_SYSTEM'] + '/' + app.config['CONFIG_NAME']
    response = httprequest('jsonget', configurl)
    tmp = response.json()
    resultlist = json.loads(tmp['configValue'])['netscalers']
    for item in resultlist:
        if (item['IP'] == netscaler):
            return item['User'], item['Passwd']
    raise Exception('can not find the server')


@check_cache
def get_groups(netscaler):
    url = 'https://{0}/nitro/v1/stat/servicegroup'.format(netscaler)
    return _get_from_netscaler(netscaler, url)


@check_cache
def get_members(servicegroupname, netscaler):
    url = 'https://{0}/nitro/v1/config/servicegroup_binding/{1}'.format(netscaler, servicegroupname)
    return _get_from_netscaler(netscaler, url)


@check_cache
def get_member_status(member, netscaler, servicegroupname, port):
    member = member.split('-')[0]
    url = 'https://{0}/nitro/v1/stat/servicegroupmember?args=servicegroupname:{1},serverName:{2},port:{3}'.format(
        netscaler, servicegroupname, member, port)
    return _get_from_netscaler(netscaler, url)


@check_cache
def get_load_balance(netscaler):
    netscaler = netscaler.split('-')[0]
    url = 'https://{0}/nitro/v1/config/lbvserver'.format(netscaler)
    return _get_from_netscaler(netscaler, url)

@check_cache
def get_load_balance_bindings(virtual_server, netscaler):
    url = 'https://{0}/nitro/v1/config/lbvserver_binding/{1}'.format(netscaler,virtual_server)
    return _get_from_netscaler(netscaler, url)

@check_cache
def get_service_status(service_name, netscaler):
    service_name=service_name.split('_-')[0]
    url = 'https://{0}/nitro/v1/stat/service/{1}'.format(netscaler,service_name)
    return _get_from_netscaler(netscaler, url)


def _get_from_netscaler(netscaler, url):
    user, passwd = get_user_and_passwd(netscaler)
    headers = {"X-NITRO-USER": user, "X-NITRO-PASS": passwd,
               "Content-Type": "application/vnd.com.citrix.netscaler.lbvserver+json"}
    response = httprequest('netscalerget', url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
