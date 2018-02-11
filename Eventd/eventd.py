'''
This script is provided free of charge by Extreme.  We hope such scripts are helpful when used
in conjunction with Extreme products and technology; however, scripts are provided simply as an
accommodation and are not supported nor maintained by Extreme.  ANY SCRIPTS PROVIDED BY EXTREME
ARE HEREBY PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL EXTREME OR ITS THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH SCRIPTS.

This module opens a socket to receive SNMP traps.
It parses the OID contents and then matches them to actions specified in a config file.

When an action match is found, a CLI command is issued to EXOS.
'''
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
import os
import argparse
import socket
import json
import time
import exos.api as exosapi

# global constants
EXTREME_VR = None
FROM_IP = 'fromIP'
CMD = 'cmd'
CONFIG_FILE = 'eventd.cfg'

# global variables
gDebug = None
gOidMap = dict()
gActionList = list()
gArgs = None


def ipaddressParam(string):
    'Validate an IP address'
    try:
        socket.inet_aton(string)
    except socket.error as msg:
        raise argparse.ArgumentTypeError(msg)
    return string


def parseConfigLine(line):
    'Parse configuration line as if it came from sys.argv'
    global gDebug
    global gArgs
    parser = argparse.ArgumentParser(prog='eventd')
    parser.add_argument(
            '-i', '--ip_address',
            help='IP address to monitor for SNMP notifications',
            type=ipaddressParam,
            required=True)
    parser.add_argument(
            '-v', '--virtual_router',
            help='Virtual Router used for IP address')
    parser.add_argument(
            '-d', '--debug',
            help='Enable debug',
            action='store_true',
            dest='debug')

    gArgs = parser.parse_args(line.split())
    gDebug = gArgs.debug
    if gDebug:
        print line.split()
        print gArgs


def parseOidMapLine(line):
    'This function parses the oid=const section of the config file'
    oid, sep, name = line.partition('=')
    try:
        gOidMap[oid.strip()] = name.strip()
    except Exception:
        print 'Error parsing oid:', line
    return


def buildCmdList(cmd):
    'take a quoted string containing EXOS commands and return a list'
    cmd = cmd.strip("'")
    return cmd.split(';')


def parseActionLine(line):
    'this function parses the action lines of the config file'
    action = dict()
    for token in line.split(','):
        name, sep, value = token.partition('=')
        name = name.strip()
        value = value.strip()
        if len(value) == 0:
            value = None
        action[name] = value if name != 'cmd' else buildCmdList(value)
    gActionList.append(action)


def processConfig(filename):
    'open and process the config file'
    CONFIG_SECTION_HEADER = '%configuration'
    MAP_SECTION_HEADER = '%map'
    ACTION_SECTION_HEADER = '%action'
    CONFIG_STATE = 1
    MAP_STATE = 2
    ACTION_STATE = 3
    sectionMap = {
            CONFIG_SECTION_HEADER: CONFIG_STATE,
            MAP_SECTION_HEADER: MAP_STATE,
            ACTION_SECTION_HEADER: ACTION_STATE}
    stateMap = {
            CONFIG_STATE: parseConfigLine,
            MAP_STATE: parseOidMapLine,
            ACTION_STATE: parseActionLine}
    state = None
    if gDebug:
        print 'Opening file:', filename
    try:
        cfgf = open(filename, 'r')
    except Exception:
        return
    lineCnt = 0
    for line in cfgf.readlines():
        lineCnt += 1
        if gDebug:
            print lineCnt, ':', line,
        # remove comments
        line, sep, comment = line.partition('#')
        # remove blanks
        line = line.strip()
        if len(line) == 0:
            continue
        if line in sectionMap:
            state = sectionMap[line]
            continue
        if state is None:
            continue
        if state in stateMap:
            stateMap[state](line)
            continue
        print 'Cannot process line:', line

    cfgf.close()


