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

#
# This script requires a python environment to run.
# It also requires the requests 2.4.2 module or later.
#
# This sample client application demonstrates the EXOS JSONRPC methods for:
# - cli
# - runscript
#
#
# The command line expects a number of arguments
#    usage: jsonrpc_client [-h] [-d] [-u USERNAME] [-p PASSWORD]
#                          [-i [IPADDRESS [IPADDRESS ...]]] [-c] [-s]
#                          [cli [cli ...]] [script [script ...]]
#
#    optional arguments:
#      -h, --help            show this help message and exit
#      -u USERNAME           Login username for the remote system
#      -p PASSWORD           Login password for the remote system
#      -i [IPADDRESS [IPADDRESS ...]]
#                            IP address(s) of remote systems or <filename>
#                            containing IP addresses
#
#    CLI command options:
#      -c                    Remote CLI command
#      cli                   CLI command
#
#    Script options:
#      -s                    Remote script
#      script                Script and arguments
#
# Examples:
# ---------
# Let jsonrpc_client.py prompt for information
#   jsonrpc_client.py
#       - jsonrpc_client.py will prompt for
#           action - cli or script
#           username
#           password
#           ipaddress(es)
#           cli command or script name/args, depending on action selected
#
# Provide a list of IP addresses and a single CLI command
#   jsonrpc_client.py -u myname -p mypassword -i 10.10.10.1 10.10.10.2 -c create vlan 10-20
#
# Provide a file with IP addresses, interactively prompt for CLI commands
#   jsonrpc_client.py -u myname -p mypassword -i ipaddrlist -c
#
# Provide a file with IP addresses and a file containing CLI commands
#   jsonrpc_client.py -u myname -p mypassword -i ipaddrlist -c cmd_list
#
# Run a script on a single IP address, prompt for the script name and args
#   jsonrpc_client.py -u myname -p mypassword -i 10.10.10.1 -s
#
# Run a script on a single IP address
#   jsonrpc_client.py -u myname -p mypassword -i 10.10.10.1 -s exos_script.py
#
# Run a script on the IP addresses contained in a file
#   jsonrpc_client.py -u myname -p mypassword -i ipaddrlist -s exos_script.py
#

# import the EXOS JSONRPC object
from jsonrpc import JsonRPC

import sys
from os.path import basename, splitext
import argparse
import json
import requests
import getpass
import socket
try:
    import readline
except:
    pass

#     _ ____   ___  _   _ ____  ____   ____
#    | / ___| / _ \| \ | |  _ \|  _ \ / ___|
# _  | \___ \| | | |  \| | |_) | |_) | |
#| |_| |___) | |_| | |\  |  _ <|  __/| |___
# \___/|____/ \___/|_| \_|_| \_\_|    \____|
#
#      _ _
#  ___| (_)
# / __| | |
#| (__| | |
# \___|_|_|
#
def remote_cli(args, jsonrpc):
    # join the command line args into a cmdlist of one entry
    cmd = ' '.join(args.cli)

    # is it a filename that contains a list of CLI commands?
    try:
        with open(args.cli[0], 'r') as fd:
            # the first arg was a filename
            # join the file lines into a ';' separated string of commands
            #cmd = ';'.join(fd.read().strip().splitlines())
            cmd = fd.readlines()
    except:
        pass

    for ipaddr in args.ipaddress:
        print '\n','=' * 80
        print 'IP:',ipaddr
        print '*' * 80
        try:
            # ###################################################################
            # Use the jsonrpc.cli() method to send CLI commands to an IP address
            # cmd = a single CLI command string or a list of CLI command strings
            # ###################################################################
            response = jsonrpc.cli(cmd, ipaddress=ipaddr)
        except Exception as msg:
            print msg
            continue

        # print headers
        print 'JSONRPC Response for:', cmd
        print '*' * 80

        # the jsonrpc.cli() response contains the data structures used by
        # EXOS to create the CLI display output, typically for show commands
        #
        # The special dictionary entry 'CLIoutput' holds the CLI display output
        #
        # Configuration commands typically do not return data structures
        # CLIoutput would contain a newline
        #
        # dump the JSONRPC response to the user in a pretty format
        # first the data stuctures
        print json.dumps(response, indent=2, sort_keys=True)

        result = None
        try:
            if isinstance(response, dict):
                result = response.get('result')
                if "error" in result:
                    continue
        except Exception as e:
            print e
            continue

        # search for each CLI command outputs (CLIoutput) to display
        remote_cli_screen_display(result)

