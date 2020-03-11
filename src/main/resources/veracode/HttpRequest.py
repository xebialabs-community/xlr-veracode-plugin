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

import re
import urllib

from java.lang import Integer
from java.lang import String
from java.util import Arrays

from org.apache.commons.codec.binary import Base64
from org.apache.http import HttpHost
from org.apache.http.auth import AuthScope, NTCredentials, UsernamePasswordCredentials
from org.apache.http.client.config import AuthSchemes, RequestConfig
from org.apache.http.client.methods import HttpGet, HttpHead, HttpPost, HttpPut, HttpDelete, HttpPatch
from org.apache.http.client.protocol import HttpClientContext
from org.apache.http.impl.client import BasicCredentialsProvider, HttpClientBuilder, HttpClients
from org.apache.http.util import EntityUtils
from org.apache.http.entity import StringEntity
from org.apache.http.protocol import BasicHttpContext

from com.xebialabs.xlrelease.domain.configuration import HttpConnection
from xlrelease.HttpResponse import HttpResponse


class HttpRequest:
    def __init__(self, params, username = None, password = None, domain = None):
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

        if params.get('authenticationMethod') == "PAT":
            if not params['username']:
                params['username'] = "dummy"

            if username is not None and not username:
                username = "dummy"

        self.params = HttpConnection(params)
        self.shared_domain = params.get('domain')
        self.username = username
        self.password = password
        self.domain = domain
        self.authentication = params.get('authenticationMethod')


    def buildRequest(self, method, context, body, contentType, headers):
        url = self.quote(self.createPath(self.params.getUrl(), context))

        method = method.upper()

        if method == 'GET':
            request = HttpGet(url)
        elif method == 'HEAD':
            request = HttpHead(url)
        elif method == 'POST':
            request = HttpPost(url)
            request.setEntity(StringEntity(body))
        elif method == 'PUT':
            request = HttpPut(url)
            request.setEntity(StringEntity(body))
        elif method == 'DELETE':
            request = HttpDelete(url)
        elif method == 'PATCH':
            request = HttpPatch(url)
            request.setEntity(StringEntity(body))
        else:
            raise Exception('Unsupported method: ' + method)

        request.addHeader('Content-Type', contentType)
        request.addHeader('Accept', contentType)
        self.setCredentials(request)
        self.setProxy(request)
        self.setHeaders(request, headers)

        return request


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


    def set_basic_credentials(self, request):
        credentials = self.get_credentials()
        encoding = Base64.encodeBase64String(String(credentials["username"] + ':' + credentials["password"]).getBytes('ISO-8859-1'))
        request.addHeader('Authorization', 'Basic ' + encoding)

    def set_pat_credentials(self, request):
        credentials = self.get_credentials()
        encoding = Base64.encodeBase64String(String(':' + credentials["password"]).getBytes('ISO-8859-1'))
        request.addHeader('Authorization', 'Basic ' + encoding)

    def get_ntlm_client(self):
        if self.params.proxyUsername and self.params.proxyPassword:
            proxy = HttpHost(self.params.getProxyHost(), int(self.params.getProxyPort()))
            request_config = RequestConfig.custom().setTargetPreferredAuthSchemes(Arrays.asList(AuthSchemes.NTLM)).setProxy(proxy).build()
            creds_provider = self.get_proxy_credentials_provider()
            http_client = HttpClients.custom().setDefaultRequestConfig(request_config).setDefaultCredentialsProvider(creds_provider).build()
        else:
            request_config = RequestConfig.custom().setTargetPreferredAuthSchemes(Arrays.asList(AuthSchemes.NTLM)).build()
            http_client = HttpClients.custom().setDefaultRequestConfig(request_config).build()
        return http_client

    def get_default_client(self):
        if self.params.proxyUsername and self.params.proxyPassword:
            creds_provider = self.get_proxy_credentials_provider()
            http_client = HttpClients.custom().setDefaultCredentialsProvider(creds_provider).build()
        else:
            http_client = HttpClients.custom().build()
        return http_client


    def setCredentials(self, request):
        if self.username:
            username = self.username
            password = self.password
        elif self.params.getUsername():
            username = self.params.getUsername()
            password = self.params.getPassword()
        else:
            return

        encoding = Base64.encodeBase64String(String(username + ':' + password).getBytes('ISO-8859-1'))
        request.addHeader('Authorization', 'Basic ' + encoding)


    def get_credentials(self):
        if self.username:
            username = self.username
            password = self.password
            domain = self.domain
        elif self.params.getUsername():
            username = self.params.getUsername()
            password = self.params.getPassword()
            domain = self.shared_domain
        else:
            return
        return {'username': username, 'password': password, 'domain': domain}

    def get_proxy_credentials_provider(self):
        credentials = UsernamePasswordCredentials(self.params.proxyUsername, self.params.proxyPassword)
        auth_scope = AuthScope(self.params.proxyHost, Integer.valueOf(self.params.proxyPort))
        creds_provider = BasicCredentialsProvider()
        creds_provider.setCredentials(auth_scope, credentials)
        return creds_provider

    def setProxy(self, request):
        if not self.params.getProxyHost():
            return

        proxy = HttpHost(self.params.getProxyHost(), int(self.params.getProxyPort()))
        config = RequestConfig.custom().setProxy(proxy).build()
        request.setConfig(config)


    def setHeaders(self, request, headers):
        if headers:
            for key in headers:
                request.setHeader(key, headers[key])


    def get_file(self, context, **options):
        """
        Return file content as byte array.
        """
        request = self.buildRequest(
            options.get('method', 'GET'),
            options.get('context', context),
            options.get('body', ''),
            options.get('contentType', None),
            options.get('headers', None))

        client = None
        response = None
        try:
            local_context = BasicHttpContext()
            if self.authentication == "Ntlm":
                credentials = self.get_credentials()
                client = self.get_ntlm_client()
                credentials_provider = BasicCredentialsProvider()
                credentials_provider.setCredentials(AuthScope.ANY, NTCredentials(credentials["username"], credentials["password"], None, credentials["domain"]))
                local_context.setAttribute(HttpClientContext.CREDS_PROVIDER, credentials_provider)
            elif self.authentication == "PAT":
                client = self.get_default_client()
                self.set_pat_credentials(request)
            elif self.authentication == "Basic":
                client = self.get_default_client()
                self.set_basic_credentials(request)
            elif self.params.proxyUsername and self.params.proxyPassword:
                credentials = UsernamePasswordCredentials(self.params.proxyUsername, self.params.proxyPassword)
                auth_scope = AuthScope(self.params.proxyHost, Integer.valueOf(self.params.proxyPort))
                creds_provider = BasicCredentialsProvider()
                creds_provider.setCredentials(auth_scope, credentials)
                client = HttpClientBuilder.create().setDefaultCredentialsProvider(creds_provider).build()
            else:
                client = HttpClients.createDefault()

            response = client.execute(request, local_context)
            status = response.getStatusLine().getStatusCode()
            entity = response.getEntity()
            result = EntityUtils.toByteArray(entity) if entity else None
            headers = response.getAllHeaders()
            EntityUtils.consume(entity)

            return status, result, headers
    
        finally:
            if response:
                response.close()
            if client:
                client.close()
