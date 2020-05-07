import sys
import requests
import logging

import veracode.HttpRequest as HttpRequest

logging.basicConfig(filename='log/custom-plugin.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.debug("main: begin")

headers = {"User-Agent": "XL Release"}

logging.debug('globals -------------------')
logging.debug(globals())
logging.debug('---------------------------')

host = configuration.getUrl()
api_key_id = configuration.getItem('api_key_id')
api_key_secret = configuration.getItem('api_key_secret')

request = HttpRequest(host, api_key_id, api_key_secret)
api_base = "/appsec/v1"

status, content = request.get_json("/appsec/v1/applications")

if status > 200:
    raise Exception(
        "Failed to connect to Veracode Server. Status: %s" % status
    )
