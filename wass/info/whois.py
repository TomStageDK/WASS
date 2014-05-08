'''
whois.py

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

import pythonwhois


class WassWhoIS(object):
    '''
    This is the WASS WhoIS class
    '''

    def __init__(self, wass):
        '''
        Initialize WassWhoIS module
        '''
        self.wass = wass

    def RunWhoIS(self):
        '''
        Run the Whois CLI Command
        '''
        self.wass.CurrentTask = "Whois"
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.WhoisWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.WhoisTargetXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        self.wass.WassGetVersion._GetWhoisVersion()
        self.wass.WassLogging.CreateLogfile(self.wass.WhoisWassLog)
        self.wass.WassCommon.printInfo()

        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()
        self.wass.WhoisTargetIPXMLReport = self.wass.CurrentTask + "_" + self.wass.TargetIP + "_" + self.wass.ReportDate + ".xml"
        self.wass.WassLogging.info("############### Whois WASS Run Starting ###############")
        # Dont do a Whois lookup if the IP Address of the target is Private
        if (self.wass.TargetIPType == True):
            self.wass.WassLogging.info("The IP Address is a private one so we don't do the Whois Lookup")
        else:
            self.wass.WassLogging.info("The IP Address is a public one so we do the Whois Lookup")
            self.wass.WassLogging.info("The Whois query for the Domain is: %s " % self.wass.TldDomainName)
            self.wass.WassLogging.info("The Whois query for the IP Address is: %s " % self.wass.TargetIP)

            emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain
            emailBody += "\n\nFollowing is the Whois Lookup for the Top Level Domain Name:\n\n"
            tlDomain = pythonwhois.net.get_whois_raw(self.wass.TldDomainName)

            self.wass.WassXML.createWhoisXML(pythonwhois.get_whois(self.wass.TldDomainName), self.wass.TldDomainName, self.wass.WhoisTargetXMLReport)

            for line in tlDomain:
                emailBody += line

            emailBody += "\n\nFollowing is the Whois lookup on the IP Address:\n\n"

            tlDomain = pythonwhois.net.get_whois_raw(self.wass.TargetIP)
            self.wass.WassXML.createWhoisXML(pythonwhois.get_whois(self.wass.TargetIP), self.wass.TargetIP, self.wass.WhoisTargetIPXMLReport)
            for line in tlDomain:
                emailBody += line

            self.wass.WassLogging.infoNoFormatting(emailBody)

            if (self.wass.SendEmail):
                self.wass.WassCommon.SendEMail(emailBody)

        self.wass.WassLogging.info("############### Whois WASS Run Done ###############")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassCommon.moveResultFile(self.wass.WhoisTargetXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.WhoisTargetIPXMLReport, finalResultDir)
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.WhoisWassLog, finalResultDir)
