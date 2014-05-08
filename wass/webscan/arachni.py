'''
arachni.py

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

__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.04.27'

import os


class WassArachni(object):
    '''
    This is the WassArachni class
    '''

    def __init__(self, wass):
        '''
        Initialize WassArachni module
        '''
        self.wass = wass

    def ArachniCLi(self):
        '''
        Build the Arachni CLI Command
        '''
        self.wass.WassCommon.getURLExcludeRegex
        f_args = ''
        if ((self.wass.ArachniArguments is not None) or (self.wass.ArachniArguments != '')):
            f_args = self.wass.ArachniArguments
        arguments = self.wass.ArachniCMD
        arguments += " --authed-by='" + self.wass.ArachniAuthedBy + "'"
        if (self.wass.TargetExcludeURLSRegex != None):
            self.wass.WassLogging.debug("Arachni setting the Exclude urls to: %s" % self.wass.TargetExcludeURLSRegex)
            arguments += " --exclude='" + self.wass.TargetExcludeURLSRegex + "'"
        if (self.wass.UseLocalZAProxy == True):
            arguments += " --proxy=" + self.wass.LocalZAProxyHost + ":" + self.wass.LocalZAProxyPort
            arguments += " --proxy-type=" + self.wass.LocalZAProxyProtocol
        arguments += " --report=afr:outfile=" + self.wass.ArachniAFRReport
        arguments += " " + self.wass.ScanTarget
        if (f_args != None):
            arguments += f_args
        self.wass.ArachniCLI = arguments

    def CreateArachniReports(self):
        self.wass.WassLogging.info("############### Entering createReports ###############")
        #,xml:outfile="+objArachni['xmlReport']+",html:outfile="+objArachni['htmlReport']+"
        xmlCMD = self.wass.ArachniCMD + " --repload=" + self.wass.ArachniAFRReport + " --report=xml:outfile=" + self.wass.ArachniXMLReport
        htmlCMD = self.wass.ArachniCMD + " --repload=" + self.wass.ArachniAFRReport + " --report=html:outfile=" + self.wass.ArachniHTMLReport
        self.wass.WassLogging.info("Creating the XML report")
        self.wass.WassCommon.runCommand(xmlCMD, self.wass.ArachniRunLog)
        self.wass.WassLogging.info("Creating the HTML report")
        self.wass.WassCommon.runCommand(htmlCMD, self.wass.ArachniRunLog)
        self.wass.WassLogging.info("############### Leaving createReports ###############")

    def RunArachni(self):
        '''
        Run the Arachni CLI Command
        '''
        self.wass.CurrentTask = "Arachni"
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.ArachniWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.ArachniRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.ArachniAFRReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".afr"
        self.wass.ArachniXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        self.wass.ArachniHTMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".html"
        self.wass.ArachniErrorLog = "error.log"
        self.wass.WassGetVersion._GetArachniVersion()
        self.wass.WassLogging.CreateLogfile(self.wass.ArachniWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.debug("Should we start the ZAProxy: %s" % self.wass.UseLocalZAProxy)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == False):
                self.wass.WassZAProxy.startZAProxy()
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        self.ArachniCLi()
        self.wass.WassCommon.runCommand(self.wass.ArachniCLI, self.wass.ArachniRunLog)
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging.info("The finalResultDir is: %s" % finalResultDir)
        if (os.path.isfile(self.wass.ArachniErrorLog)):
            self.wass.WassLogging.info("The Arachni error.log exists something went wrong!!!")
            self.wass.WassLogging.info("Check the Arachni ERROR log for more information!!!")
            self.wass.WassLogging.info("It is located in " + finalResultDir)
            self.wass.WassCommon.moveResultFile(self.wass.ArachniErrorLog, finalResultDir)

        self.wass.WassLogging.info("The Arachni Run is done, creating additional Reports")
        self.CreateArachniReports()
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.ArachniAFRReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ArachniXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ArachniHTMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ArachniRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        if (self.wass.UseLocalZAProxy == True):
            if ((self.wass.ZAProxyIsRunning == True) and (self.wass.Program != "ALL")):
                self.wass.WassZAProxy.stopZAProxy()
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.ArachniWassLog, finalResultDir)
