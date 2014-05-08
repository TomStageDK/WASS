'''
openvas.py

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

import base64
import time
import subprocess as sub
import xml.dom.minidom
import xml.parsers
import xml.etree.ElementTree as ET


class WassOpenVAS(object):
    '''
    This is the WassOpenVAS class
    '''

    def __init__(self, wass):
        '''
        Initialize WassOpenVAS module
        '''
        self.wass = wass

    def RunOpenVAS(self):
        '''
        Run OpenVAS-6 against the Target Domain
        '''
        self.wass.CurrentTask = "OpenVAS"
        # Setup the self.wass.WassLogging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.OpenVASWassLog = self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.WassLogging.CreateLogfile(self.wass.OpenVASWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()
        #Make the 1st connection to the ScanTarget to see if everything is ready for the run
        self.wass.WassCommon.checkURL()

        emailBody = "This is the result email for the " + self.wass.CurrentTask + " run against: " + self.wass.TargetDomain

        # Start the OpenVAS Run against the Target Domain
        self._startOpenVASRun()

        finalResultDir = self.wass.WassCommon.createResultDir()
        self.wass.Wassself.wass.WassLogging .info("The finalResultDir is: %s" % finalResultDir)
        mailAttachment = self.wass.WassCommon.createZipFile()
        self.wass.WassLogging.info("The Mail Attachment is: %s" % mailAttachment)
        if (self.wass.SendEmail):
            self.wass.WassCommon.SendEMail(emailBody, mailAttachment)
        self.wass.WassCommon.moveResultFile(self.wass.OpenVASWordList, finalResultDir)
        self.wass.WassCommon.moveResultFile(self.wass.OpenVASRunLog, finalResultDir)
        self.wass.WassCommon.moveResultFile(mailAttachment, finalResultDir)
        self.wass.WassCommon.printInfo()
        #Now we need to stop the current self.wass.WassLogging so we can copy the log file into the result directory for the current run
        self.wass.WassLogging.stopLogging()
        self.wass.WassCommon.moveLogFile(self.wass.OpenVASWassLog, finalResultDir)

    def _startOpenVASRun(self):
        '''
        Start the OpenVAS Run against the Target Domain
        '''
        self.wass.WassLogging.info("############### OpenVAS WASS Run Starting ###############")
        if (self.wass.OpenVASTaskID is None):
            # Check if the Target Domain exists
            self._checkTarget()
            self.wass.WassLogging.info("The TargetID found is: %s" % self.wass.OpenVASTargetID)
            # If the Target Domain dont't exist create it
            if (self.wass.OpenVASTargetID is None):
                self._createTarget()
                self.wass.WassLogging.info("The target got the following ID: %s" % self.wass.OpenVASTargetID)

            # Create a new Configuration for the SCAN
            # This is messy in OpenVAS-6 1 target multiple configurations, this is done because
            # the base configuration could have changed since last time we ran a scan against the target domain
            self._createConfig()

            self._createTask()
            self.wass.WassLogging.info("The taskID is: %s" % self.wass.OpenVASTaskID)
            if (self.wass.OpenVASTaskStatus.startswith('2')):
                self.wass.WassLogging.info("Running the task with taskID: %s" % self.wass.OpenVASTaskID)
                self._runTask()
            else:
                self.wass.WassLogging.info("The Create Task returned the following Status code: %s" % self.wass.OpenVASTaskStatus)
                exit(self.wass.OpenVASTaskStatus)

        elif (self.wass.OpenVASTaskID is not None):
            self.wass.WassLogging.info("Running the task with taskID: %s" % self.wass.OpenVASTaskID)
            self._runTask()

        if (self.wass.OpenVASTaskStatus.startswith('2')):
            self._getTask()

        if (self.wass.OpenVASTaskReportID is not None):
            self._getReport()
        else:
            self.wass.WassLogging.info("The Report ID was not Found!!!!")

        self.wass.WassLogging.info("############### OpenVAS WASS Run Done ###############")

    def _runQuery(self, currentTask, runQueryCMD):
        self.wass.WassLogging.debug(currentTask + ": Calling OpenVAS OMP with the following: %s" % runQueryCMD)
        command_Responce = ''
        p = sub.Popen(runQueryCMD, shell=True, stdout=sub.PIPE, stderr=sub.STDOUT)
        for line in p.stdout.readlines():
            command_Responce = command_Responce + line
            retval = p.wait()

        #printDebug("The "+currentTask+" returned the following XML: %s " % command_Responce)
        self.wass.WassLogging.debug("The " + currentTask + " returned the following XML: %s " % command_Responce)

        return command_Responce

    def _checkTarget(self):
        self.wass.WassLogging.info("############### Entering checkTarget ###############")
        targetDomain = self.wass.TargetDomain
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<get_targets/>"'

        checkTargetID = None
        command_Responce = self._runQuery("checkTarget", queryCommand)
        responceXML = xml.dom.minidom.parseString(command_Responce)
        for node in responceXML.getElementsByTagName("get_targets_response"):
            self.wass.WassLogging.info("Reading the Response from the checkTarget Command")
            checkTargetStatus = node.getAttribute("status")
            self.wass.WassLogging.info("The checkTarget Status is: %s" % checkTargetStatus)

        responceXML = ET.XML(command_Responce)
        notFound = True
        for element in responceXML.getiterator("target"):
            if (notFound):
                tmpTargetID = element.attrib.get("id")
                self.wass.WassLogging.info("The current TargetID is: %s " % tmpTargetID)
                for element1 in element.getchildren():
                    if (element1.tag == "name"):
                        self.wass.WassLogging.debug("The Tag is: %s " % element1.tag)
                        self.wass.WassLogging.debug("The Value is: %s " % element1.text)
                        if (element1.text == "WASS " + targetDomain):
                            self.wass.WassLogging.debug("Target found!!!")
                            checkTargetID = tmpTargetID
                            notFound = False
                            break

        self.wass.OpenVASTargetStatus = checkTargetStatus
        self.wass.OpenVASTargetID = checkTargetID

    def _createTarget(self):
        self.wass.WassLogging.info("############### Entering createTarget ###############")
        targetDomain = self.wass.TargetDomain
        targetPortListID = self.wass.OpenVASPortListID
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<create_target><name>WASS ' + targetDomain + '</name><hosts>' + targetDomain + '</hosts><comment>' + targetDomain + '</comment><port_list id="' + targetPortListID + '"/></create_target>"'

        createTargetID = None
        command_Responce = self._runQuery("createTarget", queryCommand)

        responceXML = xml.dom.minidom.parseString(command_Responce)
        for node in responceXML.getElementsByTagName("create_target_response"):
            self.wass.WassLogging.info("Reading the Response from the createTarget Command")
            createTargetStatus = node.getAttribute("status")
            self.wass.WassLogging.info("The Status is: %s" % createTargetStatus)
            if createTargetStatus.startswith('2'):
                createTargetID = node.getAttribute("id")
                self.wass.WassLogging.info("The TargetID is: %s" % createTargetID)

        self.wass.OpenVASTargetStatus = createTargetStatus
        self.wass.OpenVASTargetID = createTargetID

    def _createConfig(self):
        self.wass.WassLogging.info("############### Entering createConfig ###############")
        orgScanConfigID = self.wass.OpenVASScanConfig
        createConfigTarget = self.wass.TargetDomain
        createConfigTargetIP = self.wass.TargetIP
        self.wass.WassLogging.info("With the following parameters:")
        self.wass.WassLogging.info("orgScanConfigID: %s" % orgScanConfigID)
        self.wass.WassLogging.info("createConfigTarget: %s" % createConfigTarget)
        self.wass.WassLogging.info("createConfigTargetIP: %s" % createConfigTargetIP)
        self.wass.WassLogging.info("Start by copying the config configured in the wass.config")
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<create_config><copy>' + orgScanConfigID + '</copy><name>WASS ' + createConfigTarget + '</name><comment>Web Application Security Scan</comment></create_config>"'

        createConfigID = None
        command_Responce = self._runQuery("createConfig", queryCommand)
        responceXML = xml.dom.minidom.parseString(command_Responce)
        for node in responceXML.getElementsByTagName("create_config_response"):
            self.wass.WassLogging.info("Reading the Response from the createConfig command")
            createConfigStatus = node.getAttribute("status")
            self.wass.WassLogging.info("The createConfig Status is: %s" % createConfigStatus)
            if createConfigStatus.startswith('2'):
                createConfigID = node.getAttribute("id")
                self.wass.WassLogging.info("The createConfig ID is: %s" % createConfigID)

        if createConfigStatus.startswith('2'):
            self.wass.WassLogging.info("The copy command was OK!!")
            self.wass.WassLogging.info("Modify the configuration!! ")
            queryCommand = self.wass.OpenVASCMD + ' -i -X "<modify_config config_id="' + createConfigID + '"><preference><name>scanner[scanner]:vhosts</name><value>' + base64.b64encode(createConfigTarget) + '</value></preference></modify_config>"'

            command_Responce = self._runQuery("createConfig Modify vhosts", queryCommand)
            responceXML = xml.dom.minidom.parseString(command_Responce)
            for node in responceXML.getElementsByTagName("modify_config_response"):
                self.wass.WassLogging.info("Reading the Response from the createConfig modify Command")
                createConfigModifyVHOSTSStatus = node.getAttribute("status")
                self.wass.WassLogging.info("The createConfig Modify Status is: %s" % createConfigModifyVHOSTSStatus)

            queryCommand = self.wass.OpenVASCMD + ' -i -X "<modify_config config_id="' + createConfigID + '"><preference><name>scanner[scanner]:vhosts_ip</name><value>' + base64.b64encode(createConfigTargetIP) + '</value></preference></modify_config>"'

            command_Responce = self._runQuery("createConfig Modify vhosts_ip", queryCommand)
            responceXML = xml.dom.minidom.parseString(command_Responce)
            for node in responceXML.getElementsByTagName("modify_config_response"):
                self.wass.WassLogging.info("Reading the Response from the createConfig modify Command")
                createConfigModifyVHOSTS_IPStatus = node.getAttribute("status")
                self.wass.WassLogging.info("The createConfig Modify Status is: %s" % createConfigModifyVHOSTS_IPStatus)

        self.wass.OpenVASConfigStatus = createConfigStatus
        self.wass.OpenVASConfigModifyVHOSTSStatus = createConfigModifyVHOSTSStatus
        self.wass.OpenVASConfigModifyVHOSTSIPStatus = createConfigModifyVHOSTS_IPStatus
        self.wass.OpenVASNewConfigID = createConfigID

    def _createTask(self):
        self.wass.WassLogging.info("############### Entering createTask ###############")
        createTaskTarget = self.wass.TargetDomain
        createTaskTargetID = self.wass.OpenVASTargetID
        createTaskConfigID = self.wass.OpenVASNewConfigID
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<create_task><name>WASS ' + createTaskTarget + '</name><comment>WASS Scan</comment><config id="' + createTaskConfigID + '"/><target id="' + createTaskTargetID + '"/></create_task>"'

        createTaskID = None
        command_Responce = self._runQuery("createTask", queryCommand)
        responceXML = xml.dom.minidom.parseString(command_Responce)
        for node in responceXML.getElementsByTagName("create_task_response"):
            self.wass.WassLogging.info("Reading the Response from the createTask Command")
            createTaskStatus = node.getAttribute("status")
            self.wass.WassLogging.info("The Status is: %s" % createTaskStatus)
            if createTaskStatus.startswith('2'):
                createTaskID = node.getAttribute("id")

        self.wass.OpenVASTaskStatus = createTaskStatus
        self.wass.OpenVASTaskID = createTaskID

    def _runTask(self):
        self.wass.WassLogging.info("############### Entering runTask ###############")
        runTaskID = self.wass.OpenVASTaskID
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<start_task task_id="' + runTaskID + '"/>"'

        command_Responce = self._runQuery("runTask", queryCommand)
        responceXML = xml.dom.minidom.parseString(command_Responce)
        for node in responceXML.getElementsByTagName("start_task_response"):
            self.wass.WassLogging.info("Reading the Response from the runTask Command")
            runTaskStatus = node.getAttribute("status")
            self.wass.WassLogging.info("Status is: %s" % runTaskStatus)

        self.wass.OpenVASTaskStatus = runTaskStatus

    def _checkTask(self):
        self.wass.WassLogging.info("############### Entering checkTask ###############")
        getTaskName = self.wass.TargetDomain
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<get_tasks/>"'

        command_Responce = self._runQuery("checkTask", queryCommand)
        checkTaskID = None
        checkTaskStatus = None
        tmpTaskName = "WASS " + getTaskName
        responceXML = xml.dom.minidom.parseString(command_Responce)
        for node in responceXML.getElementsByTagName("get_tasks_response"):
            self.wass.WassLogging.info("Reading the Response from the checkTask Command")
            checkTaskStatus = node.getAttribute("status")
            self.wass.WassLogging.info("checkTask: Status is: %s" % checkTaskStatus)

        if checkTaskStatus.startswith('2'):
            responceXML = ET.XML(command_Responce)
            notFound = True
            for element in responceXML.getiterator("task"):
                if (notFound):
                    tmpTargetID = element.attrib.get("id")
                    self.wass.WassLogging.debug("The current TargetID is: %s " % tmpTargetID)
                    for element1 in element.getchildren():
                        if (element1.tag == "name"):
                            self.wass.WassLogging.debug("The Tag is: %s " % element1.tag)
                            self.wass.WassLogging.debug("The Value is: %s " % element1.text)
                            if (element1.text == tmpTaskName):
                                self.wass.WassLogging.debug("Task found!!!")
                                checkTaskID = tmpTargetID
                                notFound = False
                                break

        self.wass.OpenVASTaskStatus = checkTaskStatus
        self.wass.OpenVASTaskID = checkTaskID

    def _getTask(self):
        '''
        OpenVAS returns the progress as % while the scan is running, and returns -1 when it is done
        '''
        self.wass.WassLogging.info("############### Entering getTask ###############")
        getTaskID = self.wass.OpenVASTaskID
        getTaskProgress = self.wass.OpenVASTaskProgress
        getTaskReportID = self.wass.OpenVASTaskReportID
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<get_tasks task_id="' + getTaskID + '" details="1"/>"'

        while (getTaskProgress != "-1"):
            self.wass.WassLogging.info("The progress of the current scan is: %s" % getTaskProgress)

            command_Responce = self._runQuery("getTask", queryCommand)

            responceXML = xml.dom.minidom.parseString(command_Responce)
            for node in responceXML.getElementsByTagName("get_tasks_response"):
                self.wass.WassLogging.debug("Reading the Response from the getTask Command")
                getTaskStatus = node.getAttribute("status")
                self.wass.WassLogging.info("getTask: Status is: %s" % getTaskStatus)

            if getTaskStatus.startswith('2'):
                responceXML = ET.XML(command_Responce)
                for element in responceXML.getiterator("task"):
                    for element1 in element.getchildren():
                        if (element1.tag == "progress"):
                            self.wass.WassLogging.debug("getTask: The Tag is: %s " % element1.tag)
                            self.wass.WassLogging.debug("getTask: The Value is: %s " % element1.text)
                            getTaskProgress = element1.text
                            break

                if (getTaskReportID is None):
                    for element in responceXML.getiterator("report"):
                        tmpReportID = element.attrib.get("id")
                        self.wass.WassLogging.debug("The current Report ID is: %s " % tmpReportID)
                        for element1 in element.getchildren():
                            if (element1.tag == "scan_run_status"):
                                self.wass.WassLogging.debug("The Tag is: %s " % element1.tag)
                                self.wass.WassLogging.debug("The Value is: %s " % element1.text)
                                if (element1.text == "Running" or element1.text == "Requested"):
                                    self.wass.WassLogging.debug("Report ID found!!!")
                                    getTaskReportID = tmpReportID
                                    self.wass.WassLogging.debug("Report ID is: %s " % getTaskReportID)
                                    break
            elif getTaskStatus.startswith('4'):
                self.wass.WassLogging.debug("The getTaskStatus was: %s" % getTaskStatus)
                getTaskProgress = "-1"
            elif getTaskStatus.startswith('5'):
                self.wass.WassLogging.debug("The getTaskStatus was: %s" % getTaskStatus)
                getTaskProgress = "-1"

            if (getTaskProgress != "-1"):
                # Sleeping for 10 seconds
                time.sleep(10)

        self.wass.OpenVASTaskStatus = getTaskStatus
        self.wass.OpenVASTaskProgress = getTaskProgress
        self.wass.OpenVASTaskReportID = getTaskReportID

    def _getReport(self):
        self.wass.WassLogging.info("############### Entering getReport ###############")
        getReportID = self.wass.OpenVASTaskReportID
        queryCommand = self.wass.OpenVASCMD + ' -i -X "<get_reports report_id="' + getReportID + '"/>"'

        command_Responce = self._runQuery("getReport", queryCommand)

        responceXML = xml.dom.minidom.parseString(command_Responce)
        for node in responceXML.getElementsByTagName("get_reports_response"):
            self.wass.WassLogging.info("Reading the Response from the getReport Command")
            getReportStatus = node.getAttribute("status")
            self.wass.WassLogging.info("getReport: Status is: %s" % getReportStatus)

            if getReportStatus.startswith('2'):
                outputFile = open(self.wass.OpenVASXMLReport, "w")
                outputFile.writelines(command_Responce)
                outputFile.close()
                return getReportStatus
            else:
                return getReportStatus
