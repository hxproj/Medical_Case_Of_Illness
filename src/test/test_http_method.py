import unittest

import mock

from netscaler_sentinel.controller.method import httpmethod
from netscaler_sentinel.controller.method import methoddefine


class Testhttpmethod(unittest.TestCase):
    def setUp(self):
        self._jsonget = httpmethod.jsonget
        self._old_method = httpmethod.netscalerget
        self._jsonput = httpmethod.jsonput
        httpmethod.netscalerget = mock.Mock(spec=methoddefine.netscalerget,
                                            return_value='True')

    def tearDown(self):
        httpmethod.netscalerget = self._old_method
        httpmethod.jsonget = self._jsonget
        httpmethod.jsonput = self._jsonput

    def test_netscalerget(self):
        self.assertEqual(httpmethod.httprequest('netscalerget', 'url'), 'True')

    def test_jsonget(self):
        httpmethod.jsonget = mock.Mock(spec=methoddefine.jsonget,
                                       return_value='True')
        self.assertEqual(httpmethod.httprequest('jsonget', 'url'), 'True')

    def test_jsonput(self):
        httpmethod.jsonput = mock.Mock(spec=methoddefine.jsonput,
                                       return_value='True')
        self.assertEqual(httpmethod.httprequest('jsonput', 'url'), 'True')


if __name__ == '__main__':
    unittest.main()
