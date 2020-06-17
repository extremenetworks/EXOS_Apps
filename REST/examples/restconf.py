#!/usr/bin/env python
# Python Scripts provided by Extreme Networks.

# This script is provided free of charge by Extreme.  We hope such scripts are
# helpful when used in conjunction with Extreme products and technology;
# however, scripts are provided simply as an accommodation and are not
# supported nor maintained by Extreme.  ANY SCRIPTS PROVIDED BY EXTREME ARE
# HEREBY PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL EXTREME OR ITS
# THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH SCRIPTS.


import requests
import xml.etree.ElementTree as ET
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


RESTCONF = 'restconf'
_version_ = '1.2.0.0'

#
# This class contains the specifics of constructing a REST message and
# returning the results
class Restconf(object):

    def __init__(self, ipaddress, username, password=None, debug=None):
        self.ipaddress = ipaddress
        self.username = username
        self.password = password
        self.top_url = None
        self.token = None
        self.debug = debug

        # used for update transactions
        self.GET = 'GET'
        self.POST = 'POST'
        self.PUT = 'PUT'
        self.PATCH = 'PATCH'
        self.DELETE = 'DELETE'
        self.update_func_dict = {
            self.GET : requests.get,
            self.POST : requests.post,
            self.PUT : requests.put,
            self.PATCH : requests.patch,
            self.DELETE : requests.delete,
            }

    @staticmethod
    def version():
        return _version_

    def get(self, rest_url):
        return self._without_body(self.GET, rest_url)

    def post(self, rest_url, data):
        return self._with_body(self.POST, rest_url, data)

    def put(self, rest_url, data):
        return self._with_body(self.PUT, rest_url, data)

    def patch(self, rest_url, data):
        return self._with_body(self.PATCH, rest_url, data)

    def delete(self, rest_url):
        return self._without_body(self.DELETE, rest_url)

    def _without_body(self, http_operation, rest_url):
        http_func = self.update_func_dict.get(http_operation)
        if http_func is None:
            raise ValueError('HTTP operation should be POST, PUT, PATCH')

        self.auth() # get authorized
        self.get_top_url() # find the top level URL for RESTCONF

        # try https first, then http
        for protocol in ['https', 'http']:
            # build the URL to be sent to the device
            url = '{protocol}://{ipaddress}{top_url}/{rest_url}'.format(
                    protocol=protocol,
                    ipaddress=self.ipaddress,
                    top_url=self.top_url,
                    rest_url=rest_url)

            # collect the HTTP headers
            headers = {}
            headers['Content-Type'] = 'application/json'

            if self.token:
                headers['X-Auth-Token'] = self.token

            # send the POST request to the device
            try:
                response = http_func(url, headers=headers, verify=False)
                break
            except Exception as e:
                continue
        else:
            raise

        # get the response and check for errors
        if response.status_code == requests.codes.ok:
            # returns the requests response to the caller
            return response

        # raise http exception
        response.raise_for_status()


    def _with_body(self, http_operation, rest_url, data):
        http_func = self.update_func_dict.get(http_operation)
        if http_func is None:
            raise ValueError('HTTP operation should be GET, DELETE')

        self.auth() # get authorized
        self.get_top_url() # find the top level URL for RESTCONF

        # try https first, then http
        for protocol in ['https', 'http']:
            # build the URL to be sent to the device
            url = '{protocol}://{ipaddress}{top_url}/{rest_url}'.format(
                    protocol=protocol,
                    ipaddress=self.ipaddress,
                    top_url=self.top_url,
                    rest_url=rest_url)

            # collect the HTTP headers
            headers = {}
            headers['Content-Type'] = 'application/json'
            if self.token:
                headers['X-Auth-Token'] = self.token

            # send the POST request to the device
            try:
                response = http_func(url, headers=headers, json=data, verify=False)
                break
            except Exception as e:
                continue
        else:
            raise

        # get the response and check for errors
        if response.status_code == requests.codes.ok:
            # returns the requests response to the caller
            return response

        # raise http exception
        response.raise_for_status()

    def auth(self):
        if self.token:
            return

        for protocol in ['https', 'http']:
            try:
                response = requests.post('{protocol}://{ipaddress}/auth/token/'.format(protocol=protocol, ipaddress=self.ipaddress),
                    headers={'Content-Type': 'application/json'},
                    json={'username':self.username, 'password':self.password},
                    verify=False)
                self.token =  response.json().get('token')
                break
            except Exception as e:
                continue
        else:
            raise

        if self.token is None:
            raise IOError('Login username/password is incorrect')

    def get_top_url(self):
        if self.top_url:
            return

        for protocol in ['https', 'http']:
            try:
                response = requests.get('{protocol}://{ipaddress}/.well-known/host-meta/'.format(protocol=protocol, ipaddress=self.ipaddress),
                    headers={'Content-Type': 'application/xrd+xml'},
                    verify=False)
                break
            except Exception as e:
                continue
        else:
            raise

        root = ET.fromstring(response.text)
        for child in root:
            if child.attrib.get('rel') == RESTCONF:
                self.top_url = child.attrib.get('href')
                break

        if self.token is None:
            self.top_url = ''
            raise IOError('Unknown /.well-known/host-meta/ for restconf')

