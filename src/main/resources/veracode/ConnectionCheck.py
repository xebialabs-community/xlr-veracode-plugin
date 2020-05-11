import sys
import logging

from veracode.HttpRequest import HttpRequest

logging.basicConfig(filename='log/custom-plugin.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.debug("main: begin")

host = configuration.url
api_key_id = configuration.api_key_id
api_key_secret = configuration.api_key_secret

logging.debug("  connection parameters : host='%s', api_key='%s'" % (host, api_key_id))

request = HttpRequest(host, api_key_id, api_key_secret)

status, content = request.get("/api/4.0/getapplist.do")

if status > 200:
    raise Exception(
        "Failed to connect to Veracode Server. Status: %s" % status
    )

logging.debug("main: end")
