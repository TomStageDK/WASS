'''
nikto.py

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


class WassNikto(object):
    '''
    This is the WassNikto class
    '''

    def __init__(self, wass):
        '''
        Initialize WassNikto module
        '''
        self.wass = wass

    def NiktoUpdate(self):
        '''
        Build the Nikto CLI Update Command
        '''
        self.wass.CurrentTask = "Nikto"
        self.wass.NiktoWassLog = self.wass.CurrentTask + "_Update_" + self.wass.ReportDate + ".log"
        self.wass.NiktoRunLog = self.wass.CurrentTask + "_Run_Update_" + self.wass.ReportDate + ".log"
        self.wass.WassLogging.CreateLogfile(self.wass.NiktoWassLog)
        self.wass.WassCommon.printInfo()

        self.wass.WassLogging.info("Nikto WASS Update Run Start")
        arguments = self.wass.NiktoCMD
        arguments += " -update "
        self.wass.NiktoCLI = arguments
        runLog = self.wass.WassCommon.runCommand(self.wass.NiktoCLI)
        self.wass.WassLogging.info("Nikto WASS Update Run Done")
        self.wass.WassLogging.info("Writing the Nikto Update Run log: %s" % self.wass.NiktoRunLog)
        outputFile = open(self.wass.NiktoRunLog, "w", 0)
        outputFile.writelines(runLog)
        outputFile.close()

        self.wass.WassLogging.info("Writing the Nikto Run log Done")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging .info("The finalResultDir is: %s" % finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.NiktoRunLog, finalResultDir)
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.NiktoWassLog, finalResultDir)

    def NiktoCLi(self):
        '''
        Build the Nikto CLI Command
        '''
        if ((self.wass.NiktoArguments is not None) or (self.wass.NiktoArguments != '')):
            f_args = self.wass.NiktoArguments
        arguments = self.wass.NiktoCMD
        arguments += ' -h ' + self.wass.TargetDomain
        arguments += ' -vhost ' + self.wass.TargetDomain
        arguments += ' -port ' + str(self.wass.TargetPort)
        arguments += ' -root ' + self.wass.TargetURL
        if (self.wass.UseLocalZAProxy == True):
            arguments += ' -useproxy ' + self.wass.LocalZAProxy
        arguments += ' -ask no -output ' + self.wass.NiktoXMLReport + ' -Format xml'
        arguments += ' ' + f_args
        self.wass.NiktoCLI = arguments

    def RunNikto(self):
        '''
        Run the Nikto CLI Command
        '''
        self.wass.CurrentTask = "Nikto"
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.NiktoWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.NiktoXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        self.wass.NiktoRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.WassGetVersion._GetNiktoVersion()
        self.wass.WassLogging.CreateLogfile(self.wass.NiktoWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()
        #Make the 1st connection to the ScanTarget to see if everything is ready for the run
        self.wass.WassCommon.checkURL()

        self.wass.WassLogging.info("############### Nikto WASS Run Starting ###############")
        self.wass.WassLogging.debug("Should we start the ZAProxy: %s" % self.wass.UseLocalZAProxy)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == False):
                self.wass.WassZAProxy.startZAProxy()
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        self.NiktoCLi()
        self.wass.WassCommon.runCommand(self.wass.NiktoCLI, self.wass.NiktoRunLog)
        self.wass.WassLogging.info("############### Nikto WASS Run Done ###############")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging .info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.NiktoXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.NiktoRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        if (self.wass.UseLocalZAProxy == True):
            if ((self.wass.ZAProxyIsRunning == True) and (self.wass.Program != "ALL")):
                self.wass.WassZAProxy.stopZAProxy()
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.NiktoWassLog, finalResultDir)
