import unittest
import httpretty
from netscaler_sentinel.controller import utils
from netscaler_sentinel import app


class Test_utils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @httpretty.activate
    def test_get_netscaler_from_config(self):
        # res = requests.Response()
        # config_value = json.dumps({"netscalers": [{"IP": "10.1.38.40", "User": "nsreader1", "Passwd": "aJBI@5dpO!"}]})
        # result = {"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": config_value}
        # res._content = json.dumps(result)
        app.config['CONFIG_SERVICE'] = 'http://mock/eggkeeper/v1/'
        return_result = '{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": "{\\"netscalers\\":[{\\"IP\\":\\"10.1.38.40\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}'

        httpretty.register_uri(httpretty.GET,
                               "http://mock/eggkeeper/v1/Netscaler_sentinel/Netscaler_servers",
                               body=return_result)
        self.assertEqual(utils.get_netscaler_from_config(), '{"netscalers": [{"ip": "10.1.38.40"}]}')

    @httpretty.activate
    def test_get_groups_from_cache(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               body='{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "Value": "{\\"netscalers\\":[{\\"IP\\":\\"10.1.38.40\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}')
        result = utils.get_groups('mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'Passwd': u'aJBI@5dpO!', u'IP': u'10.1.38.40', u'User': u'nsreader'}]})

    @httpretty.activate
    def test_get_groups_from_netscaler(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               status=400)
        httpretty.register_uri(httpretty.PUT,
                               uri=app.config['NAIR_ADDRESS'],
                               status=200)
        httpretty.register_uri(httpretty.GET,
                               uri="https://mock/nitro/v1/stat/servicegroup",
                               body='{"netscalers": [{"ip": "10.1.38.40"}]}',
                               status=200)
        app.config['CONFIG_SERVICE'] = 'http://mock/eggkeeper/v1/'
        return_result = '{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": "{\\"netscalers\\":[{\\"IP\\":\\"mock\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}'

        httpretty.register_uri(httpretty.GET,
                               "http://mock/eggkeeper/v1/Netscaler_sentinel/Netscaler_servers",
                               body=return_result,
                               status=200)
        result = utils.get_groups('mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'ip': u'10.1.38.40'}]})

    @httpretty.activate
    def test_get_groupmembers_from_netscaler(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               status=400)
        httpretty.register_uri(httpretty.PUT,
                               uri=app.config['NAIR_ADDRESS'],
                               status=200)
        httpretty.register_uri(httpretty.GET,
                               uri="https://mock/nitro/v1/config/servicegroup_binding/mock",
                               body='{"netscalers": [{"ip": "10.1.38.40"}]}',
                               status=200)
        app.config['CONFIG_SERVICE'] = 'http://mock/eggkeeper/v1/'
        return_result = '{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": "{\\"netscalers\\":[{\\"IP\\":\\"mock\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}'

        httpretty.register_uri(httpretty.GET,
                               "http://mock/eggkeeper/v1/Netscaler_sentinel/Netscaler_servers",
                               body=return_result,
                               status=200)
        result = utils.get_members('mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'ip': u'10.1.38.40'}]})

    @httpretty.activate
    def test_get_groupmembers_from_cache(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               body='{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "Value": "{\\"netscalers\\":[{\\"IP\\":\\"10.1.38.40\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}')
        result = utils.get_members('mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'Passwd': u'aJBI@5dpO!', u'IP': u'10.1.38.40', u'User': u'nsreader'}]})

    @httpretty.activate
    def test_get_member_from_cache(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               body='{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "Value": "{\\"netscalers\\":[{\\"IP\\":\\"10.1.38.40\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}')
        result = utils.get_member_status('mock', 'mock', 'mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'Passwd': u'aJBI@5dpO!', u'IP': u'10.1.38.40', u'User': u'nsreader'}]})

    @httpretty.activate
    def test_get_member_from_netscaler(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               status=400)
        httpretty.register_uri(httpretty.PUT,
                               uri=app.config['NAIR_ADDRESS'],
                               status=200)
        httpretty.register_uri(httpretty.GET,
                               uri="https://mock/nitro/v1/stat/servicegroupmember?args=servicegroupname:mock,serverName:mock,port:mock",
                               body='{"netscalers": [{"ip": "10.1.38.40"}]}',
                               status=200)
        app.config['CONFIG_SERVICE'] = 'http://mock/eggkeeper/v1/'
        return_result = '{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": "{\\"netscalers\\":[{\\"IP\\":\\"mock\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}'

        httpretty.register_uri(httpretty.GET,
                               "http://mock/eggkeeper/v1/Netscaler_sentinel/Netscaler_servers",
                               body=return_result)
        result = utils.get_member_status('mock', 'mock', 'mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'ip': u'10.1.38.40'}]})

    @httpretty.activate
    def test_get_virtual_servers_cache(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock-load_balance'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               body='{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "Value": "{\\"netscalers\\":[{\\"IP\\":\\"10.1.38.40\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}')
        result = utils.get_load_balance('mock-load_balance')
        self.assertEqual(result,
                         {u'netscalers': [{u'Passwd': u'aJBI@5dpO!', u'IP': u'10.1.38.40', u'User': u'nsreader'}]})

    @httpretty.activate
    def test_get_virtual_servers_from_netscaler(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock-load_balance'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               status=400)
        httpretty.register_uri(httpretty.PUT,
                               uri=app.config['NAIR_ADDRESS'],
                               status=200)
        httpretty.register_uri(httpretty.GET,
                               uri="https://mock/nitro/v1/config/lbvserver",
                               body='{"netscalers": [{"ip": "10.1.38.40"}]}',
                               status=200)
        app.config['CONFIG_SERVICE'] = 'http://mock/eggkeeper/v1/'
        return_result = '{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": "{\\"netscalers\\":[{\\"IP\\":\\"mock\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}'

        httpretty.register_uri(httpretty.GET,
                               "http://mock/eggkeeper/v1/Netscaler_sentinel/Netscaler_servers",
                               body=return_result)
        result = utils.get_load_balance('mock-load_balance')
        self.assertEqual(result,
                         {u'netscalers': [{u'ip': u'10.1.38.40'}]})

    @httpretty.activate
    def test_get_load_balance_binding_cache(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               body='{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "Value": "{\\"netscalers\\":[{\\"IP\\":\\"10.1.38.40\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}')
        result = utils.get_load_balance_bindings('mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'Passwd': u'aJBI@5dpO!', u'IP': u'10.1.38.40', u'User': u'nsreader'}]})

    @httpretty.activate
    def test_get_load_balance_binding_from_netscaler(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               status=400)
        httpretty.register_uri(httpretty.PUT,
                               uri=app.config['NAIR_ADDRESS'],
                               status=200)
        httpretty.register_uri(httpretty.GET,
                               uri="https://mock/nitro/v1/config/lbvserver_binding/mock",
                               body='{"netscalers": [{"ip": "10.1.38.40"}]}',
                               status=200)
        app.config['CONFIG_SERVICE'] = 'http://mock/eggkeeper/v1/'
        return_result = '{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": "{\\"netscalers\\":[{\\"IP\\":\\"mock\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}'

        httpretty.register_uri(httpretty.GET,
                               "http://mock/eggkeeper/v1/Netscaler_sentinel/Netscaler_servers",
                               body=return_result)
        result = utils.get_load_balance_bindings('mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'ip': u'10.1.38.40'}]})

    @httpretty.activate
    def test_get_service_from_cache(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               body='{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "Value": "{\\"netscalers\\":[{\\"IP\\":\\"10.1.38.40\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}')
        result = utils.get_service_status('mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'Passwd': u'aJBI@5dpO!', u'IP': u'10.1.38.40', u'User': u'nsreader'}]})

    @httpretty.activate
    def test_get_service_from_netscaler(self):
        app.config['NAIR_ADDRESS'] = 'http://mock/nair/v1/wh7/database'
        url = app.config['NAIR_ADDRESS'] + '/' + 'netscalercache' + '/' + 'mock'
        httpretty.register_uri(httpretty.GET,
                               uri=url,
                               status=400)
        httpretty.register_uri(httpretty.PUT,
                               uri=app.config['NAIR_ADDRESS'],
                               status=200)
        httpretty.register_uri(httpretty.GET,
                               uri="https://mock/nitro/v1/stat/service/mock",
                               body='{"netscalers": [{"ip": "10.1.38.40"}]}',
                               status=200)
        app.config['CONFIG_SERVICE'] = 'http://mock/eggkeeper/v1/'
        return_result = '{"systemName": "Netscaler_sentinel", "configName": "Netscaler_servers", "configValue": "{\\"netscalers\\":[{\\"IP\\":\\"mock\\",\\"User\\":\\"nsreader\\",\\"Passwd\\":\\"aJBI@5dpO!\\"}]}"}'

        httpretty.register_uri(httpretty.GET,
                               "http://mock/eggkeeper/v1/Netscaler_sentinel/Netscaler_servers",
                               body=return_result)
        result = utils.get_service_status('mock', 'mock')
        self.assertEqual(result,
                         {u'netscalers': [{u'ip': u'10.1.38.40'}]})


if __name__ == '__main__':
    unittest.main()
