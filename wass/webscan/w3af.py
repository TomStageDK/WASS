'''
w3af.py

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
#TODO: Make sure that this works with w3af version 1.1
#TODO: Implement the new and improved W3af version 1.6

__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.04.27'

import os


class WassW3af(object):
    '''
    This is the WassW3af class
    '''

    def __init__(self, wass):
        '''
        Initialize WassW3af module
        '''
        self.wass = wass

    def W3afCLI(self):
        '''
        Build the W3af CLI Command
        '''
#       # Building the CLI Command
        arguments = self.wass.W3afCMD
        arguments += ' -s ' + self.wass.W3afCMDFile
        self.wass.W3afCLI = arguments

    def RunW3af(self):
        '''
        Run the W3af CLI Command
        '''
        self.wass.CurrentTask = "W3af"
        # Setup the files that w3af will create during the run
        self.wass.W3afWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.W3afRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.W3afXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        self.wass.W3afHTMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".html"
        self.wass.W3afHTTPOut = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".http"
        self.wass.W3afRepOut = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".rep"
        self.wass.W3afCMDFile = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".cmd"
        # Get the w3af Version
        self.wass.WassGetVersion._GetW3afVersion()
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.WassLogging.CreateLogfile(self.wass.W3afWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### W3af WASS Run Starting ###############")
        self.wass.WassLogging.debug("Should we start the ZAProxy: %s" % self.wass.UseLocalZAProxy)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == False):
                self.wass.WassZAProxy.startZAProxy()
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        self.createCMD()
        self.W3afCLI()
        self.wass.WassCommon.runCommand(self.wass.W3afCLI, self.wass.W3afRunLog)
        self.wass.WassLogging.info("############### W3af WASS Run Done ###############")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging.info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.W3afXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.W3afHTMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.W3afHTTPOut, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.W3afRepOut, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.W3afCMDFile, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.W3afRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        if (self.wass.UseLocalZAProxy == True):
            if ((self.wass.ZAProxyIsRunning == True) and (self.wass.Program != "ALL")):
                self.wass.WassZAProxy.stopZAProxy()
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.W3afWassLog, finalResultDir)

    def createCMD(self):
        self.wass.WassLogging.info("############### Entering createCMD ###############")
        self.wass.WassLogging.debug("The W3afCMDFile is: %s" % self.wass.W3afCMDFile)
        self.wass.WassLogging.debug("The W3afHTTPOut is: %s" % self.wass.W3afHTTPOut)
        self.wass.WassLogging.debug("The W3afRepOut is: %s" % self.wass.W3afRepOut)
        self.wass.WassLogging.debug("The W3afXMLReport is: %s" % self.wass.W3afXMLReport)
        self.wass.WassLogging.debug("The W3afHTMLReport is: %s" % self.wass.W3afHTMLReport)
        self.wass.WassLogging.debug("The ScanTarget is: %s" % self.wass.ScanTarget)
        cmd_file = open(self.wass.W3afCMDFile, "w", 0)
        if (self.wass.W3afVersion == '1.1'):
            cmd_file.write("profiles use " + self.wass.W3afProfile + "\n")
            cmd_file.write("plugins\n")
            cmd_file.write("output textFile,xmlFile,htmlFile\n")
            cmd_file.write("output config textFile\n")
            cmd_file.write("set verbose False\n")
            cmd_file.write("set httpFileName " + self.wass.W3afHTTPOut + "\n")
            cmd_file.write("set fileName " + self.wass.W3afRepOut + "\n")
            cmd_file.write("back\n")
            cmd_file.write("output config xmlFile\n")
            cmd_file.write("set fileName " + self.wass.W3afXMLReport + "\n")
            cmd_file.write("back\n")
            cmd_file.write("output config htmlFile\n")
            cmd_file.write("set fileName " + self.wass.W3afHTMLReport + "\n")
            cmd_file.write("back\n")
            cmd_file.write("back\n")
            cmd_file.write("target\n")
            cmd_file.write("set target " + self.wass.ScanTarget + "\n")
            cmd_file.write("back\n")
            cmd_file.write("start\n")
            cmd_file.write("exit\n")
            cmd_file.close()
        elif (self.wass.W3afVersion == '1.6'):
            cmd_file.write("profiles use " + self.wass.W3afProfile + "\n")
            cmd_file.write("plugins\n")
            cmd_file.write("output console,text_file,xml_file,html_file\n")
            if (self.wass.LogLevel == 'DEBUG'):
                cmd_file.write("output config console\n")
                cmd_file.write("set verbose True\n")
            else:
                cmd_file.write("output config console\n")
                cmd_file.write("set verbose False\n")
            cmd_file.write("back\n")
            cmd_file.write("output config text_file\n")
            cmd_file.write("set verbose True\n")
            cmd_file.write("set http_output_file " + self.wass.W3afHTTPOut + "\n")
            cmd_file.write("set output_file " + self.wass.W3afRepOut + "\n")
            cmd_file.write("back\n")
            cmd_file.write("output config xml_file\n")
            cmd_file.write("set output_file " + self.wass.W3afXMLReport + "\n")
            cmd_file.write("back\n")
            cmd_file.write("output config html_file\n")
            cmd_file.write("set output_file " + self.wass.W3afHTMLReport + "\n")
            cmd_file.write("set verbose False\n")
            cmd_file.write("back\n")
            w3af_installation_path, w3af_command = os.path.split(self.wass.W3afCMD)
            cmd_file.write("audit config ssl_certificate\n")
            cmd_file.write("set minExpireDays 30\n")
            cmd_file.write("set caFileName " + w3af_installation_path + "/w3af/plugins/audit/ssl_certificate/ca.pem\n")
            cmd_file.write("back\n")
            if (self.wass.TargetExcludeURLSRegex is not None):
                cmd_file.write("crawl config web_spider\n")
                cmd_file.write("set ignore_regex " + self.wass.TargetExcludeURLSRegex + "\n")
                cmd_file.write("back\n")
            cmd_file.write("back\n")
            if (self.wass.UseLocalZAProxy == True):
                cmd_file.write("http-settings\n")
                cmd_file.write("set proxy_port " + self.wass.LocalZAProxyPort + "\n")
                cmd_file.write("set proxy_address " + self.wass.LocalZAProxyHost + "\n")
                cmd_file.write("back\n")
            cmd_file.write("target\n")
            cmd_file.write("set target " + self.wass.ScanTarget + "\n")
            cmd_file.write("back\n")
            cmd_file.write("start\n")
            cmd_file.write("exit\n")
            cmd_file.close()
        self.wass.WassLogging.info("############### Leaving createCMD ###############")
