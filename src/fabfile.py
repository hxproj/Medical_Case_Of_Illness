import httplib
import logging
import os
import json
import sys

from negowl import factory


def deploy(name, server, image):
    client = factory.get(server)
    code, _ = client.get_container(name)
    if code == httplib.OK:
        code = client.update_image(name, image)
        assert code
    elif code == httplib.NOT_FOUND:
        ports = [dict(type='tcp', privateport=8080, publicport=9000)]
        code, r = client.create_container(name, image, ports=ports)
        assert code == httplib.OK
    else:
        raise Exception("api status code {0}".format(code))


def load_settings(src):
    full_path = os.path.join(src, 'matrix.json')
    with open(full_path, 'rb') as f:
        try:
            return json.load(f)
        except ValueError as e:
            logging.error("%s is invalid json file: %s", full_path, e)
            sys.exit(1)


def image_name(src='.'):
    settings = load_settings(src)
    print '{name}:{tag}'.format(name=settings.get('name'), tag=settings.get('tag', 'latest')),


if __name__ == '__main__':
    deploy("netscalersentinel", "localhost", "docker.neg/netscaler_sentinel:0.0.1")
