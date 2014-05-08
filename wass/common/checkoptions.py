'''
checkoptions.py

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
#TODO: implement that the -e / --exclude can be defined multiple times
#TODO: implement a function to build the exclude url(s) from standard url(s) to regex

__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.05.06'

import os
import sys
import platform
import argparse
from ConfigParser import SafeConfigParser

usage = '''
Wass - Web Application Security Scan, "black-box" Scanning

Usage:

    ./%(prog)s -c [CustomerName] -t [TargetDomain]

Options:
    -h or --help
        Display this help message

    -c or --customer
        Customer Name.
        Example: -c "My Company .Inc"
        Default: None
        Type: Mandatory

    -P or --program
        Defines what to do.
        Example: -P ALL
        Allowed options: ALL, Arachni, Nikto, Nmap, Fierce, OpenVAS, Skipfish, SSLyze, SSLScan, W3af, Wapiti, WhatWeb, Whois, ZAProxy, Info or Update
        Default: ALL
        Type: Optional

    -t or --target
        This is the target domain to scan.
        Example: -t zero.webappsecurity.com (This is a HP provided test site)
        Default: None
        Type: Mandatory

    -p or --port
        The port of the target application server to run against.
        Example: -p 8443
        Default: 80
        Type: Optional (The Application will try and guess the correct protocol from the port given)

    -u or --url
        The target URL to start the scan at
        Example: -u /Administrator/index.php
        Default: /
        Type: Optional

    -e or --exclude
        URLs to Exclude from the scanning processes, can be defined multiple times
        Example: -e /admin/logout.php -e exit.php
        Type: Optional

    -s or --scheme
        The scheme that the target uses.
        Example: https
        Type: Optional
        Default: http

    --auth-by
        The name of the user that is doing this scan
        Example: --auth-by "John Doe <john.doe@example.com>"
        Default: None

    --auth-user
        The user name to be used during the scan top access restricted areas of the Web Application
        Example: --auth-user test
        Default: None

    --auth-pw
        The user password to be used during the scan top access restricted areas of the Web Application
        Example: --auth-pw test
        Default: None

    --auth-type
        The type of authentication used by the Web Application
        Example: --auth-type basic
        Default: None
        Allowed options: basic, form, digest

    --auth-url
        The authentication URL used to login to the Web Application
        Example: --auth-url /admin/login.php
        Default: None

    --auth-verify-url
        The URL we can access when we are logged in to the Web Application
        Example: --auth-verify-url /admin/my-account.php
        Default: None

    --log
        Log level to use, setting this to debug will print all the logging to the console and the logfile
        Example: --log debug
        Default: info
        Allowed options: info, debug
        Type: Optional

    --version
        Prints the version number
        Example: --version=short
        Allowed options: short (This will only print the version number), long
        Type: Optional

Description:
    This Program will run anyone or all of the locally installed supported programs (see the -P option for a list),
    and E-mail the result in a Zip file to the E-Mail address from the wass.config, the ZIP File will be encrypted.
    If none of the supported Programs are found you will see this message, so make sure that you have those in place,
    and that you have updated the wass.config
