'''
__init__.py

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
#TODO: Cleanup ????? !!!!!!!
"""
Client implementation for using the WASS Functions.
"""

__version__ = '0.1.1'
__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.05.03'

import time
from attack.sqlmap import WassSQLMap
from common.common import WassCommon
from common.checkarguments import WassCheckArguments
from common.checkoptions import WassCheckOptions
from common.getversion import WassGetVersion
from common.wassexception import WassException
from common.wasslogging import WassLogging
from common.wassxml import WassXML
from info.fierce import WassFierce
from info.nmap import WassNmap
from info.sslyze import WassSSLyze
from info.sslscan import WassSSLScan
from info.theharvester import WassTheHarvester
from info.whatweb import WassWhatWeb
from info.whois import WassWhoIS
from webscan.arachni import WassArachni
from webscan.nikto import WassNikto
from webscan.openvas import WassOpenVAS
from webscan.skipfish import WassSkipfish
from webscan.w3af import WassW3af
from webscan.wapiti import WassWapiti
from webscan.zaproxy import WassZAProxy


class WASS(object):
    """
    the main WASS Object.
    """

    def __init__(self):
        """
        Creates an instance of the WASS.
        """
        # This is the WASS Object
        self.__ShortVersion = __version__
        self.__LongVersion = 'WASS version is: ' + __version__ + '\tIt was last modified: ' + __updated__
        self.__CurrentTask = None  # This will hold the name of the current running task
        self.__OrgWorkingDir = None  # This is the Original Working Directory
        self.__PythonVersion = None  # This is the Python Version
        self.__OS = None  # This is the OS we are running on
        self.__OSVersion = None  # This is the Version of the OS we are running on
        self.__WASSArguments = None  # This is arguments we where called with
        self.__Program = None  # This is what we should do, look at the line below
        self.__Programs = ['ALL', 'Arachni', 'Fierce', 'Nikto', 'Nmap', 'OpenVAS', 'Skipfish', 'SSLyze', 'SSLScan',
                            'TheHarvester', 'W3af', 'Wapiti', 'WhatWeb', 'Whois', 'ZAProxy', 'Info', 'Update']  # This is a list of supported programs
        self.__RunArachni = False  # Should we run Arachni, this check is done in the checkoptions module
        self.__RunFierce = False  # Should we run Fierce, this check is done in the checkoptions module
        self.__RunNikto = False  # Should we run Nikto, this check is done in the checkoptions module
        self.__RunNmap = False  # Should we run Nmap, this check is done in the checkoptions module
        self.__RunOpenVAS = False  # Should we run OpenVAS, this check is done in the checkoptions module
        self.__RunSkipfish = False  # Should we run Skipfish, this check is done in the checkoptions module
        self.__RunSSLyze = False  # Should we run SSLyze, this check is done in the checkoptions module
        self.__RunSSLScan = False  # Should we run SSLScan, this check is done in the checkoptions module
        self.__RunTheHarvester = False  # Should we run TheHarvester, this check is done in the checkoptions module
        self.__RunW3af = False  # Should we run W3af, this check is done in the checkoptions module
        self.__RunWapiti = False  # Should we run Wapiti, this check is done in the checkoptions module
        self.__RunWhatWeb = False  # Should we run WhatWeb, this check is done in the checkoptions module
        self.__RunWhois = False  # Should we run Whois, this check is done in the checkoptions module
        self.__RunZAProxy = False  # Should we run ZAProxy, this check is done in the checkoptions module
        self.__TargetDomain = None  # This is the Target Domain set on the command line with the -t / --target option
        self.__TldDomainName = None  # This is the Top Level Domain name of the target, e.g. TLD of www.google.com is google.com
        self.__TargetPort = None  # This is the target port set on the command line with the -p / --port option, defaults to 80
        self.__TargetURL = None  # This is the target URL to start the scans at e.g. /Administrator/view-account.php
        self.__TargetScheme = None  # This is the target scheme set on the command line with the -s / --scheme option, e.g. http or https, defaults to http
        self.__TargetExcludeURLS = None  # This is the URL(s) that should be excluded from the scan, set on the command line with the -e / --exclude option
        self.__TargetExcludeURLSRegex = None  # This is a regex expression of the exclude URL(s) given on the command line
        self.__TargetIP = None  # This is the IP Address of the target domain
        self.__TargetIPVersion = None  # This is the version of the IP Address e.g. v4 or v6
        self.__TargetIPType = None  # This is the type of IP Address the target have e.g. Private (True) or Public (False)
        self.__ScanTarget = None  # This is the Scan Target, e.g. http://zero.webappsecurity.com
        self.__AuthedBy = None  # This holds the name of the person who did this scan
        self.__AuthUser = None  # This is the User Name to use to login to restricted areas of the Web Application
        self.__AuthPW = None  # This is the User Password to use to login to restricted areas of the Web Application
        self.__AuthType = None  # This is the Authentication Type used to login to restricted areas of the Web Application
        self.__AuthURL = None  # This is Authentication URL to use to login to the restricted areas of the Web Application
        self.__AuthVerifyURL = None  # This is the URL to look for to see that we have successfully logged in to the Web Application
        self.__LogLevel = 'INFO'  # This is the log level to use for the logging in this application
        self.__ToEmail = None  # This is the Email address to send the result email to
        self.__FromEmail = None  # This is the Email address to send the result email as
        self.__SendEmail = True  # Should we send the result Email from each of the processes
        self.__ZIPPassword = None  # This is the password that will be use for the ZIP file that is created for the result email
        self.__LocalZAProxyProtocol = None  # This is the scheme that the local ZAProxy is running
        self.__LocalZAProxyHost = None  # This is the network address for the local ZAProxy
        self.__LocalZAProxyPort = None  # This is the port that the local ZAProxy is running on
        self.__LocalZAProxy = None  # This contains the complete ZAProxy URL e.g. http://127.0.0.1:8080
        self.__UseLocalZAProxy = False  # Should we use the ZAProxy for all the Web Scanners
        self.__ArachniVersion = None
        self.__ArachniCMD = None
        self.__ArachniAFRReport = None
        self.__ArachniXMLReport = None
        self.__ArachniHTMLReport = None
        self.__ArachniErrorLog = None
        self.__ArachniCLI = None  # This is the Command Line for the Arachni run
        self.__ArachniArguments = None
        self.__ArachniRunLog = None
        self.__ArachniWassLog = None
        self.__FierceVersion = None
        self.__FierceCMD = None
        self.__FierceXMLReport = None
        self.__FierceCLI = None  # This is the Command Line for the Fierce run
        self.__FierceArguments = None
        self.__FierceRunLog = None
        self.__FierceWassLog = None
        self.__NiktoVersion = None
        self.__NiktoCMD = None
        self.__NiktoXMLReport = None
        self.__NiktoRunLog = None
        self.__NiktoCLI = None  # This is the Command Line for the Nikto run
        self.__NiktoArguments = None
        self.__NiktoWassLog = None
        self.__NmapVersion = None
        self.__NmapCMD = None
        self.__NmapPort = None
        self.__NmapArguments = None
        self.__NmapXML = None
        self.__NmapWassLog = None
        self.__SkipfishVersion = None
        self.__SkipfishCMD = None
        self.__SkipfishCLI = None
        self.__SkipfishWordList = None
        self.__SkipfishScanWordList = None
        self.__SkipfishOutputDir = None
        self.__SkipfishArguments = None
        self.__SkipfishRunLog = None  # This is the log file that the Skipfish run will log to
        self.__SkipfishWassLog = None
        self.__SQLMapRunLog = None
        self.__SQLMapWassLog = None
        self.__SSLyzeVersion = None
        self.__SSLyzeCMD = None
        self.__SSLyzeCLI = None
        self.__SSLyzeArguments = None
        self.__SSLyzeXMLReport = None
        self.__SSLyzeRunLog = None
        self.__SSLyzeWassLog = None
        self.__SSLScanVersion = None
        self.__SSLScanCMD = None
        self.__SSLScanCLI = None
        self.__SSLScanArguments = None
        self.__SSLScanXMLReport = None
        self.__SSLScanRunLog = None
        self.__SSLScanWassLog = None
        self.__TheHarvesterVersion = None
        self.__TheHarvesterCMD = None
        self.__TheHarvesterCLI = None
        self.__TheHarvesterArguments = None
        self.__TheHarvesterReportName = None
        self.__TheHarvesterRunLog = None
        self.__TheHarvesterWassLog = None
        self.__W3afVersion = None
        self.__W3afCMD = None
        self.__W3afCMDFile = None
        self.__W3afProfile = None
        self.__W3afCLI = None  # This is the Command Line for the W3af run
        self.__W3afXMLReport = None
        self.__W3afHTMLReport = None
        self.__W3afHTTPOut = None
        self.__W3afRepOut = None
        self.__W3afRunLog = None
        self.__W3afWassLog = None
        self.__WapitiVersion = None
        self.__WapitiCMD = None
        self.__WapitiCLI = None  # This is the Command Line for the Wapiti run
        self.__WapitiArguments = None
        self.__WapitiXMLReport = None
        self.__WapitiRunLog = None
        self.__WapitiWassLog = None
        self.__WhatWebVersion = None
        self.__WhatWebCMD = None
        self.__WhatWebCLI = None
        self.__WhatWebArguments = None
        self.__WhatWebXMLReport = None
        self.__WhatWebRunLog = None
        self.__WhatWebWassLog = None
        self.__WhoisVersion = None
        self.__WhoisCMD = None
        self.__WhoisTargetXMLReport = None
        self.__WhoisTargetIPXMLReport = None
        self.__WhoisWassLog = None
        self.__OpenVASVersion = None
        self.__OpenVASCMD = None
        self.__OpenVASUser = None
        self.__OpenVASPassword = None
        self.__OpenVASHost = None
        self.__OpenVASPortListID = None
        self.__OpenVASTargetID = None
        self.__OpenVASNewConfigID = None
        self.__OpenVASTaskID = None
        self.__OpenVASTaskReportID = None
        self.__OpenVASTargetStatus = None
        self.__OpenVASConfigStatus = None
        self.__OpenVASConfigModifyVHOSTSStatus = None
        self.__OpenVASConfigModifyVHOSTSIPStatus = None
        self.__OpenVASTaskStatus = None
        self.__OpenVASTaskProgress = None
        self.__OpenVASWassLog = None
        self.__ZAProxyVersion = None
        self.__ZAProxyPath = None
        self.__ZAProxyCMD = None
        self.__ZAProxyIsRunning = False
        self.__ZAProxyRunningPid = False
        self.__ZAProxyCLI = None
        self.__ZAProxyDaemon = True
        self.__ZAProxyAlertThreshold = None
        self.__ZAProxyAttackStrength = None
        self.__ZAProxyStart = True
        self.__ZAProxyStop = True
        self.__ZAProxyXMLReport = None
        self.__ZAProxySessionFile = None
        self.__ZAProxySessionDataFile = None
        self.__ZAProxySessionLCKFile = None
        self.__ZAProxySessionLogFile = None
        self.__ZAProxySessionPropertiesFile = None
        self.__ZAProxySessionScriptFile = None
        self.__ZAProxyWassLog = None
        self.__ResultDir = None
        self.__ReportDate = time.strftime("%Y-%m-%d_%H%M",)
        self.__ToDay = time.strftime("%Y-%m-%d",)
        #Import other WASS Modules
        self.WassException = WassException(self)
        self.WassLogging = WassLogging(self)
        self.WassCheckArguments = WassCheckArguments(self)
        self.WassCheckOptions = WassCheckOptions(self)
        self.WassCommon = WassCommon(self)
        self.WassGetVersion = WassGetVersion(self)
        self.WassXML = WassXML(self)
        self.WassWhois = WassWhoIS(self)
        self.WassNmap = WassNmap(self)
        self.WassArachni = WassArachni(self)
        self.WassNikto = WassNikto(self)
        self.WassOpenVAS = WassOpenVAS(self)
        self.WassSkipfish = WassSkipfish(self)
        self.WassSSLyze = WassSSLyze(self)
        self.WassSSLScan = WassSSLScan(self)
        self.WassTheHarvester = WassTheHarvester(self)
        self.WassSQLMap = WassSQLMap(self)
        self.WassW3af = WassW3af(self)
        self.WassWapiti = WassWapiti(self)
        self.WassWhatWeb = WassWhatWeb(self)
        self.WassZAProxy = WassZAProxy(self)
        self.WassFierce = WassFierce(self)

    @property
    def ShortVersion(self):
        return self.__ShortVersion

    @property
    def LongVersion(self):
        return self.__LongVersion

    @property
    def CurrentTask(self):
        return self.__CurrentTask

    @CurrentTask.setter
    def CurrentTask(self, CurrentTask):
        self.__CurrentTask = CurrentTask

    @property
    def OrgWorkingDir(self):
        return self.__OrgWorkingDir

    @OrgWorkingDir.setter
    def OrgWorkingDir(self, OrgWorkingDir):
        self.__OrgWorkingDir = OrgWorkingDir

    @property
    def PythonVersion(self):
        return self.__PythonVersion

    @PythonVersion.setter
    def PythonVersion(self, PythonVersion):
        self.__PythonVersion = PythonVersion

    @property
    def SystemOS(self):
        return self.__SystemOS

    @SystemOS.setter
    def SystemOS(self, SystemOS):
        self.__SystemOS = SystemOS

    @property
    def OSVersion(self):
        return self.__OSVersion

    @OSVersion.setter
    def OSVersion(self, OSVersion):
        self.__OSVersion = OSVersion

    @property
    def WASSArguments(self):
        return self.__WASSArguments

    @WASSArguments.setter
    def WASSArguments(self, WASSArguments):
        self.__WASSArguments = WASSArguments

    @property
    def Program(self):
        return self.__Program

    @Program.setter
    def Program(self, Program):
        self.__Program = Program

    @property
    def Programs(self):
        return self.__Programs

    @property
    def RunArachni(self):
        return self.__RunArachni

    @RunArachni.setter
    def RunArachni(self, RunArachni):
        self.__RunArachni = RunArachni

    @property
    def RunFierce(self):
        return self.__RunFierce

    @RunFierce.setter
    def RunFierce(self, RunFierce):
        self.__RunFierce = RunFierce

    @property
    def RunNikto(self):
        return self.__RunNikto

    @RunNikto.setter
    def RunNikto(self, RunNikto):
        self.__RunNikto = RunNikto

    @property
    def RunNmap(self):
        return self.__RunNmap

    @RunNmap.setter
    def RunNmap(self, RunNmap):
        self.__RunNmap = RunNmap

    @property
    def RunOpenVAS(self):
        return self.__RunOpenVAS

    @RunOpenVAS.setter
    def RunOpenVAS(self, RunOpenVAS):
        self.__RunOpenVAS = RunOpenVAS

    @property
    def RunSkipfish(self):
        return self.__RunSkipfish

    @RunSkipfish.setter
    def RunSkipfish(self, RunSkipfish):
        self.__RunSkipfish = RunSkipfish

    @property
    def RunSSLyze(self):
        return self.__RunSSLyze

    @RunSSLyze.setter
    def RunSSLyze(self, RunSSLyze):
        self.__RunSSLyze = RunSSLyze

    @property
    def RunSSLScan(self):
        return self.__RunSSLScan

    @RunSSLScan.setter
    def RunSSLScan(self, RunSSLScan):
        self.__RunSSLScan = RunSSLScan

    @property
    def RunTheHarvester(self):
        return self.__RunTheHarvester

    @RunTheHarvester.setter
    def RunTheHarvester(self, RunTheHarvester):
        self.__RunTheHarvester = RunTheHarvester

    @property
    def RunW3af(self):
        return self.__RunW3af

    @RunW3af.setter
    def RunW3af(self, RunW3af):
        self.__RunW3af = RunW3af

    @property
    def RunWapiti(self):
        return self.__RunWapiti

    @RunWapiti.setter
    def RunWapiti(self, RunWapiti):
        self.__RunWapiti = RunWapiti

    @property
    def RunWhatWeb(self):
        return self.__RunWhatWeb

    @RunWhatWeb.setter
    def RunWhatWeb(self, RunWhatWeb):
        self.__RunWhatWeb = RunWhatWeb

    @property
    def RunWhois(self):
        return self.__RunWhois

    @RunWhois.setter
    def RunWhois(self, RunWhois):
        self.__RunWhois = RunWhois

    @property
    def RunZAProxy(self):
        return self.__RunZAProxy

    @RunZAProxy.setter
    def RunZAProxy(self, RunZAProxy):
        self.__RunZAProxy = RunZAProxy

    @property
    def Customer(self):
        return self.__Customer

    @Customer.setter
    def Customer(self, Customer):
        self.__Customer = Customer

    @property
    def TargetDomain(self):
        return self.__TargetDomain

    @TargetDomain.setter
    def TargetDomain(self, TargetDomain):
        self.__TargetDomain = TargetDomain

    @property
    def TldDomainName(self):
        return self.__TldDomainName

    @TldDomainName.setter
    def TldDomainName(self, TldDomainName):
        self.__TldDomainName = TldDomainName

    @property
    def TargetPort(self):
        return self.__TargetPort

    @TargetPort.setter
    def TargetPort(self, TargetPort):
        self.__TargetPort = TargetPort

    @property
    def TargetURL(self):
        return self.__TargetURL

    @TargetURL.setter
    def TargetURL(self, TargetURL):
        self.__TargetURL = TargetURL

    @property
    def TargetScheme(self):
        return self.__TargetScheme

    @TargetScheme.setter
    def TargetScheme(self, TargetScheme):
        self.__TargetScheme = TargetScheme

    @property
    def TargetExcludeURLS(self):
        return self.__TargetExcludeURLS

    @TargetExcludeURLS.setter
    def TargetExcludeURLS(self, TargetExcludeURLS):
        self.__TargetExcludeURLS = TargetExcludeURLS

    @property
    def TargetExcludeURLSRegex(self):
        return self.__TargetExcludeURLSRegex

    @TargetExcludeURLSRegex.setter
    def TargetExcludeURLSRegex(self, TargetExcludeURLSRegex):
        self.__TargetExcludeURLSRegex = TargetExcludeURLSRegex

    @property
    def TargetIP(self):
        return self.__TargetIP

    @TargetIP.setter
    def TargetIP(self, TargetIP):
        self.__TargetIP = TargetIP

    @property
    def TargetIPVersion(self):
        return self.__TargetIPVersion

    @TargetIPVersion.setter
    def TargetIPVersion(self, TargetIPVersion):
        self.__TargetIPVersion = TargetIPVersion

    @property
    def TargetIPType(self):
        return self.__TargetIPType

    @TargetIPType.setter
    def TargetIPType(self, TargetIPType):
        self.__TargetIPType = TargetIPType

    @property
    def ScanTarget(self):
        return self.__ScanTarget

    @ScanTarget.setter
    def ScanTarget(self, ScanTarget):
        self.__ScanTarget = ScanTarget

    @property
    def AuthedBy(self):
        return self.__AuthedBy

    @AuthedBy.setter
    def AuthedBy(self, AuthedBy):
        self.__AuthedBy = AuthedBy

    @property
    def AuthUser(self):
        return self.__AuthUser

    @AuthUser.setter
    def AuthUser(self, AuthUser):
        self.__AuthUser = AuthUser

    @property
    def AuthPW(self):
        return self.__AuthPW

    @AuthPW.setter
    def AuthPW(self, AuthPW):
        self.__AuthPW = AuthPW

    @property
    def AuthType(self):
        return self.__AuthType

    @AuthType.setter
    def AuthType(self, AuthType):
        self.__AuthType = AuthType

    @property
    def AuthURL(self):
        return self.__AuthURL

    @AuthURL.setter
    def AuthURL(self, AuthURL):
        self.__AuthURL = AuthURL

    @property
    def AuthVerifyURL(self):
        return self.__AuthVerifyURL

    @AuthVerifyURL.setter
    def AuthVerifyURL(self, AuthVerifyURL):
        self.__AuthVerifyURL = AuthVerifyURL

    @property
    def LogLevel(self):
        return self.__LogLevel

    @LogLevel.setter
    def LogLevel(self, LogLevel):
        self.__LogLevel = LogLevel.upper()

    @property
    def ToEmail(self):
        return self.__ToEmail

    @ToEmail.setter
    def ToEmail(self, ToEmail):
        self.__ToEmail = ToEmail

    @property
    def FromEmail(self):
        return self.__FromEmail

    @FromEmail.setter
    def FromEmail(self, FromEmail):
        self.__FromEmail = FromEmail

    @property
    def SendEmail(self):
        return self.__SendEmail

    @SendEmail.setter
    def SendEmail(self, SendEmail):
        self.__SendEmail = SendEmail

    @property
    def ZIPPassword(self):
        return self.__ZIPPassword

    @ZIPPassword.setter
    def ZIPPassword(self, ZIPPassword):
        self.__ZIPPassword = ZIPPassword

    @property
    def LocalZAProxyProtocol(self):
        return self.__LocalZAProxyProtocol

    @LocalZAProxyProtocol.setter
    def LocalZAProxyProtocol(self, LocalZAProxyProtocol):
        self.__LocalZAProxyProtocol = LocalZAProxyProtocol

    @property
    def LocalZAProxyHost(self):
        return self.__LocalZAProxyHost

    @LocalZAProxyHost.setter
    def LocalZAProxyHost(self, LocalZAProxyHost):
        self.__LocalZAProxyHost = LocalZAProxyHost

    @property
    def LocalZAProxyPort(self):
        return self.__LocalZAProxyPort

    @LocalZAProxyPort.setter
    def LocalZAProxyPort(self, LocalZAProxyPort):
        self.__LocalZAProxyPort = LocalZAProxyPort

    @property
    def LocalZAProxy(self):
        return self.__LocalZAProxy

    @LocalZAProxy.setter
    def LocalZAProxy(self, LocalZAProxy):
        self.__LocalZAProxy = LocalZAProxy

    @property
    def UseLocalZAProxy(self):
        return self.__UseLocalZAProxy

    @UseLocalZAProxy.setter
    def UseLocalZAProxy(self, UseLocalZAProxy):
        self.__UseLocalZAProxy = UseLocalZAProxy

    @property
    def ArachniVersion(self):
        return self.__ArachniVersion

    @ArachniVersion.setter
    def ArachniVersion(self, ArachniVersion):
        self.__ArachniVersion = ArachniVersion

    @property
    def ArachniCMD(self):
        return self.__ArachniCMD

    @ArachniCMD.setter
    def ArachniCMD(self, ArachniCMD):
        self.__ArachniCMD = ArachniCMD

    @property
    def ArachniAFRReport(self):
        return self.__ArachniAFRReport

    @ArachniAFRReport.setter
    def ArachniAFRReport(self, ArachniAFRReport):
        self.__ArachniAFRReport = self.__ResultDir + "/" + ArachniAFRReport

    @property
    def ArachniXMLReport(self):
        return self.__ArachniXMLReport

    @ArachniXMLReport.setter
    def ArachniXMLReport(self, ArachniXMLReport):
        self.__ArachniXMLReport = self.__ResultDir + "/" + ArachniXMLReport

    @property
    def ArachniHTMLReport(self):
        return self.__ArachniHTMLReport

    @ArachniHTMLReport.setter
    def ArachniHTMLReport(self, ArachniHTMLReport):
        self.__ArachniHTMLReport = self.__ResultDir + "/" + ArachniHTMLReport

    @property
    def ArachniErrorLog(self):
        return self.__ArachniErrorLog

    @ArachniErrorLog.setter
    def ArachniErrorLog(self, ArachniErrorLog):
        self.__ArachniErrorLog = self.__ResultDir + "/" + ArachniErrorLog

    @property
    def ArachniCLI(self):
        return self.__ArachniCLI

    @ArachniCLI.setter
    def ArachniCLI(self, ArachniCLI):
        self.__ArachniCLI = ArachniCLI

    @property
    def ArachniArguments(self):
        return self.__ArachniArguments

    @ArachniArguments.setter
    def ArachniArguments(self, ArachniArguments):
        self.__ArachniArguments = ArachniArguments

    @property
    def ArachniRunLog(self):
        return self.__ArachniRunLog

    @ArachniRunLog.setter
    def ArachniRunLog(self, ArachniRunLog):
        self.__ArachniRunLog = self.__ResultDir + "/" + ArachniRunLog

    @property
    def ArachniWassLog(self):
        return self.__ArachniWassLog

    @ArachniWassLog.setter
    def ArachniWassLog(self, ArachniWassLog):
        self.__ArachniWassLog = self.__ResultDir + "/" + ArachniWassLog

    @property
    def FierceVersion(self):
        return self.__FierceVersion

    @FierceVersion.setter
    def FierceVersion(self, FierceVersion):
        self.__FierceVersion = FierceVersion

    @property
    def FierceCMD(self):
        return self.__FierceCMD

    @FierceCMD.setter
    def FierceCMD(self, FierceCMD):
        self.__FierceCMD = FierceCMD

    @property
    def FierceXMLReport(self):
        return self.__FierceXMLReport

    @FierceXMLReport.setter
    def FierceXMLReport(self, FierceXMLReport):
        self.__FierceXMLReport = self.__ResultDir + "/" + FierceXMLReport

    @property
    def FierceCLI(self):
        return self.__FierceCLI

    @FierceCLI.setter
    def FierceCLI(self, FierceCLI):
        self.__FierceCLI = FierceCLI

    @property
    def FierceArguments(self):
        return self.__FierceArguments

    @FierceArguments.setter
    def FierceArguments(self, FierceArguments):
        self.__FierceArguments = FierceArguments

    @property
    def FierceRunLog(self):
        return self.__FierceRunLog

    @FierceRunLog.setter
    def FierceRunLog(self, FierceRunLog):
        self.__FierceRunLog = self.__ResultDir + "/" + FierceRunLog
    @property
    def FierceWassLog(self):
        return self.__FierceWassLog

    @FierceWassLog.setter
    def FierceWassLog(self, FierceWassLog):
        self.__FierceWassLog = self.__ResultDir + "/" + FierceWassLog

    @property
    def NiktoVersion(self):
        return self.__NiktoVersion

    @NiktoVersion.setter
    def NiktoVersion(self, NiktoVersion):
        self.__NiktoVersion = NiktoVersion

    @property
    def NiktoCMD(self):
        return self.__NiktoCMD

    @NiktoCMD.setter
    def NiktoCMD(self, NiktoCMD):
        self.__NiktoCMD = NiktoCMD

    @property
    def NiktoXMLReport(self):
        return self.__NiktoXMLReport

    @NiktoXMLReport.setter
    def NiktoXMLReport(self, NiktoXMLReport):
        self.__NiktoXMLReport = self.__ResultDir + "/" + NiktoXMLReport

    @property
    def NiktoRunLog(self):
        return self.__NiktoRunLog

    @NiktoRunLog.setter
    def NiktoRunLog(self, NiktoRunLog):
        self.__NiktoRunLog = self.__ResultDir + "/" + NiktoRunLog

    @property
    def NiktoCLI(self):
        return self.__NiktoCLI

    @NiktoCLI.setter
    def NiktoCLI(self, NiktoCLI):
        self.__NiktoCLI = NiktoCLI

    @property
    def NiktoArguments(self):
        return self.__NiktoArguments

    @NiktoArguments.setter
    def NiktoArguments(self, NiktoArguments):
        self.__NiktoArguments = NiktoArguments

    @property
    def NiktoWassLog(self):
        return self.__NiktoWassLog

    @NiktoWassLog.setter
    def NiktoWassLog(self, NiktoWassLog):
        self.__NiktoWassLog = self.__ResultDir + "/" + NiktoWassLog

    @property
    def NmapVersion(self):
        return self.__NmapVersion

    @NmapVersion.setter
    def NmapVersion(self, NmapVersion):
        self.__NmapVersion = NmapVersion

    @property
    def NmapCMD(self):
        return self.__NmapCMD

    @NmapCMD.setter
    def NmapCMD(self, NmapCMD):
        self.__NmapCMD = NmapCMD

    @property
    def NmapPort(self):
        return self.__NmapPort

    @NmapPort.setter
    def NmapPort(self, NmapPort):
        self.__NmapPort = NmapPort

    @property
    def NmapArguments(self):
        return self.__NmapArguments

    @NmapArguments.setter
    def NmapArguments(self, NmapArguments):
        self.__NmapArguments = NmapArguments

    @property
    def NmapXML(self):
        return self.__NmapXML

    @NmapXML.setter
    def NmapXML(self, NmapXML):
        self.__NmapXML = self.__ResultDir + "/" + NmapXML

    @property
    def NmapWassLog(self):
        return self.__NmapWassLog

    @NmapWassLog.setter
    def NmapWassLog(self, NmapWassLog):
        self.__NmapWassLog = self.__ResultDir + "/" + NmapWassLog

    @property
    def SkipfishVersion(self):
        return self.__SkipfishVersion

    @SkipfishVersion.setter
    def SkipfishVersion(self, SkipfishVersion):
        self.__SkipfishVersion = SkipfishVersion

    @property
    def SkipfishCMD(self):
        return self.__SkipfishCMD

    @SkipfishCMD.setter
    def SkipfishCMD(self, SkipfishCMD):
        self.__SkipfishCMD = SkipfishCMD

    @property
    def SkipfishCLI(self):
        return self.__SkipfishCLI

    @SkipfishCLI.setter
    def SkipfishCLI(self, SkipfishCLI):
        self.__SkipfishCLI = SkipfishCLI

    @property
    def SkipfishWordList(self):
        return self.__SkipfishWordList

    @SkipfishWordList.setter
    def SkipfishWordList(self, SkipfishWordList):
        self.__SkipfishWordList = SkipfishWordList

    @property
    def SkipfishScanWordList(self):
        return self.__SkipfishScanWordList

    @SkipfishScanWordList.setter
    def SkipfishScanWordList(self, SkipfishScanWordList):
        self.__SkipfishScanWordList = self.__ResultDir + "/" + SkipfishScanWordList

    @property
    def SkipfishOutputDir(self):
        return self.__SkipfishOutputDir

    @SkipfishOutputDir.setter
    def SkipfishOutputDir(self, SkipfishOutputDir):
        self.__SkipfishOutputDir = self.__ResultDir + "/" + SkipfishOutputDir

    @property
    def SkipfishArguments(self):
        return self.__SkipfishArguments

    @SkipfishArguments.setter
    def SkipfishArguments(self, SkipfishArguments):
        self.__SkipfishArguments = SkipfishArguments

    @property
    def SkipfishRunLog(self):
        return self.__SkipfishRunLog

    @SkipfishRunLog.setter
    def SkipfishRunLog(self, SkipfishRunLog):
        self.__SkipfishRunLog = self.__ResultDir + "/" + SkipfishRunLog

    @property
    def SkipfishWassLog(self):
        return self.__SkipfishWassLog

    @SkipfishWassLog.setter
    def SkipfishWassLog(self, SkipfishWassLog):
        self.__SkipfishWassLog = self.__ResultDir + "/" + SkipfishWassLog

    @property
    def SQLMapRunLog(self):
        return self.__SQLMapRunLog

    @SQLMapRunLog.setter
    def SQLMapRunLog(self, SQLMapRunLog):
        self.__SQLMapRunLog = self.__ResultDir + "/" + SQLMapRunLog

    @property
    def SQLMapWassLog(self):
        return self.__SQLMapWassLog

    @SQLMapWassLog.setter
    def SQLMapWassLog(self, SQLMapWassLog):
        self.__SQLMapWassLog = self.__ResultDir + "/" + SQLMapWassLog

    @property
    def SSLyzeVersion(self):
        return self.__SSLyzeVersion

    @SSLyzeVersion.setter
    def SSLyzeVersion(self, SSLyzeVersion):
        self.__SSLyzeVersion = SSLyzeVersion

    @property
    def SSLyzeCMD(self):
        return self.__SSLyzeCMD

    @SSLyzeCMD.setter
    def SSLyzeCMD(self, SSLyzeCMD):
        self.__SSLyzeCMD = SSLyzeCMD

    @property
    def SSLyzeCLI(self):
        return self.__SSLyzeCLI

    @SSLyzeCLI.setter
    def SSLyzeCLI(self, SSLyzeCLI):
        self.__SSLyzeCLI = SSLyzeCLI

    @property
    def SSLyzeArguments(self):
        return self.__SSLyzeArguments

    @SSLyzeArguments.setter
    def SSLyzeArguments(self, SSLyzeArguments):
        self.__SSLyzeArguments = SSLyzeArguments

    @property
    def SSLyzeXMLReport(self):
        return self.__SSLyzeXMLReport

    @SSLyzeXMLReport.setter
    def SSLyzeXMLReport(self, SSLyzeXMLReport):
        self.__SSLyzeXMLReport = self.__ResultDir + "/" + SSLyzeXMLReport

    @property
    def SSLyzeRunLog(self):
        return self.__SSLyzeRunLog

    @SSLyzeRunLog.setter
    def SSLyzeRunLog(self, SSLyzeRunLog):
        self.__SSLyzeRunLog = self.__ResultDir + "/" + SSLyzeRunLog

    @property
    def SSLyzeWassLog(self):
        return self.__SSLyzeWassLog

    @SSLyzeWassLog.setter
    def SSLyzeWassLog(self, SSLyzeWassLog):
        self.__SSLyzeWassLog = self.__ResultDir + "/" + SSLyzeWassLog

    @property
    def SSLScanVersion(self):
        return self.__SSLScanVersion

    @SSLScanVersion.setter
    def SSLScanVersion(self, SSLScanVersion):
        self.__SSLScanVersion = SSLScanVersion

    @property
    def SSLScanCMD(self):
        return self.__SSLScanCMD

    @SSLScanCMD.setter
    def SSLScanCMD(self, SSLScanCMD):
        self.__SSLScanCMD = SSLScanCMD

    @property
    def SSLScanCLI(self):
        return self.__SSLScanCLI

    @SSLScanCLI.setter
    def SSLScanCLI(self, SSLScanCLI):
        self.__SSLScanCLI = SSLScanCLI

    @property
    def SSLScanArguments(self):
        return self.__SSLScanArguments

    @SSLScanArguments.setter
    def SSLScanArguments(self, SSLScanArguments):
        self.__SSLScanArguments = SSLScanArguments

    @property
    def SSLScanXMLReport(self):
        return self.__SSLScanXMLReport

    @SSLScanXMLReport.setter
    def SSLScanXMLReport(self, SSLScanXMLReport):
        self.__SSLScanXMLReport = self.__ResultDir + "/" + SSLScanXMLReport

    @property
    def SSLScanRunLog(self):
        return self.__SSLScanRunLog

    @SSLScanRunLog.setter
    def SSLScanRunLog(self, SSLScanRunLog):
        self.__SSLScanRunLog = self.__ResultDir + "/" + SSLScanRunLog

    @property
    def SSLScanWassLog(self):
        return self.__SSLScanWassLog

    @SSLScanWassLog.setter
    def SSLScanWassLog(self, SSLScanWassLog):
        self.__SSLScanWassLog = self.__ResultDir + "/" + SSLScanWassLog

    @property
    def TheHarvesterVersion(self):
        return self.__TheHarvesterVersion

    @TheHarvesterVersion.setter
    def TheHarvesterVersion(self, TheHarvesterVersion):
        self.__TheHarvesterVersion = TheHarvesterVersion

    @property
    def TheHarvesterCMD(self):
        return self.__TheHarvesterCMD

    @TheHarvesterCMD.setter
    def TheHarvesterCMD(self, TheHarvesterCMD):
        self.__TheHarvesterCMD = TheHarvesterCMD

    @property
    def TheHarvesterCLI(self):
        return self.__TheHarvesterCLI

    @TheHarvesterCLI.setter
    def TheHarvesterCLI(self, TheHarvesterCLI):
        self.__TheHarvesterCLI = TheHarvesterCLI

    @property
    def TheHarvesterArguments(self):
        return self.__TheHarvesterArguments

    @TheHarvesterArguments.setter
    def TheHarvesterArguments(self, TheHarvesterArguments):
        self.__TheHarvesterArguments = TheHarvesterArguments

    @property
    def TheHarvesterReportName(self):
        return self.__TheHarvesterReportName

    @TheHarvesterReportName.setter
    def TheHarvesterReportName(self, TheHarvesterReportName):
        self.__TheHarvesterReportName = self.__ResultDir + "/" + TheHarvesterReportName

    @property
    def TheHarvesterRunLog(self):
        return self.__TheHarvesterRunLog

    @TheHarvesterRunLog.setter
    def TheHarvesterRunLog(self, TheHarvesterRunLog):
        self.__TheHarvesterRunLog = self.__ResultDir + "/" + TheHarvesterRunLog

    @property
    def TheHarvesterWassLog(self):
        return self.__TheHarvesterWassLog

    @TheHarvesterWassLog.setter
    def TheHarvesterWassLog(self, TheHarvesterWassLog):
        self.__TheHarvesterWassLog = self.__ResultDir + "/" + TheHarvesterWassLog

    @property
    def W3afVersion(self):
        return self.__W3afVersion

    @W3afVersion.setter
    def W3afVersion(self, W3afVersion):
        self.__W3afVersion = W3afVersion

    @property
    def W3afCMD(self):
        return self.__W3afCMD

    @W3afCMD.setter
    def W3afCMD(self, W3afCMD):
        self.__W3afCMD = W3afCMD

    @property
    def W3afCMDFile(self):
        return self.__W3afCMDFile

    @W3afCMDFile.setter
    def W3afCMDFile(self, W3afCMDFile):
        self.__W3afCMDFile = self.__ResultDir + "/" + W3afCMDFile

    @property
    def W3afProfile(self):
        return self.__W3afProfile

    @W3afProfile.setter
    def W3afProfile(self, W3afProfile):
        self.__W3afProfile = W3afProfile

    @property
    def W3afCLI(self):
        return self.__W3afCLI

    @W3afCLI.setter
    def W3afCLI(self, W3afCLI):
        self.__W3afCLI = W3afCLI

    @property
    def W3afXMLReport(self):
        return self.__W3afXMLReport

    @W3afXMLReport.setter
    def W3afXMLReport(self, W3afXMLReport):
        self.__W3afXMLReport = self.__ResultDir + "/" + W3afXMLReport

    @property
    def W3afHTMLReport(self):
        return self.__W3afHTMLReport

    @W3afHTMLReport.setter
    def W3afHTMLReport(self, W3afHTMLReport):
        self.__W3afHTMLReport = self.__ResultDir + "/" + W3afHTMLReport

    @property
    def W3afHTTPOut(self):
        return self.__W3afHTTPOut

    @W3afHTTPOut.setter
    def W3afHTTPOut(self, W3afHTTPOut):
        self.__W3afHTTPOut = self.__ResultDir + "/" + W3afHTTPOut

    @property
    def W3afRepOut(self):
        return self.__W3afRepOut

    @W3afRepOut.setter
    def W3afRepOut(self, W3afRepOut):
        self.__W3afRepOut = self.__ResultDir + "/" + W3afRepOut

    @property
    def W3afRunLog(self):
        return self.__W3afRunLog

    @W3afRunLog.setter
    def W3afRunLog(self, W3afRunLog):
        self.__W3afRunLog = self.__ResultDir + "/" + W3afRunLog

    @property
    def W3afWassLog(self):
        return self.__W3afWassLog

    @W3afWassLog.setter
    def W3afWassLog(self, W3afWassLog):
        self.__W3afWassLog = self.__ResultDir + "/" + W3afWassLog

    @property
    def WapitiVersion(self):
        return self.__WapitiVersion

    @WapitiVersion.setter
    def WapitiVersion(self, WapitiVersion):
        self.__WapitiVersion = WapitiVersion

    @property
    def WapitiCMD(self):
        return self.__WapitiCMD

    @WapitiCMD.setter
    def WapitiCMD(self, WapitiCMD):
        self.__WapitiCMD = WapitiCMD

    @property
    def WapitiCLI(self):
        return self.__WapitiCLI

    @WapitiCLI.setter
    def WapitiCLI(self, WapitiCLI):
        self.__WapitiCLI = WapitiCLI

    @property
    def WapitiArguments(self):
        return self.__WapitiArguments

    @WapitiArguments.setter
    def WapitiArguments(self, WapitiArguments):
        self.__WapitiArguments = WapitiArguments

    @property
    def WapitiXMLReport(self):
        return self.__WapitiXMLReport

    @WapitiXMLReport.setter
    def WapitiXMLReport(self, WapitiXMLReport):
        self.__WapitiXMLReport = self.__ResultDir + "/" + WapitiXMLReport

    @property
    def WapitiRunLog(self):
        return self.__WapitiRunLog

    @WapitiRunLog.setter
    def WapitiRunLog(self, WapitiRunLog):
        self.__WapitiRunLog = self.__ResultDir + "/" + WapitiRunLog

    @property
    def WapitiWassLog(self):
        return self.__WapitiWassLog

    @WapitiWassLog.setter
    def WapitiWassLog(self, WapitiWassLog):
        self.__WapitiWassLog = self.__ResultDir + "/" + WapitiWassLog

    @property
    def WhatWebVersion(self):
        return self.__WhatWebVersion

    @WhatWebVersion.setter
    def WhatWebVersion(self, WhatWebVersion):
        self.__WhatWebVersion = WhatWebVersion

    @property
    def WhatWebCMD(self):
        return self.__WhatWebCMD

    @WhatWebCMD.setter
    def WhatWebCMD(self, WhatWebCMD):
        self.__WhatWebCMD = WhatWebCMD

    @property
    def WhatWebCLI(self):
        return self.__WhatWebCLI

    @WhatWebCLI.setter
    def WhatWebCLI(self, WhatWebCLI):
        self.__WhatWebCLI = WhatWebCLI

    @property
    def WhatWebArguments(self):
        return self.__WhatWebArguments

    @WhatWebArguments.setter
    def WhatWebArguments(self, WhatWebArguments):
        self.__WhatWebArguments = WhatWebArguments

    @property
    def WhatWebXMLReport(self):
        return self.__WhatWebXMLReport

    @WhatWebXMLReport.setter
    def WhatWebXMLReport(self, WhatWebXMLReport):
        self.__WhatWebXMLReport = self.__ResultDir + "/" + WhatWebXMLReport

    @property
    def WhatWebRunLog(self):
        return self.__WhatWebRunLog

    @WhatWebRunLog.setter
    def WhatWebRunLog(self, WhatWebRunLog):
        self.__WhatWebRunLog = self.__ResultDir + "/" + WhatWebRunLog

    @property
    def WhatWebWassLog(self):
        return self.__WhatWebWassLog

    @WhatWebWassLog.setter
    def WhatWebWassLog(self, WhatWebWassLog):
        self.__WhatWebWassLog = self.__ResultDir + "/" + WhatWebWassLog

    @property
    def WhoisVersion(self):
        return self.__WhoisVersion

    @WhoisVersion.setter
    def WhoisVersion(self, WhoisVersion):
        self.__WhoisVersion = WhoisVersion

    @property
    def WhoisCMD(self):
        return self.__WhoisCMD

    @WhoisCMD.setter
    def WhoisCMD(self, WhoisCMD):
        self.__WhoisCMD = WhoisCMD

    @property
    def WhoisWassLog(self):
        return self.__WhoisWassLog

    @WhoisWassLog.setter
    def WhoisWassLog(self, WhoisWassLog):
        self.__WhoisWassLog = self.__ResultDir + "/" + WhoisWassLog

    @property
    def WhoisTargetXMLReport(self):
        return self.__WhoisTargetXMLReport

    @WhoisTargetXMLReport.setter
    def WhoisTargetXMLReport(self, WhoisTargetXMLReport):
        self.__WhoisTargetXMLReport = self.__ResultDir + "/" + WhoisTargetXMLReport

    @property
    def WhoisTargetIPXMLReport(self):
        return self.__WhoisTargetIPXMLReport

    @WhoisTargetIPXMLReport.setter
    def WhoisTargetIPXMLReport(self, WhoisTargetIPXMLReport):
        self.__WhoisTargetIPXMLReport = self.__ResultDir + "/" + WhoisTargetIPXMLReport

    @property
    def OpenVASVersion(self):
        return self.__OpenVASVersion

    @OpenVASVersion.setter
    def OpenVASVersion(self, OpenVASVersion):
        self.__OpenVASVersion = OpenVASVersion

    @property
    def OpenVASCMD(self):
        return self.__OpenVASCMD

    @OpenVASCMD.setter
    def OpenVASCMD(self, OpenVASCMD):
        self.__OpenVASCMD = OpenVASCMD

    @property
    def OpenVASUser(self):
        return self.__OpenVASUser

    @OpenVASUser.setter
    def OpenVASUser(self, OpenVASUser):
        self.__OpenVASUser = OpenVASUser

    @property
    def OpenVASPassword(self):
        return self.__OpenVASPassword

    @OpenVASPassword.setter
    def OpenVASPassword(self, OpenVASPassword):
        self.__OpenVASPassword = OpenVASPassword

    @property
    def OpenVASHost(self):
        return self.__OpenVASHost

    @OpenVASHost.setter
    def OpenVASHost(self, OpenVASHost):
        self.__OpenVASHost = OpenVASHost

    @property
    def OpenVASPortListID(self):
        return self.__OpenVASPortListID

    @OpenVASPortListID.setter
    def OpenVASPortListID(self, OpenVASPortListID):
        self.__OpenVASPortListID = OpenVASPortListID

    @property
    def OpenVASTargetID(self):
        return self.__OpenVASTargetID

    @OpenVASTargetID.setter
    def OpenVASTargetID(self, OpenVASTargetID):
        self.__OpenVASTargetID = OpenVASTargetID

    @property
    def OpenVASNewConfigID(self):
        return self.__OpenVASNewConfigID

    @OpenVASNewConfigID.setter
    def OpenVASNewConfigID(self, OpenVASNewConfigID):
        self.__OpenVASNewConfigID = OpenVASNewConfigID

    @property
    def OpenVASTaskID(self):
        return self.__OpenVASTaskID

    @OpenVASTaskID.setter
    def OpenVASTaskID(self, OpenVASTaskID):
        self.__OpenVASTaskID = OpenVASTaskID

    @property
    def OpenVASTaskReportID(self):
        return self.__OpenVASTaskReportID

    @OpenVASTaskReportID.setter
    def OpenVASTaskReportID(self, OpenVASTaskReportID):
        self.__OpenVASTaskReportID = OpenVASTaskReportID

    @property
    def OpenVASTargetStatus(self):
        return self.__OpenVASTargetStatus

    @OpenVASTargetStatus.setter
    def OpenVASTargetStatus(self, OpenVASTargetStatus):
        self.__OpenVASTargetStatus = OpenVASTargetStatus

    @property
    def OpenVASConfigStatus(self):
        return self.__OpenVASConfigStatus

    @OpenVASConfigStatus.setter
    def OpenVASConfigStatus(self, OpenVASConfigStatus):
        self.__OpenVASConfigStatus = OpenVASConfigStatus

    @property
    def OpenVASConfigModifyVHOSTSStatus(self):
        return self.__OpenVASConfigModifyVHOSTSStatus

    @OpenVASConfigModifyVHOSTSStatus.setter
    def OpenVASConfigModifyVHOSTSStatus(self, OpenVASConfigModifyVHOSTSStatus):
        self.__OpenVASConfigModifyVHOSTSStatus = OpenVASConfigModifyVHOSTSStatus

    @property
    def OpenVASConfigModifyVHOSTSIPStatus(self):
        return self.__OpenVASConfigModifyVHOSTSIPStatus

    @OpenVASConfigModifyVHOSTSIPStatus.setter
    def OpenVASConfigModifyVHOSTSIPStatus(self, OpenVASConfigModifyVHOSTSIPStatus):
        self.__OpenVASConfigModifyVHOSTSIPStatus = OpenVASConfigModifyVHOSTSIPStatus

    @property
    def OpenVASTaskStatus(self):
        return self.__OpenVASTaskStatus

    @OpenVASTaskStatus.setter
    def OpenVASTaskStatus(self, OpenVASTaskStatus):
        self.__OpenVASTaskStatus = OpenVASTaskStatus

    @property
    def OpenVASTaskProgress(self):
        return self.__OpenVASTaskProgress

    @OpenVASTaskProgress.setter
    def OpenVASTaskProgress(self, OpenVASTaskProgress):
        self.__OpenVASTaskProgress = OpenVASTaskProgress

    @property
    def OpenVASXMLReport(self):
        return self.__OpenVASXMLReport

    @OpenVASXMLReport.setter
    def OpenVASXMLReport(self, OpenVASXMLReport):
        self.__OpenVASXMLReport = self.__ResultDir + "/" + OpenVASXMLReport

    @property
    def OpenVASWassLog(self):
        return self.__OpenVASWassLog

    @OpenVASWassLog.setter
    def OpenVASWassLog(self, OpenVASWassLog):
        self.__OpenVASWassLog = self.__ResultDir + "/" + OpenVASWassLog

    @property
    def ZAProxyVersion(self):
        return self.__ZAProxyVersion

    @ZAProxyVersion.setter
    def ZAProxyVersion(self, ZAProxyVersion):
        self.__ZAProxyVersion = ZAProxyVersion

    @property
    def ZAProxyPath(self):
        return self.__ZAProxyPath

    @ZAProxyPath.setter
    def ZAProxyPath(self, ZAProxyPath):
        self.__ZAProxyPath = ZAProxyPath

    @property
    def ZAProxyCMD(self):
        return self.__ZAProxyCMD

    @ZAProxyCMD.setter
    def ZAProxyCMD(self, ZAProxyCMD):
        self.__ZAProxyCMD = ZAProxyCMD

    @property
    def ZAProxyIsRunning(self):
        return self.__ZAProxyIsRunning

    @ZAProxyIsRunning.setter
    def ZAProxyIsRunning(self, ZAProxyIsRunning):
        self.__ZAProxyIsRunning = ZAProxyIsRunning

    @property
    def ZAProxyRunningPid(self):
        return self.__ZAProxyRunningPid

    @ZAProxyRunningPid.setter
    def ZAProxyRunningPid(self, ZAProxyRunningPid):
        self.__ZAProxyRunningPid = ZAProxyRunningPid

    @property
    def ZAProxyCLI(self):
        return self.__ZAProxyCLI

    @ZAProxyCLI.setter
    def ZAProxyCLI(self, ZAProxyCLI):
        self.__ZAProxyCLI = ZAProxyCLI

    @property
    def ZAProxyDaemon(self):
        return self.__ZAProxyDaemon

    @ZAProxyDaemon.setter
    def ZAProxyDaemon(self, ZAProxyDaemon):
        self.__ZAProxyDaemon = ZAProxyDaemon

    @property
    def ZAProxyAlertThreshold(self):
        return self.__ZAProxyAlertThreshold

    @ZAProxyAlertThreshold.setter
    def ZAProxyAlertThreshold(self, ZAProxyAlertThreshold):
        self.__ZAProxyAlertThreshold = ZAProxyAlertThreshold.upper()

    @property
    def ZAProxyAttackStrength(self):
        return self.__ZAProxyAttackStrength

    @ZAProxyAttackStrength.setter
    def ZAProxyAttackStrength(self, ZAProxyAttackStrength):
        self.__ZAProxyAttackStrength = ZAProxyAttackStrength.upper()

    @property
    def ZAProxyStart(self):
        return self.__ZAProxyStart

    @ZAProxyStart.setter
    def ZAProxyStart(self, ZAProxyStart):
        self.__ZAProxyStart = ZAProxyStart

    @property
    def ZAProxyStop(self):
        return self.__ZAProxyStop

    @ZAProxyStop.setter
    def ZAProxyStop(self, ZAProxyStop):
        self.__ZAProxyStop = ZAProxyStop

    @property
    def ZAProxyXMLReport(self):
        return self.__ZAProxyXMLReport

    @ZAProxyXMLReport.setter
    def ZAProxyXMLReport(self, ZAProxyXMLReport):
        self.__ZAProxyXMLReport = ZAProxyXMLReport

    @property
    def ZAProxySessionFile(self):
        return self.__ZAProxySessionFile

    @ZAProxySessionFile.setter
    def ZAProxySessionFile(self, ZAProxySessionFile):
        self.__ZAProxySessionFile = ZAProxySessionFile

    @property
    def ZAProxySessionDataFile(self):
        return self.__ZAProxySessionDataFile

    @ZAProxySessionDataFile.setter
    def ZAProxySessionDataFile(self, ZAProxySessionDataFile):
        self.__ZAProxySessionDataFile = ZAProxySessionDataFile

    @property
    def ZAProxySessionLCKFile(self):
        return self.__ZAProxySessionLCKFile

    @ZAProxySessionLCKFile.setter
    def ZAProxySessionLCKFile(self, ZAProxySessionLCKFile):
        self.__ZAProxySessionLCKFile = ZAProxySessionLCKFile

    @property
    def ZAProxySessionLogFile(self):
        return self.__ZAProxySessionLogFile

    @ZAProxySessionLogFile.setter
    def ZAProxySessionLogFile(self, ZAProxySessionLogFile):
        self.__ZAProxySessionLogFile = ZAProxySessionLogFile

    @property
    def ZAProxySessionPropertiesFile(self):
        return self.__ZAProxySessionPropertiesFile

    @ZAProxySessionPropertiesFile.setter
    def ZAProxySessionPropertiesFile(self, ZAProxySessionPropertiesFile):
        self.__ZAProxySessionPropertiesFile = ZAProxySessionPropertiesFile

    @property
    def ZAProxySessionScriptFile(self):
        return self.__ZAProxySessionScriptFile

    @ZAProxySessionScriptFile.setter
    def ZAProxySessionScriptFile(self, ZAProxySessionScriptFile):
        self.__ZAProxySessionScriptFile = ZAProxySessionScriptFile

    @property
    def ZAProxyWassLog(self):
        return self.__ZAProxyWassLog

    @ZAProxyWassLog.setter
    def ZAProxyWassLog(self, ZAProxyWassLog):
        self.__ZAProxyWassLog = self.__ResultDir + "/" + ZAProxyWassLog

    @property
    def ResultDir(self):
        return self.__ResultDir

    @ResultDir.setter
    def ResultDir(self, ResultDir):
        self.__ResultDir = ResultDir

    @property
    def ReportDate(self):
        return self.__ReportDate

    @property
    def ToDay(self):
        return self.__ToDay
