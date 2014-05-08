#!/usr/bin/env python
'''
Wass.py

Copyright 2014 Tom Stage

Wass is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

Wass is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Wass; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''

import sys
import os
from wass import WASS

currentDir = os.getcwd()


def backToCurrentDir():
    os.chdir(currentDir)


def main():
    """
    This is the main execution block of WASS
    """
    # Check that we have the needed Options declared on the command line
    errCode = objWASS.WassCheckOptions.CheckOptions()
    if (errCode is not None):
        return errCode

    if (objWASS.Program == "ALL"):
        # 1st we run the information gathering programs
        objWASS.WassWhois.RunWhoIS()
        objWASS.WassNmap.RunNmap()
        objWASS.WassFierce.RunFierce()
        objWASS.WassWhatWeb.RunWhatWeb()
        objWASS.WassSSLyze.RunSSLyze()
        objWASS.WassSSLScan.RunSSLScan()
        objWASS.WassTheHarvester.RunTheHarvester()
        # 2nd we run the Web Application scanners
        objWASS.WassArachni.RunArachni()
        objWASS.WassNikto.RunNikto()
        #objWASS.WassOpenVAS.RunOpenVAS()
        objWASS.WassW3af.RunW3af()
        objWASS.WassWapiti.RunWapiti()
        objWASS.WassSkipfish.RunSkipfish()
        objWASS.WassZAProxy.RunZAProxy()
        # 3rd we run the Brute force software
        # 4th we create the report with data from all the scans
    elif (objWASS.Program == "Arachni"):
        objWASS.WassArachni.RunArachni()
    elif (objWASS.Program == "Fierce"):
        objWASS.WassFierce.RunFierce()
    elif (objWASS.Program == "Nikto"):
        objWASS.WassNikto.RunNikto()
    elif (objWASS.Program == "Nmap"):
        objWASS.WassNmap.RunNmap()
    elif (objWASS.Program == "Skipfish"):
        objWASS.WassSkipfish.RunSkipfish()
    elif (objWASS.Program == "SSLyze"):
        objWASS.WassSSLyze.RunSSLyze()
    elif (objWASS.Program == "SSLScan"):
        objWASS.WassSSLScan.RunSSLScan()
    elif (objWASS.Program == "TheHarvester"):
        objWASS.WassTheHarvester.RunTheHarvester()
    elif (objWASS.Program == "W3af"):
        objWASS.WassW3af.RunW3af()
    elif (objWASS.Program == "Wapiti"):
        objWASS.WassWapiti.RunWapiti()
    elif (objWASS.Program == "WhatWeb"):
        objWASS.WassWhatWeb.RunWhatWeb()
    elif (objWASS.Program == "Whois"):
        objWASS.WassWhois.RunWhoIS()
    elif (objWASS.Program == "OpenVAS"):
        #objWASS.WassOpenVAS.RunOpenVAS()
        pass
    elif (objWASS.Program == "ZAProxy"):
        objWASS.WassZAProxy.RunZAProxy()
    elif (objWASS.Program == "Info"):
        objWASS.WassWhois.RunWhoIS()
        objWASS.WassNmap.RunNmap()
        objWASS.WassFierce.RunFierce()
        objWASS.WassWhatWeb.RunWhatWeb()
        objWASS.WassSSLyze.RunSSLyze()
        objWASS.WassSSLScan.RunSSLScan()
        objWASS.WassTheHarvester.RunTheHarvester()
    elif (objWASS.Program == "Update"):
        objWASS.WassNikto.NiktoUpdate()
        objWASS.WassNikto.NmapUpdate()

    return errCode

if __name__ == '__main__':
    errCode = None
    objWASS = WASS()
    errCode = main()
    backToCurrentDir()
    sys.exit(errCode)
