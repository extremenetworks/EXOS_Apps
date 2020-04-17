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

# This is an example script to demostrate how to access and EXOS switch running
# RESTCONF
#
# This script runs on PC or server and accesses an Extreme EXOS switch via RESTCONF.
# It requires:
#   the IP address of the EXOS switch
#   the user name and password for the remote switch
#
# The script then prompts for a RESTCONF URL.
# The response is the data defined by the YANG model for the URL provided
#
#usage: restpost [-h] [-i IPADDRESS] [-u USERNAME] [-p PASSWORD] [-d]
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -i IPADDRESS, --ipaddress IPADDRESS
#                        IP address of remote system
#  -u USERNAME, --username USERNAME
#                        Login username for the remote system
#  -p PASSWORD, --password PASSWORD
#                        Login password for the remote system
#
#

import argparse
import json
try:
    import readline
except:
    pass
from restconf import Restconf
import getpass

class RestPost(Restconf):
    def __init__(self, ipaddress, username, password, debug=False):
        super(RestPost, self).__init__(ipaddress, username, password, debug=debug)

    def __call__(self):
        # start a CLI prompt loop for the user to enter URLs
        while True:
            # prompt the user for an EXOS command
            print('1. data/ 2. operations/ 3. quit')
            input_rpc = int(raw_input('Choose the input RPC option number: '))
            if input_rpc == 1:
                url_prefix = 'data/'
                prompt = 'Complete the RESTCONF URL {0}'.format(url_prefix)
                input_url = raw_input(prompt)
            elif input_rpc == 2:
                url_prefix = 'operations/'
                prompt = 'Complete the RESTCONF URL {0}'.format(url_prefix)
                input_url = raw_input(prompt)
            elif input_rpc == 3:
                break
            else:
                print('Enter a valid option')
                continue

            post_url = url_prefix + input_url
            post_data = raw_input('Enter the body of the request: ')
            post_json = json.loads(post_data)
            try:
                # send the command to the EXOS switch over HTTP.
                # the object will do the proper encoding
                response = self.post(post_url, post_json)
            except Exception as msg:
                print msg
                continue
            
            print 'REST Response for:', post_url
            print '*' * 80

            # decode the response body as JSON data
            if response:
                try:
                    response_dict = response.json()
                    print json.dumps(response_dict, indent=2, sort_keys=True)
                except Exception as e:
                    print e
                    raise
            else:
                print response

def get_params():
    # These are the command line options for jsoncli
    parser = argparse.ArgumentParser(prog = 'restpost')
    parser.add_argument('-i', '--ipaddress',
            help='IP address of remote system',
            default=None)
    parser.add_argument('-u', '--username',
            help='Login username for the remote system')
    parser.add_argument('-p', '--password',
            help='Login password for the remote system',
            default='')
    args = parser.parse_args()
    return args

args = get_params()
if args.ipaddress is None:
    # prompt for ip address of the remote system
    args.ipaddress = raw_input('Enter remote system IP address: ')

if args.username is None:
    # prompt for username
    args.username = raw_input('Enter remote system username: ')
    # also get password
    args.password = getpass.getpass('Remote system password: ')

rest_obj = RestPost(args.ipaddress, args.username, args.password)
try:
    rest_obj()
except KeyboardInterrupt:
    pass