'''

parser = argparse.ArgumentParser(usage=usage)
parser.add_argument("-P", "--program", action="store", type=str, dest="program", default="ALL", help='The Program to run e.g.: All')
parser.add_argument("-c", "--customer", action="store", type=str, dest="customer", help='The Customer Name e.g.: "My Company Name"')
parser.add_argument("-t", "--target", action="store", type=str, dest="targetdomain", help="The Target (domain) to Scan e.g.: www.example.com")
parser.add_argument("-p", "--port", action="store", type=int, dest="port", default="80", help="The Target (Port) of the server e.g.: 80, 443, 8080 or 8443")
parser.add_argument("-u", "--url", action="store", type=str, dest="url", default="/", help='The Target (URL) to Scan e.g.: "/Administration/index.php"')
parser.add_argument("-s", "--scheme", action="store", type=str, dest="scheme", default="http", choices=['http', 'https'], help='The scheme that is used by the application e.g.: http (default) or https')
parser.add_argument("-e", "--exclude", action="store", type=str, dest="excludeURL", nargs='+', help="This option expects a plain string of URLs to exclude from the scan processes.")
parser.add_argument("--authed-by", action="store", type=str, dest="authedby", default=None, help="This option is the Name of the user doing this scan.")
parser.add_argument("--auth-user", action="store", type=str, dest="authuser", default=None, help="This option is the User Name to be used for the logins.")
parser.add_argument("--auth-pw", action="store", type=str, dest="authpw", default=None, help="This option is the User password to be used for the logins.")
parser.add_argument("--auth-type", action="store", type=str, dest="authtype", default=None, choices=['basic', 'form', 'digest'], help="This option is the type of authentication used by the site.")
parser.add_argument("--auth-url", action="store", type=str, dest="authurl", default=None, help="What is the authentication URL")
parser.add_argument("--auth-verify-url", action="store", type=str, dest="authverifyurl", default=None, help="What URL Can we only access when we are logged in?")
parser.add_argument("--log", action="store", type=str, dest="loglevel", default="info", choices=['info', 'debug'], help="The Log level to use: info, debug or error")
parser.add_argument("-v", "--version", action="store", type=str, dest="version", help="The version of the program: short or long")
args = parser.parse_args()


class WassCheckOptions(object):
    '''
    This is the WASS CheckOptions class
    '''
    def __init__(self, wass):
        '''
        Initialize CheckOptions module
        '''
        self.wass = wass

    def Usage(self):
        '''
        Print the usage information
        '''
        parser.print_help()

    def CheckOptions(self):
        '''
        Check the Commandline options and get the configuration from the wass.config file
        '''
        if (args.version is not None):
            if(args.version.lower() == "short"):
                print ("%s" % self.wass.ShortVersion)
                return -1
            else:
                print ("%s" % self.wass.LongVersion)
                return -1

        # Getting the Command Line parameters
        if ((args.customer is None) or (args.targetdomain is None)):
            parser.print_help()
            return -1
        else:
            if (platform.system() == "Linux"):
                if os.path.isfile('wass.config'):
                    wassConfig = 'wass.config'
                else:
                    print ("CONFIGURATION FILE NOT FOUND!!! CRITICAL ERROR!!!")
                    return -1
            else:
                print ("You are not running this application on a Linux platform!!!!!!")
                return -1

        self.wass.OrgWorkingDir = os.getcwd()
        self.wass.PythonVersion = sys.version
        self.wass.SystemOS = platform.dist()[0]
        self.wass.OSVersion = platform.dist()[1]
        # Getting the Command Line parameters
        self.wass.Program = args.program
        self.wass.Customer = args.customer
        self.wass.TargetDomain = args.targetdomain
        self.wass.TargetPort = args.port
        self.wass.TargetURL = args.url
        self.wass.TargetScheme = args.scheme
        self.wass.WASSArguments = str(sys.argv)
        if ((args.excludeURL is not None) or (args.excludeURL != '')):
            self.wass.TargetExcludeURLS = args.excludeURL
        if (args.authuser is not None):
            self.wass.AuthUser = args.authuser
        if (args.authpw is not None):
            self.wass.AuthPW = args.authpw
        if (args.authtype is not None):
            self.wass.AuthType = args.authtype
        if (args.authurl is not None):
            self.wass.AuthURL = args.authurl
        if (args.authverifyurl is not None):
            self.wass.AuthVerifyURL = args.AuthVerifyURL
        self.wass.LogLevel = args.loglevel

        # Getting the configuration from the wass.config file
        confParser = SafeConfigParser()
        confParser.read(wassConfig)
        # Get the general configurations from config file
        if (args.authedby is not None):
            self.wass.AuthedBy = args.authedby
        elif (confParser.get("General", "authed-by") != ''):
            self.wass.AuthedBy = confParser.get("General", "authed-by")
        else:
            print ("The authby parameter is missing from both the wass.config and the command line exitting!!!!!!!!")
            return -1
        if (confParser.get("General", "resultDir") != ""):
            self.wass.ResultDir = confParser.get("General", "resultDir")
        else:
            self.wass.ResultDir = self.wass.OrgWorkingDir
        self.wass.ToEmail = confParser.get("General", "emailTo")
        self.wass.FromEmail = confParser.get("General", "emailFrom")
        if (confParser.get("General", "sendEmail") == 'False'):
            self.wass.SendEmail = False
        self.wass.ZIPPassword = confParser.get("General", "password")
        if (confParser.get("General", "proxyprotocol") != '' and confParser.get("General", "proxyhost") != '' and confParser.get("General", "proxyport") != ''):
            self.wass.LocalZAProxyProtocol = confParser.get("General", "proxyprotocol")
            if (confParser.get("General", "proxyhost") == 'localhost'):
                self.wass.LocalZAProxyHost = '127.0.0.1'
            else:
                self.wass.LocalZAProxyHost = confParser.get("General", "proxyhost")
            self.wass.LocalZAProxyPort = confParser.get("General", "proxyport")
        self.wass.LocalZAProxy = self.wass.LocalZAProxyProtocol + "://" + self.wass.LocalZAProxyHost + ":" + self.wass.LocalZAProxyPort
        self.wass.UseLocalZAProxy = confParser.get("General", "use_proxy")
        # Get the Arachni configurations from config file
        if (os.path.isfile(confParser.get("Arachni", "cmd"))):
            self.wass.ArachniCMD = confParser.get("Arachni", "cmd")
            self.wass.ArachniArguments = confParser.get("Arachni", "arguments")
            self.wass.WassCheckArguments.checkArachniArguments
            self.wass.RunArachni = True
        # Get the Fierce configurations from config file
        if (os.path.isfile(confParser.get("Fierce", "cmd"))):
            self.wass.FierceCMD = confParser.get("Fierce", "cmd")
            self.wass.FierceArguments = confParser.get("Fierce", "arguments")
            self.wass.WassCheckArguments.checkFierceArguments
            self.wass.RunFierce = True
        # Get the Nikto configurations from config file
        if (os.path.isfile(confParser.get("Nikto", "cmd"))):
            self.wass.NiktoCMD = confParser.get("Nikto", "cmd")
            self.wass.NiktoArguments = confParser.get("Nikto", "arguments")
            self.wass.WassCheckArguments.checkNiktoArguments
            self.wass.RunNikto = True
        # Get the Nmap configurations from config file
        if (os.path.isfile(confParser.get("Nmap", "cmd"))):
            self.wass.NmapCMD = confParser.get("Nmap", "cmd")
            if (confParser.get("Nmap", "port") != ''):
                self.wass.NmapPort = confParser.get("Nmap", "port")
            self.wass.NmapArguments = confParser.get("Nmap", "arguments")
            self.wass.WassCheckArguments.checkNmapArguments
            self.wass.RunNmap = True
        # Get the Skipfish configurations from config file
        if (os.path.isfile(confParser.get("Skipfish", "cmd"))):
            self.wass.SkipfishCMD = confParser.get("Skipfish", "cmd")
            self.wass.SkipfishArguments = confParser.get("Skipfish", "arguments")
            self.wass.SkipfishWordList = confParser.get("Skipfish", "skipfishwordlist")
            self.wass.WassCheckArguments.checkSkipfishArguments
            self.wass.RunSkipfish = True
        # Get the SSLyze configurations from config file
        if (os.path.isfile(confParser.get("SSLyze", "cmd"))):
            self.wass.SSLyzeCMD = confParser.get("SSLyze", "cmd")
            self.wass.SSLyzeArguments = confParser.get("SSLyze", "arguments")
            self.wass.WassCheckArguments.checkSSLyzeArguments
            self.wass.RunSSLyze = True
        # Get the SSLScan configurations from config file
        if (os.path.isfile(confParser.get("SSLScan", "cmd"))):
            self.wass.SSLScanCMD = confParser.get("SSLScan", "cmd")
            self.wass.SSLScanArguments = confParser.get("SSLScan", "arguments")
            self.wass.WassCheckArguments.checkSSLScanArguments
            self.wass.RunSSLScan = True
        # Get the TheHarvester configurations from config file
        if (os.path.isfile(confParser.get("TheHarvester", "cmd"))):
            self.wass.TheHarvesterCMD = confParser.get("TheHarvester", "cmd")
            self.wass.TheHarvesterArguments = confParser.get("TheHarvester", "arguments")
            self.wass.WassCheckArguments.checkTheHarvesterArguments
            self.wass.RunTheHarvester = True
        # Get the W3af configurations from config file
        if (os.path.isfile(confParser.get("W3af", "cmd"))):
            self.wass.W3afCMD = confParser.get("W3af", "cmd")
            if (confParser.get("W3af", "profile") == 'Default'):
                if (os.path.isfile(self.wass.OrgWorkingDir + '/wass/config/OWASP_TOP10.pw3af')):
                    self.wass.W3afProfile = self.wass.OrgWorkingDir + '/wass/config/OWASP_TOP10.pw3af'
                    self.wass.RunW3af = True
                else:
                    self.wass.RunW3af = False
            elif (confParser.get("W3af", "profile") == 'OWASP_TOP10.pw3af'):
                if (os.path.isfile(self.wass.OrgWorkingDir + '/wasslib/OWASP_TOP10.pw3af')):
                    self.wass.W3afProfile = self.wass.OrgWorkingDir + '/wass/config/OWASP_TOP10.pw3af'
                    self.wass.RunW3af = True
                else:
                    self.wass.RunW3af = False
            elif (confParser.get("W3af", "profile") == 'WASS_1.6_Profile.pw3af'):
                if (os.path.isfile(self.wass.OrgWorkingDir + '/wass/config/WASS_1.6_Profile.pw3af')):
                    self.wass.W3afProfile = self.wass.OrgWorkingDir + '/wass/config/WASS_1.6_Profile.pw3af'
                    self.wass.RunW3af = True
                else:
                    self.wass.RunW3af = False
            elif (confParser.get("W3af", "profile") != ''):
                self.wass.W3afProfile = confParser.get("W3af", "profile")
                self.wass.RunW3af = True
            else:
                self.wass.RunW3af = False
        # Get the Wapiti configurations from config file
        if (os.path.isfile(confParser.get("Wapiti", "cmd"))):
            self.wass.WapitiCMD = confParser.get("Wapiti", "cmd")
            self.wass.WapitiArguments = confParser.get("Wapiti", "arguments")
            self.wass.WassCheckArguments.checkWapitiArguments
            self.wass.RunWapiti = True
        # Get the WhatWeb configurations from config file
        if (os.path.isfile(confParser.get("WhatWeb", "cmd"))):
            self.wass.WhatWebCMD = confParser.get("WhatWeb", "cmd")
            self.wass.WhatWebArguments = confParser.get("WhatWeb", "arguments")
            self.wass.WassCheckArguments.checkWhatWebArguments
            self.wass.RunWhatWeb = True
        # Get the Whhois configurations from config file
        if (os.path.isfile(confParser.get("Whois", "cmd"))):
            self.wass.WhoisCMD = confParser.get("Whois", "cmd")
            self.wass.RunWhois = True
        # Get the OpenVAS configurations from config file
        if (os.path.isfile(confParser.get("OpenVAS", "cmd"))):
            self.wass.RunOpenVAS = True
            self.wass.OpenVASUser = confParser.get("OpenVAS", "username")
            self.wass.OpenVASPassword = confParser.get("OpenVAS", "password")
            self.wass.OpenVASHost = confParser.get("OpenVAS", "host")
            self.wass.OpenVASCMD = confParser.get("OpenVAS", "cmd") + ' -h ' + self.wass.OpenVASHost + ' -u ' + self.wass.OpenVASUser + ' -w ' + self.wass.OpenVASPassword
            self.wass.OpenVASPortListID = confParser.get("OpenVAS", "port_list")
            self.wass.OpenVASScanConfig = confParser.get("OpenVAS", "scan_config")
        # Get the ZAProxy configurations from config file
        if (os.path.isdir(confParser.get("ZAPProxy", "path"))):
            self.wass.ZAProxyPath = confParser.get("ZAPProxy", "path")
            if (not self.wass.ZAProxyPath.endswith('/')):
                self.wass.ZAProxyPath = self.wass.ZAProxyPath + "/"
            self.wass.ZAProxyCMD = self.wass.ZAProxyPath + confParser.get("ZAPProxy", "cmd")
            self.wass.RunZAProxy = True
            self.wass.ZAProxyCLI = self.wass.ZAProxyCMD + " -daemon"
            self.wass.ZAProxyDaemon = confParser.get("ZAPProxy", "daemon")
            self.wass.ZAProxyAttackStrength = confParser.get("ZAPProxy", "attackStrength")
            self.wass.ZAProxyAlertThreshold = confParser.get("ZAPProxy", "alertThreshold")
            self.wass.ZAProxyStart = confParser.get("ZAPProxy", "start")
            self.wass.ZAProxyStop = confParser.get("ZAPProxy", "stop")

        listOfFoundPrograms = []
        if (self.wass.RunArachni):
            listOfFoundPrograms.append('Arachni')
        if (self.wass.RunFierce):
            listOfFoundPrograms.append('Fierce')
        if (self.wass.RunNikto):
            listOfFoundPrograms.append('Nikto')
        if (self.wass.RunNmap):
            listOfFoundPrograms.append('Nmap')
        if (self.wass.RunOpenVAS):
            listOfFoundPrograms.append('OpenVAS')
        if (self.wass.RunSkipfish):
            listOfFoundPrograms.append('Skipfish')
        if (self.wass.RunSSLyze):
            listOfFoundPrograms.append('SSLyze')
        if (self.wass.RunSSLScan):
            listOfFoundPrograms.append('SSLScan')
        if (self.wass.RunTheHarvester):
            listOfFoundPrograms.append('TheHarvester')
        if (self.wass.RunW3af):
            listOfFoundPrograms.append('W3af')
        if (self.wass.RunWapiti):
            listOfFoundPrograms.append('Wapiti')
        if (self.wass.RunWhatWeb):
            listOfFoundPrograms.append('WhatWeb')
        if (self.wass.RunWhois):
            listOfFoundPrograms.append('Whois')
        if (self.wass.RunZAProxy):
            listOfFoundPrograms.append('ZAProxy')

        if (len(listOfFoundPrograms) > 0):
            if (self.wass.LogLevel.upper() == "DEBUG"):
                print ("WASS Found the following installed software: %s" % listOfFoundPrograms)
        else:
            if (self.wass.LogLevel.upper() == "DEBUG"):
                print ("WASS Found the following installed software: %s" % listOfFoundPrograms)
            self.Usage()
