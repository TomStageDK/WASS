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


class WassTheHarvester(object):
    '''
    This is the WassTheHarvester class
    '''

    def __init__(self, wass):
        '''
        Initialize WassTheHarvester module
        '''
        self.wass = wass

    def TheHarvesterCLI(self):
        '''
        Build the TheHarvester CLI Command
        '''
#       # Building the CLI Command
        arguments = self.wass.TheHarvesterCMD
        f_args = ''
        if ((self.wass.TheHarvesterArguments is not None) or (self.wass.TheHarvesterArguments != '')):
            f_args = self.wass.TheHarvesterArguments
        arguments += ' -f ' + self.wass.TheHarvesterReportName
        if (f_args != None):
            arguments += ' ' + f_args
        arguments += ' -d ' + self.wass.TldDomainName
        self.wass.TheHarvesterCLI = arguments

    def RunTheHarvester(self):
        '''
        Run the TheHarvester CLI Command
        '''
        self.wass.CurrentTask = "TheHarvester"
        # Setup the files that SSLScan will create during the run
        self.wass.TheHarvesterWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.TheHarvesterRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.TheHarvesterReportName = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate
        # Get the SSLScan Version
        self.wass.WassGetVersion._GetTheHarvesterVersion()
        # Setup the logging, we are about to use it in wass.common.WassCommon.Common !!!!!
        self.wass.WassLogging.CreateLogfile(self.wass.TheHarvesterWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### TheHarvester WASS Run Starting ###############")
        self.wass.WassLogging.debug("Should we start the ZAProxy: %s" % self.wass.UseLocalZAProxy)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == False):
                self.wass.WassZAProxy.startZAProxy()

        # Create the CLI for the run
        self.TheHarvesterCLI()
        # Run the command
        self.wass.WassCommon.runCommand(self.wass.TheHarvesterCLI, self.wass.TheHarvesterRunLog)
        self.wass.WassLogging.info("############### TheHarvester WASS Run Done ###############")
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging.info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.TheHarvesterRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.TheHarvesterReportName + '.xml', finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.TheHarvesterReportName + '.html', finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == True and self.wass.Program != "ALL"):
                self.wass.WassZAProxy.stopZAProxy()
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.TheHarvesterWassLog, finalResultDir)
