#!flask/bin/python
#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from flask import Flask
from flask import request, Response
from flask import make_response, send_from_directory
from werkzeug.exceptions import HTTPException, BadRequest, NotFound
from functools import wraps
import os, io, json

import verify_hmac

app = Flask(__name__)

# These are the username and password we expect 
api_key_id = '3ddaeeb10ca690df3fee5e3bd1c329fa'
api_key_secret = '3ddaeeb10ca690df3fee5e3bd1c329fa3ddaeeb10ca690df3fee5e3bd1c329fa3ddaeeb10ca690df3fee5e3bd1c329fa3ddaeeb10ca690df3fee5e3bd1c329fa'
signing_data = "id=3ddaeeb10ca690df3fee5e3bd1c329fa&host=localhost&url=/api/4.0/detailedreportpdf.do?build_id=1&method=GET"

def getFile( fileName, status="200" ):
     filePath = "../../mockserver/app/responses/%s" % fileName
     if not os.path.isfile(filePath):
        raise NotFound("Unable to load response file")

     # f = io.open(filePath, "r", encoding="utf-8")
     f = io.open(filePath, "r")

     resp = make_response( (f.read(), status) )
     resp.headers['Content-Type'] = 'application/xml; charset=utf-8'

     return resp


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    """
    Determines if the basic auth is valid
    Example...
    Authorization: VERACODE-HMAC-SHA-256 id=3ddaeeb10ca690df3fee5e3bd1c329fa,ts=1588878918722,nonce=a8d7fdb5aa22fc3fdb688fbb6807c2b4,sig=055490fe1aba6c309205ef5322b37a77a9de0646a318de23699e69ce4c5cb9d4
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not verify_hmac.verifyAuthorization(signing_data, request.headers['Authorization'], api_key_secret):
            print('ERROR: hmac authorization failed')
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    return "Hello, from the Mockserver!"

@app.route('/api/4.0/getapplist.do', methods=['GET'])
def getApps():
    return 'app1'

@app.route('/api/4.0/getappbuilds.do', methods=['GET'])
@requires_auth
def getAppBuilds():
    return getFile('sample-appbuilds.xml')

@app.route('/api/4.0/detailedreportpdf.do', methods=['GET'])
@requires_auth
def getDetailedReport():
    build_id = request.args.get('build_id', default = 1, type = int)
    print('Build Id = %s' % build_id)
    fileName = 'sample-detailedreportpdf.pdf'
    filePath = "responses/%s" % fileName
    print('File Path = %s' % filePath)
    return send_from_directory('responses', filename=fileName)


if __name__ == '__main__':
    app.run(debug=False)
