# X870 ZTP update fix
The X870 ships from the factory with EXOS 22.2.0.30. This version has a problem when trying to perform ZTP+ with Extreme Management Center (EMC).

Unfortunately, the X870 requires a manual software upgrade before it will properly connect to EMC.

These files are available to make the manual upgrade process as painless as possible.

## Requirements
- X870 connected to a network that has internet access
- X870 has an IP address (either DHCP or manually configured)

## To Upgrade
### Upgrade by Management port
```
config dns-client add name-server 8.8.8.8 vr VR-Mgmt
download url https://github.com/extremenetworks/EXOS_Apps/blob/master/X870/onie-22.2.1.5.lst
```
### Upgrade by front panel port
```
config dns-client add name-server 8.8.8.8
download url https://github.com/extremenetworks/EXOS_Apps/blob/master/X870/onie-22.2.1.5.lst vr VR-Default
```

### What you should see
```
* (Software Update Required) X870-96x-8c.1 # download url https://github.com/extremenetworks/EXOS_Apps/blob/master/X870/onie-22.2.1.5.lst
Downloading https://github.com/extremenetworks/EXOS_Apps/blob/master/X870/onie-22.2.1.5.xos

Downloading to Switch.......................................................................................
Installing to primary partition!

Installing to Switch.........................................
Image installed successfully
This image will be used only after rebooting the switch!
Downloading https://github.com/extremenetworks/EXOS_Apps/blob/master/X870/onie-22.2.1.5-diagnostics.xmod

Downloading to Switch.....................................
Installing to primary partition!

Installing to Switch...
Image installed successfully
Downloading https://github.com/extremenetworks/EXOS_Apps/blob/master/X870/onie-cloud_connector-1.1.14.35.xmod

Downloading to Switch
Installing to primary partition!

Installing to Switch
Image installed successfully
* (Software Update Required) X870-96x-8c.2 #
```