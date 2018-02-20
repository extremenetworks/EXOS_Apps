# ******************************************************
#  Copyright (c) Extreme Networks Inc. 2018
#  All rights reserved
# ******************************************************
'''
This autoexec.py script will start diagnostics at startup.
Once diagnostic complete, detect if reboot is returning from
diags and do not start them again
'''
from os import remove
from os.path import isfile, splitext, basename
from sys import stderr
import subprocess

# Determine our running context by which import is available
try:
    import exsh
    i_am_script = True
except Exception:
    i_am_script = False


# **********************************************************************
# C O N S T A N T S
# **********************************************************************
PROCESS_NAME = splitext(basename(__file__))[0]


# **********************************************************************
# This class is invoked in the expy context via the EXOS CLI: create process
# **********************************************************************
class ExpyAutoexec(object):
    def __call__(self):
        # create an empty file to mark we are starting diags
        p = subprocess.Popen(
                ['/exos/bin/exsh', '-n', '0'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
        print >> p.stdin, 'run diagnostics normal'
        print >> p.stdin, 'y'


# **********************************************************************
# This class is invoked from autoexec.py
# **********************************************************************
class Autoexec(object):
    def __call__(self):
        DIAG_LOCK = '/usr/local/cfg/diag.lock'
        if isfile(DIAG_LOCK):
            # returning from a diagnostics reboot
            remove(DIAG_LOCK)
            return

        # create an EXOS process that starts diagnostics
        print >> stderr, "\nStarting Diagnostics\n"
        with open(DIAG_LOCK, 'w'):
            pass
        # create the EXOS expy backend process
        exsh.clicmd('create process {0} python-module {0} start on-demand'.format(PROCESS_NAME))

        slot_clause = ''
        exsh.clicmd('start process {0} {1}'.format(PROCESS_NAME, slot_clause))


# **********************************************************************
# Determine the run time context and invoke the proper class
# **********************************************************************
if __name__ == '__main__':
    if i_am_script is True:
        # started from autoexec.py
        autoexec = Autoexec()
        autoexec()
    else:
        # Script was started as EXOS process
        expy_autoexec = ExpyAutoexec()
        expy_autoexec()
