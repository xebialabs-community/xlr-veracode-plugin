#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# from XL Release HttpRequest, specialized to return file content as byte array

# v1.2.0 : HMAC Authentication : https://www.veracode.com/blog/customer-news/detailing-veracode%E2%80%99s-hmac-api-authentication

import sys
import re
import urllib
import requests
import logging

from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

class HttpRequest:

    def __init__(self, host, api_key_id, api_key_secret):
        """
        Builds an HttpRequest

        :param params: an <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a>
        :param username: the username
            (optional, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        :param password: an password
            (optional, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        :param domain: the Ntlm authentication domain
            (optional, and only used if Ntlm authentication enabled, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        """
        logging.debug("HttpRequest: __init__")

        self.host = host
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret
        self.headers = {"User-Agent": "XL Release"}


    def createPath(self, url, context):
        url = re.sub('/*$', '', url)
        if context is None:
            return url
        elif context.startswith('/'):
            return url + context
        else:
            return url + '/' + context


    def quote(self, url):
        return urllib.quote(url, ':/?&=%')


    def get_json(self, context, **options):
        url = self.quote(self.createPath(self.host, context))

        headers = self.headers
        header['Content-Type'] = options.get('contentType', None)
        header['Accept'] = options.get('contentType', None)

        try:
            response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(api_key_id=self.api_key_id, api_key_secret=self.api_key_secret), headers=headers)
        except requests.RequestException as e:
            print("Whoops!")
            print(e)
            sys.exit(1)

        if response.ok:
            status = response.status_code
            content = response.json

            return status, content

        else:
            print(response.status_code)
    
    def get_file(self, context, **options):
        """
        Return file content as byte array.
        """
        url = self.quote(self.createPath(self.host, context))

        headers = self.headers
        headers['Content-Type'] = options.get('contentType', None)

        try:
            logging.debug('[get_file] url = "%s"' % url)
            response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(api_key_id=self.api_key_id, api_key_secret=self.api_key_secret), headers=headers)
            logging.debug('[get_file] response...')
            logging.debug(response)
        except requests.RequestException as e:
            logging.error('[get_file] url = "%s" request failed' % url)
            logging.error(e)
            sys.exit(1)

        return response.status_code, response.content
