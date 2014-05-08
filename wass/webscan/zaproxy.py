'''
zaproxy.py

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
__updated__ = '2014.05.06'

import os
import signal
import time
import subprocess as sub
try:
    from zapv2 import ZAPv2
except ImportError:
    print("You must have the python-owasp-zap-v2 module installed")
    raise SystemExit(1)


class WassZAProxy(object):
    '''
    This is the WASS ZAProxy class
    '''

    def __init__(self, wass):
        '''
        Initialize WassZAProxy module
        '''
        self.wass = wass

    def startZAProxy(self):
        '''
        Start the ZAProxy
        '''
        self.wass.WassLogging.info("############### Entering startZAProxy ###############")
        self.checkZAProxyRunning()
        if (self.wass.ZAProxyIsRunning == False):
            self.wass.WassLogging.info("Starting the ZAProxy with following command: %s" % self.wass.ZAProxyCLI)
            p = sub.Popen(self.wass.ZAProxyCLI, shell=True, stdout=sub.PIPE)
            self.wass.WassLogging.info("We have started the ZAProxy and are going to sleep for 20 seconds to give it a chance to start up")
            time.sleep(20)
            self.wass.WassLogging.info("Done sleeping moving on")
            self.wass.ZAProxyIsRunning = True
        self.checkZAProxyRunning()
        self.wass.WassLogging.info("############### Leaving startZAProxy ###############")

    def stopZAProxy(self):
        '''
        Stop the ZAProxy thru the ZAProxy API
        '''
        self.wass.WassLogging.info("############### Entering stopZAProxy ###############")
        if (self.wass.ZAProxyIsRunning == True):
            self.wass.WassLogging.info("Stopping the ZAProxy via the ZAPv2 API")
            zap = ZAPv2()
            zap.core.shutdown
            self.wass.WassLogging.debug("We have sent the Stop command going to sleep for 30 seconds to give it a chance to shutdown")
            time.sleep(30)
            self.wass.WassLogging.debug("Done sleeping moving on")
            self.wass.WassLogging.debug("Making sure that the ZAProxy process is dead, running checkZAProxyRunning")
            self.checkZAProxyRunning()
            if (self.wass.ZAProxyIsRunning == True):
                self.wass.WassLogging.debug("Apparently the ZAProxy process is still running, now we try and kill it the HARD way!!!")
                self.wass.WassLogging.info("Stopping the ZAProxy via the os.kill()")
                self.wass.WassLogging.info("The ZAProxy PID is: %s" % self.wass.ZAProxyRunningPid)
                # The below command only work on Linux platforms !!!
                os.kill(int(self.wass.ZAProxyRunningPid), signal.SIGTERM)
                self.wass.WassLogging.debug("The ZAProxy process should now be dead RIP. !!!")

        self.wass.WassLogging.info("############### Leaving stopZAProxy ###############")

    def checkZAProxyRunning(self):
        '''
        Check if ZAProxy running
        '''
        self.wass.WassLogging.info("############### Entering checkZAProxyRunning ###############")
        self.wass.WassLogging.info("Cheking if the is ZAProxy is running")
        currentUserName = os.path.split(os.path.expanduser('~'))[-1]
        runCMD = "ps -o pid,pcpu,rss,command -u " + currentUserName + " | grep zap.jar | grep -v grep"
        # If the ZAProxy is running a line like the following will be returned:
        # 11044  1.8 352404 java -Xmx512m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar -daemon
        self.wass.WassLogging.debug("checkZAProxyRunning is running this command: %s" % runCMD)
        processFound = False
        pidfound = None
        commandfound = None
        proc = sub.Popen(runCMD, shell=True, stdout=sub.PIPE)
        for output in proc.stdout:
            if output.strip().startswith('PID'):
                continue
            pid, pcpu, rss, command = output.strip().split(None,3)
            # ZAProxy can be started with 3 different memory options so we need to handle that
            if ('java -Xmx512m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar -daemon' in command):
                processFound = True
                pidfound = pid
                commandfound = command
                self.wass.WassLogging.debug("ZAProxy is running with this command: java -Xmx512m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar -daemon")
                self.wass.WassLogging.debug("And the PID is: %s" % pidfound)
            elif ('java -Xmx256m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar -daemon' in command):
                processFound = True
                pidfound = pid
                commandfound = command
                self.wass.WassLogging.debug("ZAProxy is running with this command: java -Xmx256m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar -daemon")
                self.wass.WassLogging.debug("And the PID is: %s" % pidfound)
            elif ('java -Xmx128m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar -daemon' in command):
                processFound = True
                pidfound = pid
                commandfound = command
                self.wass.WassLogging.debug("ZAProxy is running with this command: java -Xmx128m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar -daemon")
                self.wass.WassLogging.debug("And the PID is: %s" % pidfound)
            elif ('java -Xmx512m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar' in command):
                processFound = True
                pidfound = pid
                commandfound = command
                self.wass.WassLogging.debug("ZAProxy is running with this command: java -Xmx512m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar")
                self.wass.WassLogging.debug("And the PID is: %s" % pidfound)
            elif ('java -Xmx256m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar' in command):
                processFound = True
                pidfound = pid
                commandfound = command
                self.wass.WassLogging.debug("ZAProxy is running with this command: java -Xmx256m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar")
                self.wass.WassLogging.debug("And the PID is: %s" % pidfound)
            elif ('java -Xmx128m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar' in command):
                processFound = True
                pidfound = pid
                commandfound = command
                self.wass.WassLogging.debug("ZAProxy is running with this command: java -Xmx128m -XX:PermSize=256M -jar /opt/ZAProxy/zap.jar")
                self.wass.WassLogging.debug("And the PID is: %s" % pidfound)

        if (processFound):
            self.wass.WassLogging.info("ZAProxy is running with the following command: %s" % commandfound)
            self.wass.WassLogging.info("And the PID is: %s" % pidfound)
            self.wass.WassLogging.info("ZAProxy appears to be running, issuing the zap.urlopen(self.wass.ScanTarget) command")
            zap = ZAPv2()
            zap.urlopen(self.wass.ScanTarget)
            self.wass.WassLogging.info("Sleeping for 10 seconds")
            time.sleep(10)
            self.wass.WassLogging.info("Done sleeping moving on")

        self.wass.WassLogging.debug("Was a running ZAProxy instance found: %s" % processFound)
        self.wass.ZAProxyIsRunning = processFound
        if (pidfound is not None):
            self.wass.ZAProxyRunningPid = pidfound
        self.wass.WassLogging.info("############### Leaving checkZAProxyRunning ###############")

    def RunZAProxy(self):
        '''
        Run the ZAProxy Scan
        '''
        self.wass.CurrentTask = "ZAProxy"
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.ZAProxyWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        # Setting the ZAProxy result files
        self.wass.ZAProxyXMLReport = self.wass.ZAProxyPath + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".xml"
        self.wass.ZAProxySessionFile = self.wass.ZAProxyPath + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".session"
        self.wass.ZAProxySessionDataFile = self.wass.ZAProxyPath + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".session.data"
        self.wass.ZAProxySessionLCKFile = self.wass.ZAProxyPath + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".session.lck"
        self.wass.ZAProxySessionLogFile = self.wass.ZAProxyPath + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".session.log"
        self.wass.ZAProxySessionPropertiesFile = self.wass.ZAProxyPath + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".session.properties"
        self.wass.ZAProxySessionScriptFile = self.wass.ZAProxyPath + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".session.script"
        self.wass.WassGetVersion._GetZAProxyVersion()
        self.wass.WassLogging.CreateLogfile(self.wass.ZAProxyWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run of: " + self.wass.TargetDomain
        if (self.wass.ZAProxyIsRunning == False):
            self.startZAProxy()

        self.wass.WassLogging.info("The Configured local ZAProxy is: %s" % self.wass.LocalZAProxy)
        if ((self.wass.LocalZAProxy == 'http://127.0.0.1:8080') or (self.wass.LocalZAProxy == 'http://localhost:8080')):
            self.wass.WassLogging.info("The local ZAProxy is by default: http://127.0.0.1:8080")
            zap = ZAPv2()
        else:
            # zap = ZAP(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})
            zapProxyOptions = "proxies={'http': '" + self.wass.LocalZAProxy + "', 'https': '" + self.wass.LocalZAProxy + "'}"
            self.wass.WassLogging.info("The local ZAProxy is configured to the following: %s " % zapProxyOptions)
            zap = ZAPv2(zapProxyOptions)

        self.wass.WassLogging.info("############### Start ZAProxy Basic Setup ###############")
        self.wass.WassLogging.info("Doing some basic configuration and Starting the ZAProxy run")
        os.chdir(self.wass.ZAProxyPath)
        self.wass.WassLogging.info("The Current Working Directory is: %s" % os.getcwd())
        self.wass.WassLogging.info("The ZAProxy Home directory is: %s " % zap.core.home_directory)
        if (zap.core.home_directory != self.wass.ZAProxyPath):
            self.wass.WassLogging.debug("Setting the ZAProxy Home directory to: %s " % self.wass.ZAProxyPath)
            zap.core.set_home_directory(self.wass.ZAProxyPath)
            self.wass.WassLogging.debug("The ZAProxy Home directory is now: %s " % zap.core.home_directory)

        self.wass.WassLogging.info("--------------------Alert threshold--------------------")
        self.wass.WassLogging.info("The Current Alert threshold is: %s" % zap.ascan.option_alert_threshold)
        self.wass.WassLogging.debug("The Configured Alert threshold is: %s" % self.wass.ZAProxyAlertThreshold)
        if (zap.ascan.option_alert_threshold != self.wass.ZAProxyAlertThreshold):
            self.wass.WassLogging.debug("The Alert threshold will be set to: %s" % self.wass.ZAProxyAlertThreshold)
            if (self.wass.ZAProxyAlertThreshold == 'LOW'):
                zap.ascan.set_option_alert_threshold('LOW')
                self.wass.WassLogging.info("The Alert threshold should now be Low")
            elif (self.wass.ZAProxyAlertThreshold == 'MEDIUM'):
                zap.ascan.set_option_alert_threshold('MEDIUM')
                self.wass.WassLogging.info("The Alert threshold should now be Medium")
            elif (self.wass.ZAProxyAlertThreshold == 'HIGH'):
                zap.ascan.set_option_alert_threshold('HIGH')
                self.wass.WassLogging.info("The Alert threshold should now be High")
        self.wass.WassLogging.info("The Alert threshold is now: %s" % zap.ascan.option_alert_threshold)
        self.wass.WassLogging.info("--------------------Alert threshold--------------------")

        self.wass.WassLogging.info("--------------------Attack threshold--------------------")
        self.wass.WassLogging.info("The Current Attack Strength is: %s" % zap.ascan.option_attack_strength)
        self.wass.WassLogging.debug("The Configured Attack Strength is: %s" % self.wass.ZAProxyAttackStrength)
        if (zap.ascan.option_attack_strength != self.wass.ZAProxyAttackStrength):
            self.wass.WassLogging.debug("The Attack Strength will be set to: %s" % self.wass.ZAProxyAttackStrength)
            if (self.wass.ZAProxyAttackStrength == 'LOW'):
                zap.ascan.set_option_attack_strength('LOW')
                self.wass.WassLogging.info("The Attack Strength should now be Low")
            elif (self.wass.ZAProxyAttackStrength == 'MEDIUM'):
                zap.ascan.set_option_attack_strength('MEDIUM')
                self.wass.WassLogging.info("The Attack Strength should now be Medium")
            elif (self.wass.ZAProxyAttackStrength == 'HIGH'):
                zap.ascan.set_option_attack_strength('HIGH')
                self.wass.WassLogging.info("The Attack Strength should now be High")
            elif (self.wass.ZAProxyAttackStrength == 'INSANE'):
                zap.ascan.set_option_attack_strength('INSANE')
                self.wass.WassLogging.info("The Attack Strength should now be Insane")

        self.wass.WassLogging.info("The Attack Strength is now: %s" % zap.ascan.option_attack_strength)
        self.wass.WassLogging.info("--------------------Attack threshold--------------------")
        self.wass.WassLogging.info("############### Done ZAProxy Basic Setup ###############")

        self.wass.WassLogging.info("############### Start ZAProxy Scan of the Target ###############")
        self.wass.WassLogging.info("Open the URL of the Target: %s " % self.wass.ScanTarget)
        zap.urlopen(self.wass.ScanTarget)
        # Give the sites tree a chance to get updated
        time.sleep(5)

        self.wass.WassLogging.info("Start Spidering the Target: %s " % self.wass.ScanTarget)
        zap.spider.scan(self.wass.ScanTarget)
        # Give the Spider a chance to start
        time.sleep(5)
        while (int(zap.spider.status) < 100):
                self.wass.WassLogging.debug("Spider progress %: " + zap.spider.status)
                time.sleep(5)
        self.wass.WassLogging.info("Finished Spidering the Target: %s " % self.wass.ScanTarget)
        # Give the passive scanner a chance to finish
        time.sleep(10)

        self.wass.WassLogging.info("Start Scanning the Target: %s " % self.wass.ScanTarget)
        self.wass.WassLogging.debug("The parameters for the Target is: %s " % zap.params.params(self.wass.ScanTarget))
        zap.ascan.scan(self.wass.ScanTarget)
        while (int(zap.ascan.status) < 100):
                self.wass.WassLogging.debug("Scan progress %: " + zap.ascan.status)
                time.sleep(5)
        self.wass.WassLogging.info("Finished Scanning the Target: %s " % self.wass.ScanTarget)
        time.sleep(10)

        self.wass.WassLogging.info("Start getting the XML Report for the Target: %s " % self.wass.ScanTarget)
        try:
            xmlFile = zap.core.xmlreport
            self.wass.WassLogging.info("Finished getting the XML Report for the Target: %s " % self.wass.ScanTarget)
            self.wass.WassLogging.debug("The ZAP Alerts are:")
            self.wass.WassLogging.debug(xmlFile)
            outputFile = open(self.wass.ZAProxyXMLReport, "w")
            outputFile.writelines(xmlFile)
            outputFile.close()
        except ValueError as e:
            self.wass.WassLogging.debugNoFormatting("There was an error in creating the XML File, the Error is: %s " % e)

        self.wass.WassLogging.info("Start Saving the Session for the Target: %s " % self.wass.ScanTarget)
        self.wass.WassLogging.debug("The Current Working Directory is: %s" % os.getcwd())
        self.wass.WassLogging.debug("The ZAProxy Home directory is: %s " % zap.core.home_directory)
        saveSession = "ZAProxy_" + self.wass.TargetDomain + "_" + self.wass.ReportDate
        zap.core.save_session(saveSession)
        time.sleep(10)   # Give the save_session time to complete
        self.wass.WassLogging.info("Finished Saving the Session for the Target: %s " % self.wass.ScanTarget)
        self.wass.WassLogging.info("############### Done ZAProxy Scan of the Target ###############")

        self.wass.WassLogging.info("############### Start ZAProxy Cleanup ###############")
        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.WassLogging.info("The finalResultDir is: %s" % finalResultDir)

        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)

        if ((self.wass.ZAProxyIsRunning and self.wass.ZAProxyStop and self.wass.Program == "ALL" and self.wass.CurrentTask == "ZAProxy") or (self.wass.ZAProxyIsRunning and self.wass.ZAProxyStop and self.wass.Program != "ALL")):
            self.stopZAProxy()

        self.wass.WassCommon.moveResultFile(self.wass.ZAProxyXMLReport, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ZAProxySessionFile, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ZAProxySessionDataFile, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ZAProxySessionLCKFile, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ZAProxySessionLogFile, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ZAProxySessionPropertiesFile, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.ZAProxySessionScriptFile, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        self.wass.WassLogging.info("############### Done ZAProxy Cleanup ###############")
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current logging so we can copy the log file into the result dir for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.ZAProxyWassLog, finalResultDir)
