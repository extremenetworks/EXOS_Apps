import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# CONSTANTS
JSONRPC_VERSION = '2.0'
IPADDRESS = 'ipaddress'
USERNAME = 'username'
PASSWORD = 'password'
TRANSACTION = 'transaction'
COOKIE = 'session'
X_AUTH_TOKEN = 'X-Auth-Token'
X_AUTH_TOKEN_LOWER = X_AUTH_TOKEN.lower()
_version_ = JSONRPC_VERSION + '.0.3'


#
# This class contains the specifics of constructing a JSONRPC message and
# returning the results
class JsonRPC(object):

    def __init__(self, ipaddress=None, username=None, password=None):
        # the device DB keeps track of information by remote device IP address
        # you may specify an ip address, username, password when this class is create
        # to use that information as the default for all JSONRPC transactions
        # or you can specify these parameters when calling the individual JSONRPC methods
        self.default_ipaddress = None
        self.device_db = {}

        if ipaddress:
            self.default_ipaddress = ipaddress

        self.default_ipaddress = ipaddress
        self.device_db[ipaddress] = {
                IPADDRESS: ipaddress,
                USERNAME: username,
                PASSWORD: password if password else '',
                TRANSACTION: 1,
                COOKIE: None,
                X_AUTH_TOKEN: None,
                }

    @staticmethod
    def version():
        return _version_

#       _ _                  _   _               _
#   ___| (_)  _ __ ___   ___| |_| |__   ___   __| |
#  / __| | | | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` |
# | (__| | | | | | | | |  __/ |_| | | | (_) | (_| |
#  \___|_|_| |_| |_| |_|\___|\__|_| |_|\___/ \__,_|
#
    def cli(self, cmds, ipaddress=None, username=None, password=None):
        # This is the JSONRPC method='cli':
        #   fills out the JSONRPC POST data structures
        #   Sends the POST via HTTP to the EXOS switch
        #   gets the POST response
        #   returns the decoded JSON in native python structures

        # cmds - a single CLI command string or a list of CLI command strings
        # ipaddress,
        # username,
        # password can be provided during the cli() call to enable
        # communications with multiple switches using a single instance of the JsonRPC class
        #
        # Or ipaddress, username, password can be provided during class creation to specify
        # a default switch if communication with multiple switches is not necessary.
        #

        cmd_string = ''
        if isinstance(cmds, list):
            for c in cmds:
                cmd_string += '{};'.format(c.strip())
        else:
            cmd_string = cmds

        # params[0] = CLI command(s) string separated by ';'
        jsonrpc_response = self._send_to_remote_device('cli',
                                                       [cmd_string],
                                                       ipaddress,
                                                       username,
                                                       password
                                                       )

        rslt_list = jsonrpc_response.get('result')
        if rslt_list is None:
            raise ValueError("JSON result field is not present in response")

        # return the JSONRPC response to the caller
        return jsonrpc_response

#                                 _       _
#  _ __ _   _ _ __  ___  ___ _ __(_)_ __ | |_
# | '__| | | | '_ \/ __|/ __| '__| | '_ \| __|
# | |  | |_| | | | \__ \ (__| |  | | |_) | |_
# |_|   \__,_|_| |_|___/\___|_|  |_| .__/ \__|
#                                  |_|
#                 _   _               _
#  _ __ ___   ___| |_| |__   ___   __| |
# | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` |
# | | | | | |  __/ |_| | | | (_) | (_| |
# |_| |_| |_|\___|\__|_| |_|\___/ \__,_|
#
    def runscript(self, params, ipaddress=None, username=None, password=None):
        # This is the JSONRPC method='runscript'
        # These scripts use the exsh.clicmd() to issue CLI commands to EXOS.
        # This method is used for remotely running scripts that could also be
        # run on the switch using the 'run script' CLI command.

        # JSONRPC defines params as a list
        # EXOS expects params[0] to be the script to run on the remote system
        #
        # params[0]: then entire script as a string. usually read from a file
        # params[1:]: any additional command line parameters
        # ipaddress,
        # username,
        # password can be provided during the cli() call to enable
        # communications with multiple switches using a single instance of the JsonRPC class
        # Or ipaddress, username, password can be provided during class creation to specify
        # a default switch if communication with multiple switches is not necessary.

        if not isinstance(params, list):
            raise TypeError('params must be a list')

        jsonrpc_response = self._send_to_remote_device('runscript',
                                                       params,
                                                       ipaddress,
                                                       username,
                                                       password
                                                       )
        return jsonrpc_response