def lookupVR(vrName):
    'Given a virtual router name, query EXOS to find the VR number'
    global EXTREME_VR
    EXTREME_VR = None
    reply = exosapi.exec_cli(['debug cfgmgr show next vlan.vlanProc action=SHOW_VR name2=None'])
    vrReply = json.loads(str(reply))
    vrTable = vrReply['data']
    for vr in vrTable:
        if vr['status'] in ['MORE', 'SUCCESS']:
            if vr["name2"] == vrName:
                if vr["vrId"] is not None and int(vr["vrId"]) != 0:
                    EXTREME_VR = int(vr["vrId"])
                    break


def matchActions(eventDict):
    'match action keyword/values to the event'
    if gDebug:
        print 'SNMP notification:'
        for eventName, eventVal in eventDict.items():
            print ' ' * 4, '{0}:{1}'.format(eventName, eventVal)

    if gDebug:
        print 'Scanning actions'
    for action in gActionList:
        if gDebug:
            print ' ' * 4, action
        for name, val in action.items():
            if name == CMD:
                continue
            if name not in eventDict:
                break
            if val != eventDict[name]:
                break
            if gDebug:
                print '  Matched:', name, val
        else:
            if CMD in action:
                if gDebug:
                    print 'EXOS CLI:', action[CMD]
                exosapi.exec_cli(action[CMD])


def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    'callback function when an SNMP trap is received'
    trapMap = {
            "'coldStart'": '1.3.6.1.6.3.1.1.5.1',
            "'warmStart'": '1.3.6.1.6.3.1.1.5.2'
            }

    eventDict = dict()
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
            )

        (fromIP, fromPort) = transportAddress
        eventDict[FROM_IP] = fromIP

        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                if gDebug:
                    print('\nEnterprise: %s' % (
                        pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                        )
                    )
                    print('Agent Address: %s' % (
                        pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                        )
                    )
                    print('Generic Trap: %s' % (
                        pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                        )
                    )
                    print('Specific Trap: %s' % (
                        pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                        )
                    )
                    print('Uptime: %s' % (
                        pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                        )
                    )
                trapType = pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                if trapType in trapMap:
                    oidKey = trapMap[trapType]
                    if oidKey in gOidMap:
                        eventDict[gOidMap[oidKey]] = None
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)

            if gDebug:
                print('Var-binds:')
                for oid, value in varBinds:
                    print('%s = %s' % (oid.prettyPrint(), value.prettyPrint()))

            # constuct a dictionary of translated name/values
            for oid, value in varBinds:
                varParts = value.prettyPrint().splitlines()
                while len(varParts[-1]) == 0:
                    del varParts[-1]
                oidType, sep, value = varParts[-1].strip().partition('=')
                oidKey = value if oidType == 'objectID-value' else str(oid)
                valKey = None if oidType == 'objectID-value' else value
                if oidKey in gOidMap:
                    eventDict[gOidMap[oidKey]] = valKey
                else:
                    eventDict[oidKey] = valKey
            matchActions(eventDict)
    return wholeMsg


def main():
    'main program function'
    if os.path.isfile(CONFIG_FILE):
        filename = CONFIG_FILE
    elif os.path.isfile('/config/{0}'.format(CONFIG_FILE)):
        filename = '/config/{0}'.format(CONFIG_FILE)
    else:
        print 'Error: cannot find configuration file', CONFIG_FILE
        return

    processConfig(filename)

    transportDispatcher = AsynsockDispatcher()

    transportDispatcher.registerRecvCbFun(cbFun)

# UDP/IPv4
    if gArgs.virtual_router:
        lookupVR(gArgs.virtual_router)

    # During startup, the IP address may not be ready yet. So we try a few times
    for retry in range(30):
        try:
            transportDispatcher.registerTransport(
                udp.domainName, udp.UdpSocketTransport().openServerMode((gArgs.ip_address, 162))
            )
            break
        except Exception:
            time.sleep(5)

# UDP/IPv6
    transportDispatcher.registerTransport(
        udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 162))
    )

    transportDispatcher.jobStarted(1)

    try:
        # Dispatcher will never finish as job#1 never reaches zero
        transportDispatcher.runDispatcher()
    except Exception:
        transportDispatcher.closeDispatcher()
        raise


main()
