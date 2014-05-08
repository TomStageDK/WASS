'''
whatweb.py

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


class WassWhatWeb(object):
    '''
    This is the WassWhatWeb class
    '''

    def __init__(self, wass):
        '''
        Initialize WassWhatWeb module
        '''
        self.wass = wass

    def WhatWebCLi(self):
        '''
        Build the WhatWeb CLI Command
        '''
        f_args = ''
        if (self.wass.WhatWebArguments is not None):
            f_args = self.wass.WhatWebArguments
        arguments = self.wass.WhatWebCMD
        arguments += ' ' + self.wass.ScanTarget
        arguments += ' --log-xml ' + self.wass.WhatWebXMLReport
        if (self.wass.UseLocalZAProxy == True):
            arguments += ' --proxy ' + self.wass.LocalZAProxyHost + ":" + self.wass.LocalZAProxyPort
        arguments += ' --color never '
        arguments += ' ' + f_args
        self.wass.WhatWebCLI = arguments

    def RunWhatWeb(self):
        '''
        Run the WhatWeb CLI Command
        '''
        self.wass.CurrentTask = "WhatWeb"
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.WhatWebWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.WhatWebXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        self.wass.WhatWebRunLog = self.wass.CurrentTask + "_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.WassGetVersion._GetWhatWebVersion()
        self.wass.WassLogging.CreateLogfile(self.wass.WhatWebWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### WhatWeb WASS Run Starting ###############")
        self.wass.WassLogging.debug("Should we start the ZAProxy: %s" % self.wass.UseLocalZAProxy)
        if (self.wass.UseLocalZAProxy == True):
            if (self.wass.ZAProxyIsRunning == False):
                self.wass.WassZAProxy.startZAProxy()
        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
        self.WhatWebCLi()
        self.wass.WassCommon.runCommand(self.wass.WhatWebCLI, self.wass.WhatWebRunLog)
        self.wass.WassLogging.info("############### WhatWeb WASS Run Done ###############")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging .info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)

        self.wass.WassCommon.moveResultFile(self.wass.WhatWebXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.WhatWebRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        if (self.wass.UseLocalZAProxy == True):
            if ((self.wass.ZAProxyIsRunning == True) and (self.wass.Program != "ALL")):
                self.wass.WassZAProxy.stopZAProxy()
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.WhatWebWassLog, finalResultDir)