#              _   _                                  _   _               _
#  _ __  _   _| |_| |__   ___  _ __    _ __ ___   ___| |_| |__   ___   __| |
# | '_ \| | | | __| '_ \ / _ \| '_ \  | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` |
# | |_) | |_| | |_| | | | (_) | | | | | | | | | |  __/ |_| | | | (_) | (_| |
# | .__/ \__, |\__|_| |_|\___/|_| |_| |_| |_| |_|\___|\__|_| |_|\___/ \__,_|
# |_|    |___/
#
    def python(self, params, ipaddress=None, username=None, password=None):
        # This is the JSONRPC method='python':
        # this method is used for remotely running python applications that use
        # the published EXOS python api. The JSONRPC constuction is similar to
        # the 'runscript' method, but the python application has a wider selection
        # of EXOS API calls available for a more advanced application.

        # JSONRPC defines params as a list
        # EXOS expects params[0] to be the script to run on the remote system
        #
        # params[0]: then entire script as a string. usually read from a file
        # params[1:]: any additional command line parameters
        # ipaddress,
        # username,
        # password can be provided during the cli() call to enable
        # communications with multiple switches using a single instance of the JsonRPC class
        # Or ipaddress, username, password can be provided during class creation to specify
        # a default switch if communication with multiple switches is not necessary.

        if not isinstance(params, list):
            raise TypeError('params must be a list')

        jsonrpc_response = self._send_to_remote_device('python',
                                                       params,
                                                       ipaddress,
                                                       username,
                                                       password
                                                       )

        return jsonrpc_response

    #
    # this function keeps track of device information by IP address
    # if an entry isn't found, a new entry is created.
    # if specific username/password is not provided for an IP address
    # the default username/password is returned (provided to __init__())
    def _lookup_device_info(self, ipaddress, username=None, password=None):
        # returns the dict of device specific info for the ipaddress
        if ipaddress is None:
            # cause an exception if the default is also not present
            try:
                return self.device_db[self.default_ipaddress]
            except KeyError:
                raise KeyError('No Device IP address')

        # couldn't find a matching IP address entry. Create a new one
        if ipaddress:
            # if we have an entry for an IP address already, use that
            db_row = self.device_db.get(ipaddress)
            if db_row:
                return db_row

            # if the individual username/password is not provided,
            # see if there is are default values
            default_row = self.device_db.get(self.default_ipaddress)
            if default_row:
                if username is None:
                    username = default_row.get(USERNAME)
                if password is None:
                    password = default_row.get(PASSWORD)

            self.device_db[ipaddress] = {
                    IPADDRESS: ipaddress,
                    USERNAME: username,
                    PASSWORD: password if password else '',
                    TRANSACTION: 1,
                    COOKIE: None,
                    X_AUTH_TOKEN: None,
                    }
            return self.device_db[ipaddress]
        raise KeyError('No Device IP address')

    def _send_to_remote_device(self, method, params, ipaddress=None, username=None, password=None):
        # this function formats the JSONRPC 2.0 request
        # method = cli, runscript, python
        # params = a list passed in from the caller
        # ipaddress = switch IP address, if not provided use the default
        # username = switch username, if not provided, use the default
        # password = switch password, if not provided, use the default

        # Lookup the parameter db for this IP address
        try:
            device_dict = self._lookup_device_info(ipaddress, username, password)
        except Exception:
            raise

        # id = transcation number unique to an IP address
        device_dict[TRANSACTION] += 1

        # format the HTTP body
        json_request = {'method': method,
                        'id': device_dict[TRANSACTION],
                        'jsonrpc': JSONRPC_VERSION,
                        'params': params,
                        }

        # http headers
        headers = {'Content-Type': 'application/json'}

        # after the first authentication, EXOS returns a cookie we can use
        # in JSONRPC transactions to avoid re-authenticating for every transaction
        cookie = {}
        if device_dict.get(X_AUTH_TOKEN):
            # X_AUTH_TOKEN in 22.5 is used as a header and a cookie
            headers[X_AUTH_TOKEN] = device_dict.get(X_AUTH_TOKEN)
            cookie[X_AUTH_TOKEN_LOWER] = device_dict.get(X_AUTH_TOKEN)

        # if we have a cookie from previsous authentication, use it
        if device_dict.get(COOKIE):
            cookie[COOKIE] = device_dict.get(COOKIE)

        # auth_retry will handle the case if the session cookie expires
        # If that happens, the credentials provided are re-authorized
        for auth_retry in range(2):
            if cookie:
                # if we have a cookie, don't use credentials
                auth = None
            else:
                # no cookie available, use login credentials
                auth = (device_dict.get(USERNAME), device_dict.get(PASSWORD))

            # use https if available
            for protocol in ['https', 'http']:
                # construct a JSONRPC URL for the EXOS JSONRPC POST message
                url = '{proto}://{ip}/jsonrpc'.format(
                        proto=protocol,
                        ip=device_dict.get(IPADDRESS))

                # send the JSONRPC message to the EXOS switch
                try:
                    response = requests.post(
                        url,
                        headers=headers,
                        verify=False,
                        cookies=cookie,
                        auth=auth,
                        json=json_request)
                    break
                except Exception as e:
                    # device did not like the protocol choice, try the next one
                    pass
            else:
                # a basic http transport error occured
                raise

            # did authentication fail using a cookie?
            # Try again using credentials
            if response.status_code == 401 and auth is None:
                cookie = {}
                device_dict[X_AUTH_TOKEN] = None
                device_dict[COOKIE] = None
                continue
            break

        # interpret the response from the EXOS switch
        # first check the HTTP error code to see if HTTP was successful
        # delivering the message
        if response.status_code != requests.codes.ok:
            # raise http exception
            response.raise_for_status()

        # if X-Auth-Token is present, use that for a auth
        if device_dict[X_AUTH_TOKEN] is None:
            device_dict[X_AUTH_TOKEN] = response.headers.get(X_AUTH_TOKEN)
            if device_dict[X_AUTH_TOKEN] is None:
                device_dict[X_AUTH_TOKEN] = response.cookies.get(X_AUTH_TOKEN.lower())

        # if we have a cookie, store it so we can use it later
        if device_dict[COOKIE] is None:
            device_dict[COOKIE] = response.cookies.get('session')

        try:
            # ensure the response is JSON encoded
            return response.json()
        except Exception as e:
            raise e