def remote_cli_screen_display(out_list):
    # this function searches for all of the 'CLIoutput' entries and
    # displays them as they would have shown on the EXOS shell output
    #
    # If multiple commands were sent in the request, there will be
    # one CLIoutput entry per command
    if isinstance(out_list, list):
        for cli_out in out_list:
            if isinstance(cli_out, list):
                remote_cli_screen_display(cli_out)
                continue
            if isinstance(cli_out, dict):
                cli_output = cli_out.get('CLIoutput')
                if cli_output is not None:
                    print '\nFormatted CLIoutput Display'
                    print '*' * 80
                    print cli_output
                    print '*' * 80

def prompt_for_cli(args, jsonrpc):
    # start a CLI prompt loop for the user to enter EXOS commands
    while True:
        # prompt the user for an EXOS command
        args.cli = raw_input('Enter EXOS cli or filename: ')
        if args.cli in ['q','quit','exit']:
            break
        if len(args.cli.strip()) == 0:
            print '\tEXOS command or q, quit or exit to discontinue'
            continue

        # split CLI to make it look like a command line arg
        args.cli = args.cli.split()
        remote_cli(args, jsonrpc)


#     _ ____   ___  _   _ ____  ____   ____
#    | / ___| / _ \| \ | |  _ \|  _ \ / ___|
# _  | \___ \| | | |  \| | |_) | |_) | |
#| |_| |___) | |_| | |\  |  _ <|  __/| |___
# \___/|____/ \___/|_| \_|_| \_\_|    \____|
#
#                                _       _
# _ __ _   _ _ __  ___  ___ _ __(_)_ __ | |_
#| '__| | | | '_ \/ __|/ __| '__| | '_ \| __|
#| |  | |_| | | | \__ \ (__| |  | | |_) | |_
#|_|   \__,_|_| |_|___/\___|_|  |_| .__/ \__|
def remote_script(args, jsonrpc):
    # first token must be the local script file name
    script_name = args.cli[0]

    # there any additional command line args to pass to the script on the switch
    script_options = args.cli[1:] if len(args.cli) > 1 else []


    try:
        # open up the script name provided by the user
        with open(script_name, 'r') as fd:
            # read the entire script into the first params entry
            params = [fd.read()]
    except Exception as e:
        print e
        return

    # add any additional parameters to the params list
    params += script_options

    for ipaddr in args.ipaddress:
        print '\n','=' * 80
        print 'IP:',ipaddr
        print '*' * 80

        # ###############################################################
        # Use the jsonrpc.runscript() method to send the script and parameters
        # to the remote IP address
        # params[0] = script as a string
        # params[1:] = script command line args
        # ###############################################################
        try:
            response = jsonrpc.runscript(params, ipaddress=ipaddr)
        except Exception as e:
            print e
            continue

        # extract the response stored in 2 variables 'stdout' and 'stderr'
        result = response.get('result')
        if result:
            if result.get('stdout'):
                print result.get('stdout')

            # if something was output to stderr, print that last
            if result.get('stderr'):
                print 'STDERR\n',result.get('stderr')

def prompt_for_script(args, jsonrpc):
    while True:
        # prompt the user for a script name and args
        cmd = raw_input('run script <file> [args]: ')
        if cmd in ['q','quit','exit']:
            break
        if len(cmd.strip()) == 0:
            print '\t<filename> or q, quit or exit to discontinue'
            continue

        # split the user input into parts
        args.cli = cmd.split()

        # call the script send function
        remote_script(args, jsonrpc)

