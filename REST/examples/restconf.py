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

RESTCONF = 'restconf'
X_AUTH_TOKEN = 'X-Auth-Token'

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
        self.requests_func_dict = {
            self.GET : requests.get,
            self.POST : requests.post,
            self.PUT : requests.put,
            self.PATCH : requests.patch,
            self.DELETE : requests.delete,
            }

    def get(self, rest_url):
        return self._send_http(self.GET, rest_url)

    def post(self, rest_url, data):
        return self._send_http(self.POST, rest_url, data)

    def put(self, rest_url, data):
        return self._send_http(self.PUT, rest_url, data)

    def patch(self, rest_url, data):
        return self._send_http(self.PATCH, rest_url, data)

    def delete(self, rest_url):
        return self._send_http(self.DELETE, rest_url)

    def _send_http(self, http_operation, rest_url, data=None):
        # this function handles the authentication wrappers
        # collecting the top level RESTCONF url
        # sending the HTTP transaction
        # returning the results or raising an excpetion if there was an error

        # translate the HTTP method into a requests function
        http_func = self.requests_func_dict.get(http_operation)
        if http_func is None:
            raise ValueError('HTTP operation should be POST, PUT, PATCH')

        # find the top level URL for RESTCONF
        self.get_top_url()

        # setup the authentication attempts based on:
        # Token present
        # username/password present
        if self.token:
            # try token first without username/password
            auth_list = [None, (self.username, self.password)]
        else:
            # no toke, use username/password
            auth_list = [(self.username, self.password)]

        for auth in auth_list:
            headers = {}
            if data:
                headers['Content-Type'] = 'application/json'
            if self.token:
                headers[X_AUTH_TOKEN] = self.token

            # try https first, then http
            for protocol in ['https', 'http']:
                # build the URL to be sent to the device
                rest_url = rest_url.lstrip('/')
                url = '{protocol}://{ipaddress}{top_url}/{rest_url}'.format(
                        protocol=protocol,
                        ipaddress=self.ipaddress,
                        top_url=self.top_url,
                        rest_url=rest_url)

                # send the request to the device
                try:
                    response = http_func(url,
                            headers=headers,
                            auth=auth,
                            json=data,
                            verify=False)
                    break
                except Exception as e:
                    # HTTP transport exception
                    continue
            else:
                raise

            # get the response and check for errors
            if response.status_code in [401]:
                # Authentication problem, reset the token and try again
                self.token = None
                continue

            if response.status_code != requests.codes.ok:
                # raise http exception for calling function to catch
                response.raise_for_status()

            break

        self._extract_token(response)

        # returns the requests response to the caller
        return response

    def _extract_token(self, response):
        token = response.headers.get(X_AUTH_TOKEN)
        if token:
            self.token = token
            return
        token = response.cookies.get(X_AUTH_TOKEN)
        if token:
            self.token = token
            return

    def exos_auth(self):
        if self.token:
            return
        try:
            response = requests.post('http://{0}/auth/token/'.format(self.ipaddress),
                headers={'Content-Type': 'application/json'},
                json={'username':self.username, 'password':self.password})
            self.token =  response.json().get('token')
        except Exception as e:
            raise
        if self.token is None:
            raise IOError('Login username/password is incorrect')

    def get_top_url(self):
        if self.top_url:
            return

        headers = {}
        headers['Content-Type'] = 'application/xrd+xml'
        if self.token:
            headers[X_AUTH_TOKEN] = self.token
            auth = None
        else:
            auth = (self.username, self.password)

        try:
            response = requests.get('http://{0}/.well-known/host-meta/'.format(self.ipaddress),
                headers=headers,
                auth=auth)
        except Exception as e:
            raise

        root = ET.fromstring(response.text)

        for child in root:
            if child.attrib.get('rel') == RESTCONF:
                self.top_url = child.attrib.get('href')
                break

        self._extract_token(response)

        if self.top_url is None:
            self.top_url = ''
            raise IOError('Unknown /.well-known/host-meta/ for restconf')

