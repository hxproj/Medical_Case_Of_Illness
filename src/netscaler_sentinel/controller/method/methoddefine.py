from functools import partial
import requests

netscalerget = partial(requests.get, headers={"X-NITRO-USER": "nsreader", "X-NITRO-PASS": "aJBI@5dpO!",
                                              "Content-Type": "application/vnd.com.citrix.netscaler.lbvserver+json"},
                       verify=False)
jsonput = requests.put = partial(requests.put,
                                   headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
jsonget = requests.get = partial(requests.get,
                                   headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

notfound = 404
invalid = 403
ok = 200