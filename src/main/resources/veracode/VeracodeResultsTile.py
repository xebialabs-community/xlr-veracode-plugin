#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# Sequence of actions is
# 1. https://analysiscenter.veracode.com/api/4.0/getappbuilds.do.
# 2. Get build_id, e.g., 2855466.
# 3. https://analysiscenter.veracode.com/api/4.0/detailedreport.do?build_id=2855466 for xml data

import json
import subprocess
from xml.etree import ElementTree as ET
from HTMLParser import HTMLParser

def cleanXml(xmlstring):
    h = HTMLParser()
    return re.sub(' xmlns="[^"]+"', '', h.unescape(xmlstring).replace('&', '+'), count=1)

if not veracodeServer:
  raise Exception("Veracode server must be provided")

veracodeCredentials = "%s:%s" % (veracodeServer['username'],veracodeServer['password'])

# The Veracode api works only under curl, so we break out to a shell subprocess here rather than using HttpRequest/HttpResponse.
appBuilds = subprocess.check_output(['/usr/bin/curl', '-u', veracodeCredentials, '%s/api/4.0/getappbuilds.do' % veracodeServer['url']])
appBuildsXmlRoot = ET.fromstring(cleanXml(appBuilds))

build_id = None
for build in appBuildsXmlRoot.iter('build'):
    build_id = build.attrib['build_id']

data = {}
if build_id:
    detailedReport = subprocess.check_output(['/usr/bin/curl', '-u', veracodeCredentials, '%s/api/4.0/detailedreport.do?build_id=%s' % (veracodeServer['url'], build_id)])
    detailedReportXmlRoot = ET.fromstring(cleanXml(detailedReport))
    for staticAnalysis in detailedReportXmlRoot.iter('static-analysis'):
        data = []
        for key in staticAnalysis.attrib:
            data.append({'key': str(key), 'value': str(staticAnalysis.attrib[key])})
