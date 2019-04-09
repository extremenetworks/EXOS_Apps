# EXOS ezvxlan.py Application
## User Documentation
[EZ_VXLAN](https://rawgit.com/extremenetworks/EXOS_Apps/master/EZ_VXLAN/docs/ezvxlan.html)

## ezvxlan.py 2.0.0.3

Already included with EXOS 22.3

For Extreme customers deploying a virutal network using VXLAN, this application provides an automatic mapping of certain VLANS into VXLAN VNIs when used with the EXOS virtual-network capability available on:
- X670-G2
- X770
- X690
- X870

This application works best when combined with Extreme Management Center. http://www.extremenetworks.com/product/management-center/


## Requirements
- ExtremeXOS 21.1.1.4 or later
- ExtremeSwitch X670-G2
- ExtremeSwitch X770
- ExtremeSwitch X690

## Updates in 2.0.0.3
- Interoperates with Extreme Fabric
    - start --fabric
- Automatic L2 VXLAN for all VLANS
    - start --allvlans

## Application Highlights:
- See User Documentation for details

## Download
EXOS offers a variety of download methods. All of the methods below assume the EXOS switch has been configured with an IP address either on the `mgmt` VLAN (for the management port) or `default` VLAN (for the front panel ports).
### Download over tftp
To download summitX-ezvxlan-1.0.0.6.xmod to an EXOS switch running ExtremeXOS 21.1 or later, place the file in a server tftp directory.

#### Download tftp over management port
Enter the EXOS CLI command:
- download image _serverIP_ summitX-ezvxlan-2.0.0.3.xmod

E.g.
`download image 10.10.10.1 summitX-ezvxlan-2.0.0.3.xmod`

#### Download tftp over front panel port
Enter the EXOS CLI command:
- download image _serverIP_ summitX-ezvxlan-2.0.0.3.xmod vr VR-Default

E.g.
`download image 10.10.10.1 summitX-ezvxlan-2.0.0.3.xmod vr VR-Default`

### Download over http
EXOS can download files from a web site using http. 
If your server does not have a web server and Python is installed, Python offers a simple HTTP web server. [Python Simple Web Server](https://docs.python.org/2/library/simplehttpserver.html)

Example starting a simple python web server on port 8000
```
cd <directory>
python -m SimpleHTTPServer 8000
```
Copy summitX-ezvxlan-2.0.0.3.xmod to _directory_ used in the example above.
#### Download http over management port
Enter the EXOS CLI command:
- download url http://_serverIP_/summitX-ezvxlan-2.0.0.3.xmod

E.g. `download url http://10.10.10.1/summitX-ezvxlan-2.0.0.3.xmod`

#### Download http over front panel port
Enter the EXOS CLI command:
- download url http://_serverIP_/summitX-ezvxlan-2.0.0.3.xmod vr VR-Default

E.g. `download url http://10.10.10.1/summitX-ezvxlan-2.0.0.3.xmod vr VR-Default`

### Download using EXOS web (Chalet)
- Using your browser, download summitX-ezvxlan-2.0.0.3.xmod from github to your PC. 
- Then using the EXOS web interface (Chalet), navigate to Apps->File Manager.
- Use: `Upload files from Local Drive:` to upload and install the file to the EXOS switch

## License
Copyright© 2016, Extreme Networks
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support
The software is provided as is and Extreme Networks has no obligation to provide
maintenance, support, updates, enhancements or modifications.
Any support provided by Extreme Networks is at its sole discretion.

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).

>Be Extreme