# ##################################################################
# MAIN APPLICATION
# ##################################################################
def get_params():
    # These are the command line options for jsonrpc_client
    parser = argparse.ArgumentParser(prog = 'jsonrpc_client')
    parser.add_argument('-u',
            dest='username',
            help='Login username for the remote system')
    parser.add_argument('-p',
            dest='password',
            help='Login password for the remote system',
            default='')
    parser.add_argument('-i',
            help='IP address(s) of remote systems or <filename> containing IP addresses',
            dest='ipaddress',
            nargs='*',
            default=[])

    cli_group = parser.add_argument_group('CLI command options')
    cli_group.add_argument('-c',
            help='Remote CLI command',
            dest='is_cli',
            action='store_true',
            default=False)
    cli_group.add_argument('cli',
            help='CLI command',
            nargs='*',
            default=[])

    script_group = parser.add_argument_group('Script options')
    script_group.add_argument('-s',
            help='Remote script',
            dest='is_script',
            action='store_true',
            default=False)
    script_group.add_argument('script',
            help='Script and arguments',
            nargs='*',
            default=[])

    args = parser.parse_args()

    # username/password not provided on the command line, ask
    if args.username is None:
        # prompt for username
        args.username = raw_input('Enter remote system username: ')
        # also get password
        args.password = getpass.getpass('Remote system password: ')


    while not args.ipaddress:
        # no IP address(es) or file name was provided on the command line, ask
        while True:
            # prompt for ip address of the remote system
            input_ipaddress = raw_input('Enter remote system IP address(es) or filename: ')
            input_ipaddress = input_ipaddress.strip()
            input_ipaddress=input_ipaddress.replace(',',' ')
            args.ipaddress = input_ipaddress.split()
            if len(args.ipaddress):
                break

    # args.ipaddress is either a list of IP addresses or a file name
    if len(args.ipaddress) == 1:
        try:
            with open(args.ipaddress[0], 'r') as fd:
                # the first arg was a filename
                # read the contents into args.ipaddress
                args.ipaddress = fd.read().strip().splitlines()
        except:
            pass

    # args.ipaddress is now a list of IP addresses
    # check to see if the addresses are in the correct format
    for ipaddr in args.ipaddress:
        for addr_type in [socket.AF_INET, socket.AF_INET6]:
            try:
                socket.inet_pton(addr_type, ipaddr)
                break
            except Exception as e:
                pass
        else:
            print ipaddr, 'is not a filename or IP address'
            args.ipaddress.remove(ipaddr)

    # the command line didn't tell us what to do. Let's ask
    if args.is_cli is False and args.is_script is False:
        while True:
            # prompt for ip address of the remote system
            method_type = raw_input("Enter either 'cli' or 'script': ")
            method_type = method_type.strip()
            if method_type.startswith('c'):
                args.is_cli = True
                break
            if method_type.startswith('s'):
                args.is_script = True
                break
            print 'Unrecognized input:', method_type


    return args


def main():
    args = get_params()

    # get the version from the class
    print 'JsonRPC', JsonRPC.version()

    # create a JSONRPC interface object with any defaults
    jsonrpc = JsonRPC(username=args.username, password=args.password)

    # or get the version from the object
    # print 'jsonrpc', jsonrpc.version()

    if args.is_script is True:
        # if command line script option, check if we have need to prompt
        if args.cli:
            remote_script(args, jsonrpc)
        else:
            # ask user interactively for script and script args
            prompt_for_script(args, jsonrpc)
    elif args.is_cli is True:
        # if command line cli option, check if we have need to prompt
        if args.cli:
            # command line args are available
            remote_cli(args, jsonrpc)
        else:
            # ask user for CLI command
            prompt_for_cli(args, jsonrpc)
    else:
        print 'Unknown script error'

try:
    main()
except KeyboardInterrupt:
    pass
