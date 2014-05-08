'''
skipfish.py

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
#TODO: Fix the ZIP archiving of the Result directory
#TODO: Make it work with the downloaded Skipfish v 2.10b

__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.04.27'

import os


class WassSkipfish(object):
    '''
    This is the WassSkipfish class
    '''

    def __init__(self, wass):
        '''
        Initialize WassSkipfish module
        '''
        self.wass = wass

    def SkipfishCLI(self):
        '''
        Build the Skipfish CLI Command
        '''
#       # Building the CLI Command
#        -e "+objSkipFish['scanTarget']
        f_args = ''
        if ((self.wass.SkipfishArguments is not None) or (self.wass.SkipfishArguments != '')):
            f_args = self.wass.SkipfishArguments
        arguments = self.wass.SkipfishCMD
        arguments += ' -I ' + self.wass.ScanTarget
        arguments += ' -o ' + self.wass.SkipfishOutputDir
        arguments += ' -W ' + self.wass.SkipfishScanWordList
        if (self.wass.SkipfishWordList is not None):
            arguments += ' -S ' + self.wass.SkipfishWordList
        if (self.wass.TargetExcludeURLS is not None):
            for exclude_url in self.wass.TargetExcludeURLS:
                arguments += ' -x ' + exclude_url
        arguments += ' ' + f_args
        arguments += ' ' + self.wass.ScanTarget
        self.wass.SkipfishCLI = arguments

    def RunSkipfish(self):
        '''
        Run the Skipfish with the CLI Command
        '''
        self.wass.CurrentTask = "Skipfish"
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.SkipfishOutputDir = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate
        self.wass.SkipfishWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.SkipfishRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.SkipfishScanWordList = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".wl"
        self.wass.WassGetVersion._GetSkipfishVersion()
        # Creating the Word List File for the Target scan
        outputFile = open(self.wass.SkipfishScanWordList, "w")
        outputFile.close()

        self.wass.WassLogging.CreateLogfile(self.wass.SkipfishWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### Skipfish WASS Run Starting ###############")
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        self.SkipfishCLI()
        if (self.wass.SkipfishVersion == '2.10b'):
            self.wass.WassLogging.debug("Skipfish Version detected is >= 2.10b")
            self.wass.WassLogging.debug("Changing to the Skipfish installation directory")
            path, file = os.path.split(self.wass.SkipfishCMD)
            os.chdir(path)
        self.wass.WassCommon.runCommand(self.wass.SkipfishCLI, self.wass.SkipfishRunLog)
        if (self.wass.SkipfishVersion == '2.10b'):
            self.wass.WassLogging.debug("Because we found Skipfish version >= 2.10b we need to change back to the OrgWorkingDir")
            os.chdir(self.wass.OrgWorkingDir)
        self.wass.WassLogging.info("############### Skipfish WASS Run Done ###############")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging .info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.SkipfishRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.SkipfishScanWordList, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.SkipfishScanWordList + '.old', finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.SkipfishOutputDir, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.SkipfishWassLog, finalResultDir)
