'''
sslyze.py

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


class WassSSLyze(object):
    '''
    This is the WassSSLyze class
    '''

    def __init__(self, wass):
        '''
        Initialize WassSSLyze module
        '''
        self.wass = wass

    def SSLyzeCLI(self):
        '''
        Build the SSLyze CLI Command
        '''
#       # Building the CLI Command
        arguments = self.wass.SSLyzeCMD
        f_args = ''
        if ((self.wass.SSLyzeArguments is not None) or (self.wass.SSLyzeArguments != '')):
            f_args = self.wass.SSLyzeArguments
        arguments += ' --xml_out ' + self.wass.SSLyzeXMLReport
        arguments += ' --regular'
        if (self.wass.UseLocalZAProxy == True):
            arguments += ' --https_tunnel ' + self.wass.LocalZAProxy
        arguments += ' --certinfo full'
        if (f_args != None):
            arguments += f_args
        arguments += ' ' + self.wass.ScanTarget
        self.wass.SSLyzeCLI = arguments

    def RunSSLyze(self):
        '''
        Run the SSLyze CLI Command
        '''
        self.wass.CurrentTask = "SSLyze"
        # Setup the files that SSLyze will create during the run
        self.wass.SSLyzeWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.SSLyzeRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.SSLyzeXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        # Get the SSLyze Version
        self.wass.WassGetVersion._GetSSLyzeVersion()
        # Setup the logging, we are about to use it in wass.common.WassCommon.Common !!!!!
        self.wass.WassLogging.CreateLogfile(self.wass.SSLyzeWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### SSLyze WASS Run Starting ###############")
        self.wass.WassLogging.debug("Should we start the ZAProxy: %s" % self.wass.UseLocalZAProxy)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == False):
                self.wass.WassZAProxy.startZAProxy()

        # Create the CLI for the run
        self.SSLyzeCLI()
        # Run the command
        self.wass.WassCommon.runCommand(self.wass.SSLyzeCLI, self.wass.SSLyzeRunLog)
        self.wass.WassLogging.info("############### SSLyze WASS Run Done ###############")
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging.info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.SSLyzeRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.SSLyzeXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == True and self.wass.Program != "ALL"):
                self.wass.WassZAProxy.stopZAProxy()
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.SSLyzeWassLog, finalResultDir)
