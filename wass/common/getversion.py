'''
getversions.py

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
#
#TODO: Extract version from OpenVAS

__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.04.27'

import subprocess as sub
import re
import os


class WassGetVersion(object):
    '''
    This is the WassGetVersions class
    '''
    def __init__(self, wass):
        '''
        Initialize WassGetVersions module
        '''
        self.wass = wass

    def _runCommand(self, runCMD):
        '''
        Use sub.Popen to run the command runCMD

        :returns: string containing the output from the command that was run
        '''
        command_Responce = ''
        p = sub.Popen(runCMD, bufsize=-1, shell=True, stdout=sub.PIPE, stderr=sub.STDOUT)
        command_Responce = bytes.decode(p.communicate()[0])  # store stdout
        #if (self.wass.LogLevel.upper() == "DEBUG"):
        #    print ("GetVersion ran this Command: %s" % runCMD)
        #    print ("GetVersion command_Responce is: %s" % command_Responce)
        return command_Responce

    def _GetArachniVersion(self):
        '''
        Get Arachni Version

        This will run the arachni --version command and look for the Version number in the responce.
        Responce example:
        Arachni - Web Application Security Scanner Framework v0.4.6
           Author: Tasos "Zapotek" Laskos <tasos.laskos@gmail.com>

                   (With the support of the community and the Arachni Team.)

           Website:       http://arachni-scanner.com
           Documentation: http://arachni-scanner.com/wiki


        Arachni 0.4.6 (ruby 1.9.3p448) [x86_64-linux]

        sets the  the self.wass.ArachniVersion
        '''
        arachni_detected_version = None
        # SED Way to get the version number
        #arachni_version_cmd = self.wass.ArachniCMD + ' --version | head -1 | sed -e"s/Arachni - Web Application Security Scanner Framework v//""'
        arachni_version_cmd = self.wass.ArachniCMD + ' --version'
        arachni_detected_version = self._runCommand(arachni_version_cmd)

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('Arachni - Web Application Security Scanner Framework v[0-9]*\.[0-9]*\.[0-9]')

        for line in arachni_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]\.[0-9]')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.ArchniVersion = str(line[rv.start():rv.end()])

                break

    def _GetFierceVersion(self):
        '''
        Get Fierce Version

        This will run the fierce -version command and look for the Version number in the responce.
        Responce example:
        fierce Version 2.0-r420

        sets the  the self.wass.FierceVersion
        '''
        fierce_detected_version = None
        fierce_version_cmd = self.wass.FierceCMD + ' -version'
        fierce_detected_version = self._runCommand(fierce_version_cmd)

        # regex used to detect nmap
        # regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('fierce Version [0-9]*\.[0-9].*')

        for line in fierce_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.FierceVersion = str(line[rv.start():rv.end()])

                break

    def _GetNiktoVersion(self):
        '''
        Get Nikto Version

        This will run the nikto command and look for the Version number in the responce.
        Responce example:
        - Nikto v2.1.5
        ---------------------------------------------------------------------------
        + ERROR: No host specified

        [List of options]

        sets the  the self.wass.NiktoVersion
        '''
        nikto_detected_version = None
        # SED Way to get the version number
        #nikto_version_cmd = self.wass.NiktoCMD + ' | head -1 | sed -e"s/- Nikto v//"'

        nikto_version_cmd = self.wass.NiktoCMD + ' | head -1 | sed -e"s/- Nikto v//"'
        nikto_detected_version = self._runCommand(nikto_version_cmd)

        #self.wass.NiktoVersion = nikto_detected_version

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('- Nikto v[0-9]*\.[0-9]*\.[0-9]')

        for line in nikto_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]\.[0-9]')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.NiktoVersion = str(line[rv.start():rv.end()])

                break

    def _GetOpenVASVersion(self):
        '''
        Get OpenVAS Version

        This will run the each of the OpenVAS commands and look for the Version number in the responce.

        sets the  the self.wass.OpenVASVersion
        '''
        # Start Current default version is OpenVAS-6
        ver = '6'
        scanner_major='3'
        scanner_minor = '4'
        manager_major = '4'
        manager_minor = '0'
        administrator_major = '1'
        administrator_minor = '3'
        gsa_major = '4'
        gsa_minor = '0'
        cli_major = '1'
        cli_minor = '2'
        # Stop Current default version is OpenVAS-6

        detected_openvassd_version = None
        detected_openvasmd_version = None
        detected_openvasad_version = None
        detected_gsad_version = None
        detected_omp_version = None
        detected_openvassd_host = None
        detected_openvassd_port = None
        detected_openvasmd_host = None
        detected_openvasmd_port = None
        detected_openvasad_host = None
        detected_openvasad_port = None
        detected_gsad_host = None
        detected_gsad_port = None

        openvassd_version_cmd = 'openvassd --version | head -1 | sed -e"s/OpenVAS Scanner //"'
        openvasmd_version_cmd = 'openvasmd --version | head -1 | sed -e"s/OpenVAS Manager //"'
        openvasad_version_cmd = 'openvasad --version | head -1 | sed -e"s/OpenVAS Administrator //"'
        gsad_version_cmd = 'gsad --version | head -1 | sed -e"s/Greenbone Security Assistant //"'
        omp_version_cmd = 'omp --version | head -1 | sed -e"s/OMP Command Line Interface //"'
        openvassd_host_cmd = "netstat -A inet -ntlp 2> /dev/null | grep openvassd | awk -F\  '{print $4}' | awk -F: '{print $1}'"
        openvassd_port_cmd = "netstat -A inet -ntlp 2> /dev/null | grep openvassd | awk -F\  '{print $4}' | awk -F: '{print $2}'"
        openvasmd_host_cmd = "netstat -A inet -ntlp 2> /dev/null | grep openvasmd | awk -F\  '{print $4}' | awk -F: '{print $1}'"
        openvasmd_port_cmd = "netstat -A inet -ntlp 2> /dev/null | grep openvasmd | awk -F\  '{print $4}' | awk -F: '{print $2}'"
        openvasad_host_cmd = "netstat -A inet -ntlp 2> /dev/null | grep openvasad | awk -F\  '{print $4}' | awk -F: '{print $1}'"
        openvasad_port_cmd = "netstat -A inet -ntlp 2> /dev/null | grep openvasad | awk -F\  '{print $4}' | awk -F: '{print $2}'"
        gsad_host_cmd = "netstat -A inet -ntlp 2> /dev/null | grep gsad | awk -F\  '{print $4}' | awk -F: '{print $1}'"
        gsad_port_cmd = "netstat -A inet -ntlp 2> /dev/null | grep gsad | awk -F\  '{print $4}' | awk -F: '{print $2}'"

    def _GetSkipfishVersion(self):
        '''
        Get Skipfish Version

        This will run the skipfish -h command and look for the Version number in the responce.
        Responce example:
        skipfish version 2.09b by <lcamtuf@google.com>
        Usage: skipfish [ options ... ] -W wordlist -o output_dir start_url [ start_url2 ... ]

        [List of options]

        sets the  the self.wass.SkipfishVersion
        '''
        skipfish_detected_version = None

        # SED Way to get the version number
        #skipfish_version_cmd = self.wass.SkipfishCMD + ' -h | head -1 | sed -e"s/skipfish version //" | sed -e"s/ by <lcamtuf@google.com>//"'

        skipfish_version_cmd = self.wass.SkipfishCMD + ' -h'
        skipfish_detected_version = self._runCommand(skipfish_version_cmd)

        #self.wass.SkipfishVersion = skipfish_detected_version

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('skipfish version [0-9]*\.[0-9]*[^ ]* by \<lcamtuf@google.com\>')

        for line in skipfish_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]\w+')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.SkipfishVersion = str(line[rv.start():rv.end()])

                break

        # If we get here and the SkipfishVersion is not set we look Version string from 2.10b instead for the 1 from 2.09b
        if (self.wass.SkipfishVersion == None):
            # regex used to detect nmap
            #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
            regex = re.compile('skipfish web application scanner - version [0-9]*\.[0-9]*[^ ]*')

            for line in skipfish_detected_version.split('\n'):
                if regex.match(line) is not None:
                    # Search for version number
                    regex_version = re.compile('[0-9]\.[0-9]\w+')

                    rv = regex_version.search(line)

                    if rv is not None:
                        # extract version/subversion
                        self.wass.SkipfishVersion = str(line[rv.start():rv.end()])

                    break

    def _GetSSLyzeVersion(self):
        '''
        Get SSLyze Version

        Responce example:



         REGISTERING AVAILABLE PLUGINS
         -----------------------------

          PluginSessionResumption
          PluginHSTS
          PluginCompression
          PluginHeartbleed
          PluginCertInfo
          PluginSessionRenegotiation
          PluginOpenSSLCipherSuites



        SSLyze v0.9


        sets the the self.wass.SSLyzeVersion
        '''
        sslyze_detected_version = None
        sslyze_version_cmd = self.wass.SSLyzeCMD + ' --version'
        sslyze_detected_version = self._runCommand(sslyze_version_cmd)

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('SSLyze v[0-9]*\.[0-9]')

        for line in sslyze_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.SSLyzeVersion = str(line[rv.start():rv.end()])

                break

    def _GetSSLScanVersion(self):
        '''
        Get SSLScan Version

        Responce example:
        sslscan version 1.8.0
        http://www.titania.co.uk
        Copyright (C) Ian Ventura-Whiting 2009

        sets the the self.wass.SSLScanVersion
        '''
        sslscan_detected_version = None
        sslscan_version_cmd = self.wass.SSLScanCMD + ' --version'
        sslscan_detected_version = self._runCommand(sslscan_version_cmd)

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('.[34msslscan version [0-9]*\.[0-9]*\.[0-9]')

        for line in sslscan_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]\.[0-9]')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.SSLScanVersion = str(line[rv.start():rv.end()])

                break

    def _GetTheHarvesterVersion(self):
        '''
        Get TheHarvester Version

        Responce example:
        *******************************************************************
        *                                                                 *
        * | |_| |__   ___    /\  /\__ _ _ ____   _____  ___| |_ ___ _ __  *
        * | __| '_ \ / _ \  / /_/ / _` | '__\ \ / / _ \/ __| __/ _ \ '__| *
        * | |_| | | |  __/ / __  / (_| | |   \ V /  __/\__ \ ||  __/ |    *
        *  \__|_| |_|\___| \/ /_/ \__,_|_|    \_/ \___||___/\__\___|_|    *
        *                                                                 *
        * TheHarvester Ver. 2.2a                                          *
        * Coded by Christian Martorella                                   *
        * Edge-Security Research                                          *
        * cmartorella@edge-security.com                                   *
        *******************************************************************


        Usage: theharvester options
        [LIST OF OPTIONS]

        sets the the self.wass.TheHarvesterVersion
        '''
        theharvester_detected_version = None
        theharvester_detected_version = self._runCommand(self.wass.TheHarvesterCMD)

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('\* TheHarvester Ver\. [0-9]*\.[0-9]\w.*\*')

        for line in theharvester_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]\w')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.TheHarvesterVersion = str(line[rv.start():rv.end()])

                break

    def _GetW3afVersion(self):
        '''
        Get W3af Version

        This will get the W3af version from either:
        w3af 1.6 (/path/to/w3af/w3af/core/data/constants/version.txt)
        w3af 1.1 (/usr/share/w3af/core/controllers/misc/get_w3af_version.py) (Default installation directory on CentOS with Atomicorp repo)

        sets the  the self.wass.W3afVersion
        '''
        w3af_detected_version = None
        if (os.path.isfile(os.path.expanduser('~') + '/.w3af/startup.conf')):
            w3af_installation_path, w3af_command = os.path.split(self.wass.W3afCMD)
            if (self.wass.LogLevel.upper() == "DEBUG"):
                print ("The W3af command path is: %s " % w3af_installation_path)
            if (os.path.isdir(w3af_installation_path + '/w3af/core/data/constants/')):
                if (os.path.isfile(w3af_installation_path + '/w3af/core/data/constants/version.txt')):
                    w3af_version_file = open(w3af_installation_path + '/w3af/core/data/constants/version.txt')
                    for line in w3af_version_file:
                        if (line.rstrip() != ''):
                            w3af_detected_version = line.rstrip()
            elif (os.path.isfile('/usr/share/w3af/core/controllers/misc/get_w3af_version.py')):
                for line in '/usr/share/w3af/core/controllers/misc/get_w3af_version.py':
                    if (line == "'Version: 1.1\n'"):
                        w3af_detected_version = '1.1'
        else:
            if (self.wass.LogLevel.upper() == "DEBUG"):
                print ("You need to run the w3af_console or w3af_gui command at least once before using this software.")
                print ("This needs to be done so that you can accept the user licens")
        self.wass.W3afVersion = w3af_detected_version

    def _GetWapitiVersion(self):
        '''
        Get Wapiti Version

        This will run the wapiti command and look for the Version number in the responce.
        Responce example:
        Wapiti-2.3.0 (wapiti.sourceforge.net)
        Wapiti-2.3.0 - Web application vulnerability scanner

         Usage: python wapiti.py http://server.com/base/url/ [options]

         Supported options are:
        [List of options]

        sets the  the self.wass.WapitiVersion
        '''
        wapiti_detected_version = None
        # SED Way to get the version number
        #wapiti_version_cmd = self.wass.WapitiCMD + ' | head -1 | sed -e"s/Wapiti-//" | sed -e"s/ (wapiti.sourceforge.net)//"'
        wapiti_detected_version = self._runCommand(self.wass.WapitiCMD)

        #self.wass.WapitiVersion = wapiti_detected_version

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('Wapiti-[0-9]*\.[0-9]*[^ ]* \(wapiti.sourceforge.net\)')

        for line in wapiti_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]\.[0-9]+')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.WapitiVersion = str(line[rv.start():rv.end()])

                break

    def _GetWhatWebVersion(self):
        '''
        Get WhatWeb Version

        sets the  the self.wass.WhatWebVersion
        '''
        whatweb_detected_version = None
        whatweb_version_cmd = self.wass.WhatWebCMD + ' --version'
        whatweb_detected_version = self._runCommand(whatweb_version_cmd)

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('WhatWeb version [0-9]*\.[0-9]*\.[0-9] \( http://.* \)')

        for line in whatweb_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]\.[0-9]')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.WhatWebVersion = str(line[rv.start():rv.end()])

                break

    def _GetWhoisVersion(self):
        '''
        Get Whois Version

        Responce example:
        jwhois version 4.0, Copyright (C) 1999-2007  Free Software Foundation, Inc.

        sets the the self.wass.WhoisVersion
        '''
        whois_detected_version = None
        whois_version_cmd = self._runCommand('which whois')
        whois_version_cmd += ' --version'
        whois_detected_version = self._runCommand(whois_version_cmd)

        # regex used to detect nmap
        #regex = re.compile('Nmap version [0-9]*\.[0-9]*[^ ]* \( http://.* \)')
        regex = re.compile('.*whois version [0-9]*\.[0-9], .*')

        for line in whois_detected_version.split('\n'):
            if regex.match(line) is not None:
                # Search for version number
                regex_version = re.compile('[0-9]\.[0-9]')

                rv = regex_version.search(line)

                if rv is not None:
                    # extract version/subversion
                    self.wass.WhoisVersion = str(line[rv.start():rv.end()])

                break

    def _GetZAProxyVersion(self):
        '''
        Get ZAProxy Version

        This will look for the ~/.ZAP/config.xml file and look for the Version number in that.
        config.xml example:
        <version>2003000</version>

        sets the  the self.wass.ZAProxyVersion
        '''
        zaproxy_detected_version = None

        if (os.path.isfile(os.path.expanduser('~') + '/.ZAP/config.xml')):
            zap_config = open(os.path.expanduser('~') + '/.ZAP/config.xml')
            for line in zap_config:
                zaproxy_detected_version = line

                if (zaproxy_detected_version == '<version>2003000</version>\n'):
                    self.wass.ZAProxyVersion = '2.3.0'
                    break
                elif (zaproxy_detected_version == '<version>2002002</version>\n'):
                    self.wass.ZAProxyVersion = '2.2.2'
                    break
        else:
            if (self.wass.LogLevel.upper() == "DEBUG"):
                print ("The Version of ZAProxy cannot be set.")
                print ("The default ZAProxy config.xml file was not found!!")
                print ("It should be: %s" % os.path.expanduser('~') + '/.ZAP/config.xml')
                print ("Please run the ZAProxy gui and accecpt the Licens, and create the owasp_zap_root_ca.cer file")
