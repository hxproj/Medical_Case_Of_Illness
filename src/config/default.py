# Eggkeeper setting
CONFIG_SERVICE = 'http://10.16.75.24:3000/eggkeeper/v1/'
CONFIG_SYSTEM = 'Netscaler_sentinel'
CONFIG_NAME = 'Netscaler_servers'

# Nair cache setting
NAIR_ADDRESS = 'http://10.16.75.24:3000/nair/v1/wh7/database'
NAIR_DATABASE_NAME = 'netscalercache'
GROUP_EXPIRE_TIME = 3600
GROUP_MEMBERS_EXPIRE_TIME = 300
MEMBER_EXPIRE_TIME = 60
SERVICE_EXPIRE_TIME = 60
LOAD_BALANCE_BINDING_EXPIRE_TIME= 1800

HTTP_HOST = ''
HTTP_PORT = 8080
LOG = 'var/netscaler_sentinel/logs'
