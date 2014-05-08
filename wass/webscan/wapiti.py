'''
wapiti.py

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


class WassWapiti(object):
    '''
    This is the WassWapiti class
    '''

    def __init__(self, wass):
        '''
        Initialize WassWapiti module
        '''
        self.wass = wass

    def WapitiCLi(self):
        '''
        Build the Wapiti CLI Command
        '''
        f_args = ''
        if ((self.wass.WapitiArguments is not None) or (self.wass.WapitiArguments != '')):
            f_args = self.wass.WapitiArguments
        arguments = self.wass.WapitiCMD
        arguments += ' ' + self.wass.ScanTarget
        if (self.wass.TargetExcludeURLS is not None):
            for excludeurl in self.wass.TargetExcludeURLS:
                arguments += ' -x ' + self.wass.ScanTarget + excludeurl
        if (self.wass.UseLocalZAProxy == True):
            arguments += ' -p ' + self.wass.LocalZAProxy + '/'
        arguments += ' -f xml -o ' + self.wass.WapitiXMLReport
        arguments += ' ' + f_args
        self.wass.WapitiCLI = arguments

    def RunWapiti(self):
        '''
        Run the Wapiti CLI Command
        '''
        self.wass.CurrentTask = "Wapiti"
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.WapitiWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.WapitiXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        self.wass.WapitiRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.WassGetVersion._GetWapitiVersion()
        self.wass.WassLogging.CreateLogfile(self.wass.WapitiWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### Wapiti WASS Run Starting ###############")
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == False):
                self.wass.WassZAProxy.startZAProxy()
        self.WapitiCLi()
        self.wass.WassCommon.runCommand(self.wass.WapitiCLI, self.wass.WapitiRunLog)
        self.wass.WassLogging.info("############### Wapiti WASS Run Done ###############")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging .info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)

        if (os.path.isfile(os.path.expanduser('~') + '/.wapiti/scans/' + self.wass.TargetDomain + '.xml')):
            wapiti_scan_xml = os.path.expanduser('~') + '/.wapiti/scans/' + self.wass.TargetDomain + '.xml'
            self.wass.WassCommon.moveResultFile(wapiti_scan_xml, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.WapitiXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.WapitiRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        if (self.wass.UseLocalZAProxy == True):
            if ((self.wass.ZAProxyIsRunning == True) and (self.wass.Program != "ALL")):
                self.wass.WassZAProxy.stopZAProxy()
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.WapitiWassLog, finalResultDir)
