'''
fierce.py

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


class WassFierce(object):
    '''
    This is the WassFierce class
    '''

    def __init__(self, wass):
        '''
        Initialize WassFierce module
        '''
        self.wass = wass

    def FierceCLI(self):
        '''
        Build the Fierce CLI Command
        '''
#       # Building the CLI Command
        arguments = self.wass.FierceCMD
        f_args = ''
        if ((self.wass.FierceArguments is not None) or (self.wass.FierceArguments != '')):
            f_args = self.wass.FierceArguments
        arguments += ' -format xml'
        arguments += ' -output ' + self.wass.FierceXMLReport
        fierce_path, fierce_cmd =  os.path.split(self.wass.FierceCMD)
        arguments += ' -template ' + fierce_path + '/tt'
        if (self.wass.LogLevel == 'DEBUG'):
            arguments += ' -debug '
        if (f_args != None):
            arguments += f_args
        arguments += ' -dns ' + self.wass.TldDomainName
        self.wass.FierceCLI = arguments

    def RunFierce(self):
        '''
        Run the Fierce CLI Command
        '''
        self.wass.CurrentTask = "Fierce"
        # Setup the files that Fierce will create during the run
        self.wass.FierceWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.FierceRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.FierceXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        # Get the SSLScan Version
        self.wass.WassGetVersion._GetFierceVersion()
        # Setup the logging, we are about to use it in wass.common.WassCommon.Common !!!!!
        self.wass.WassLogging.CreateLogfile(self.wass.FierceWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### Fierce WASS Run Starting ###############")

        # Create the CLI for the run
        self.FierceCLI()
        # Run the command
        self.wass.WassCommon.runCommand(self.wass.FierceCLI, self.wass.FierceRunLog)
        self.wass.WassLogging.info("############### Fierce WASS Run Done ###############")
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging.info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.FierceRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.FierceXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.FierceWassLog, finalResultDir)
