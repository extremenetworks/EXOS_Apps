.. Cablediag User Guide master file, created by
   sphinx-quickstart on Sun Apr 16 07:48:05 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: ExtremeSwitchingLogo.png
.. image:: XosLogo.png

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Cable Diagnostic On-Switch Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
---------------
Version 1.1.0.3
---------------
- added support for -p PORTLIST command line option

----------------------------
 Minimum ExtremeXOS Required
----------------------------
EXOS 21.1.2

EXOS 22.5
    An EXOS command which invokes the cablediag.py applicaiton has been added to EXOS 22.5.

.. code-block:: bash

    run diagnostics cable ports [ <port_list> | all ]

Files
-----
.. csv-table:: Cable Diagnostic Application Download
    :header: File, Description

    `summitX-cablediag-1.1.0.3.xmod <https://github.com/extremenetworks/EXOS_Apps/blob/master/Cablediags/summitX-cablediag-1.1.0.3.xmod>`_, Summit Cable Diagnostic Application
    `onie-cablediag-1.1.0.3.xmod <https://github.com/extremenetworks/EXOS_Apps/blob/master/Cablediags/onie-cablediag-1.1.0.3.xmod>`_, ONIE Cable Diagnostic Application

Overview
--------
The cablediag.py application performs a Time Domain Reflectometry (TDR) diagnostic on copper switch interfaces.

Download
--------
To update your Extreme EXOS switch with this version of cablediag.py:

#. Using the right mouse button, copy the link of the desired .xmod above
#. On an EXOS Command line enter: ``download url`` *<paste the link from above>*


EXOS Command Line
=================
cablediag.py is managed using the ``run script`` CLI command.

Help
----
To see the cablediag options, enter

.. code-block:: bash

    run script cablediag.py -h

.. code-block:: bash

    usage: cablediag [-h] [-p PORTLIST [PORTLIST ...]] [-d]

    optional arguments:
      -h, --help            show this help message and exit
      -p PORTLIST [PORTLIST ...], --portList PORTLIST [PORTLIST ...]
                            Port list separated by a "," or "-"
      -d, --debug           Enable debug

Default behavior
    Perform a diagnostic on all copper interfaces carrying user data. Copper interfaces used for stacking are not included in the diagnostic.

``--p`` or ``--portList``
    Specify individual port or ports.

    Individual ports may be:

    - a single port
    - multiple ports separated by a comma ','
    - A range of ports specified by a dash '-' between a beginning and ending port.

Running cablediag.py
--------------------
.. code-block:: bash

    run script cablediag.py

Or EXOS 22.5 and later    

.. code-block:: bash

    run diagnostics cable ports all

.. code-block:: bash

    cablediag: 1.1.0.3


    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    +                             C A U T I O N                             +
    +   cablediag will momentarily interfere with traffic on active ports   +
    +-----------------------------------------------------------------------+
    +   Ports: All Ports                                                    +
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Do you want to continue cable diagnostics? [y/N]: y

.. code-block:: bash

    Collecting port cable diagnostic information may take a moment...
    port 1: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 2: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 3: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 4: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    .
    .
    .
    port 24: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    CABLEdiag: ERROR: port 25: Feature unavailable

    CABLEdiag: ERROR: port 26: Feature unavailable

    CABLEdiag: ERROR: port 27: Feature unavailable

    CABLEdiag: ERROR: port 28: Feature unavailable

*In the example above, ports 25-28 are not copper ports used for user data.*

Running cablediag.py with Ports
-------------------------------
.. code-block:: bash

    run script cablediag.py -p 1-4,9-15,40,41

Or EXOS 22.5 and later    

.. code-block:: bash

    run diagnostics cable ports 1-4, 9-15, 40,41

.. code-block:: bash

    cablediag: 1.1.0.3


    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    +                             C A U T I O N                             +
    +   cablediag will momentarily interfere with traffic on active ports   +
    +-----------------------------------------------------------------------+
    +   Ports: 1,2,3,4,9,10,11,12,13,14,15,40,41                            +
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Do you want to continue cable diagnostics? [y/N]: y

.. code-block:: bash

    Collecting port cable diagnostic information may take a moment...
    port 1: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 4 meters
            pair B Ok, length 0 meters
            pair C Ok, length 0 meters
            pair D Ok, length 0 meters

    port 2: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 3: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 4: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 9: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 5 meters
            pair B Crosstalk, length 1 meters
            pair C Ok, length 0 meters
            pair D Crosstalk, length 1 meters

    port 10: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 11: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 4 meters
            pair B Ok, length 0 meters
            pair C Ok, length 0 meters
            pair D Ok, length 5 meters

    port 12: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 13: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 191 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 14: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 10 meters
            pair B Ok, length 5 meters
            pair C Ok, length 9 meters
            pair D Ok, length 10 meters

    port 15: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 40: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 0 meters
            pair B Ok, length 0 meters
            pair C Ok, length 0 meters
            pair D Ok, length 0 meters

    port 41: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 0 meters
            pair B Ok, length 0 meters
            pair C Ok, length 0 meters
            pair D Ok, length 0 meters

Running cablediag.py on a Stack
-------------------------------

.. code-block:: bash

    run script cablediag.py 1:1,1:3,1:9-16,2:1-5,2:13

Or EXOS 22.5 and later    

.. code-block:: bash

    run diagnostics cable ports 1:1,1:3, 1:9-16, 2:1-5,2:13

.. code-block:: bash

    cablediag: 1.1.0.3


    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    +                             C A U T I O N                             +
    +   cablediag will momentarily interfere with traffic on active ports   +
    +-----------------------------------------------------------------------+
    +   Slot 1: Ports: 1,3,9,10,11,12,13,14,15,16                           +
    +   Slot 2: Ports: 1,2,3,4,5,13                                         +
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Do you want to continue cable diagnostics? [y/N]: y

.. code-block:: bash

    Collecting port cable diagnostic information may take a moment...
    Slot 1
    port 1: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 5 meters
            pair B Ok, length 0 meters
            pair C Ok, length 0 meters
            pair D Ok, length 0 meters

    port 3: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 9: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 5 meters
            pair B Crosstalk, length 1 meters
            pair C Ok, length 0 meters
            pair D Crosstalk, length 1 meters

    port 10: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 11: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 4 meters
            pair B Ok, length 5 meters
            pair C Ok, length 4 meters
            pair D Ok, length 4 meters

    port 12: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 13: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 14: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 5 meters
            pair B Ok, length 7 meters
            pair C Ok, length 5 meters
            pair D Ok, length 5 meters

    port 15: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    port 16: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters

    Slot 2
    port 1: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 0 meters
            pair B Ok, length 0 meters
            pair C Ok, length 0 meters
            pair D Ok, length 0 meters
    port 2: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 5 meters
            pair B Ok, length 4 meters
            pair C Ok, length 4 meters
            pair D Ok, length 2 meters
    port 3: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters
    port 4: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters
    port 5: cable (4 pairs, length +/- 10 meters)
            pair A Open, length 0 meters
            pair B Open, length 0 meters
            pair C Open, length 0 meters
            pair D Open, length 0 meters
    port 13: cable (4 pairs, length +/- 10 meters)
            pair A Ok, length 4 meters
            pair B Ok, length 0 meters
            pair C Ok, length 2 meters
            pair D Ok, length 0 meters
