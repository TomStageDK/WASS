'''
common.py

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
#TODO: Fix the printing of the data section in CheckUrl
#TODO: Check the getURLExclude function

__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.04.27'

import os
import time
import sys
import subprocess as sub
import socket
import smtplib
import mimetypes
import shutil
import zipfile
import ipaddr
from threading  import Thread
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
try:
    import tld
except ImportError:
    print('You must have the tld module installed')
    raise SystemExit(1)
try:
    import requests as HTTPRequest
except ImportError:
    print('You must have the requests module installed')
    raise SystemExit(1)


class WassCommon(object):
    '''
    This is the WASS Common class for standard functions used by all the WASS Scripts
    '''

    def __init__(self, wass):
        '''
        Initialize Common module
        '''
        self.wass = wass

    def getDynamic(self):
        '''
        Get the Dynamic Parameters

        Will call: self.getHostIP(), self.getScanTarget(), self.getDomainName()
        '''
        # Get the dynamic options
        # Before we do anything else we need to get the IP Address of the target, if this fails the program will exit
        # Which is better to do here so we can exit the script
        if (self.wass.TargetIP is None):
            self.getHostIP()
        else:
            self.wass.WassLogging.info("We allready have the IP address for: %s" % self.wass.TargetDomain)
            self.wass.WassLogging.info("And it is: %s" % self.wass.TargetIP)
        # Get and set the scanTarget
        if (self.wass.ScanTarget is None):
            self.wass.ScanTarget = self.getScanTarget()
        else:
            self.wass.WassLogging.info("We allready have the Scan Target for: %s" % self.wass.TargetDomain)
            self.wass.WassLogging.info("And it is: %s" % self.wass.ScanTarget)
        # Get and set the domainName
        if (self.wass.TldDomainName is None):
            self.wass.TldDomainName = self.getDomainName()
        else:
            self.wass.WassLogging.info("We allready have the TLD for: %s" % self.wass.TargetDomain)
            self.wass.WassLogging.info("And it is: %s" % self.wass.TldDomainName)
        #Make the 1st connection to the ScanTarget to see if everything is ready for the run
        self.checkURL()
        self.getURLExcludeRegex()

    def getHostIP(self):
        '''
        Get the IP Address of the target Host name, e.g. www.google.dk
        '''
        self.wass.WassLogging.info("############### Entering getHostIP ###############")
        self.wass.WassLogging.info("Trying to lookup the IP address for %s" % self.wass.TargetDomain)
        try:
            self.wass.TargetIP = socket.gethostbyname(self.wass.TargetDomain)
            self.wass.TargetIPVersion = str(ipaddr.IPAddress(self.wass.TargetIP).version)
            self.wass.TargetIPType = ipaddr.IPAddress(self.wass.TargetIP).is_private
            self.wass.WassLogging.info("The IP is: %s" % self.wass.TargetIP)
            self.wass.WassLogging.info("The IP Version is: %s" % self.wass.TargetIPVersion)
            self.wass.WassLogging.info("The IP is Private: %s" % self.wass.TargetIPType)
            self.wass.WassLogging.info("############### Leaving getHostIP ###############")
        except socket.gaierror as e:
            self.wass.WassLogging.info("Exception error is: %s" % e)
            exit(-1)

    def getDomainName(self):
        '''
        Get the Top Level Domain Name of the target Host name, e.g. www.google.dk will become google.dk
        '''
        self.wass.WassLogging.info("############### Entering getDomainName ###############")
        self.wass.WassLogging.info("Get The TLD of the Host: %s" % self.wass.TargetDomain)
        domainName = tld.get_tld("http://" + self.wass.TargetDomain)
        self.wass.WassLogging.info("The TLD of the Host is: %s" % domainName)
        self.wass.WassLogging.info("############### Leaving getDomainName ###############")
        return domainName

    def getScanTarget(self):
        '''
        Build the ScanTarget string.

        e.g. www.google.dk will become: http://www.google.dk
        e.g. -t www.somsite.com -p 8443 will become: https://www.somsite.com:8443
        e.g. -t www.somsite.com -p 8443 -u /Administration/login will become: https://www.somsite.com:8443/Administration/login
        '''
        self.wass.WassLogging.info("############### Entering getScanTarget ###############")
        scanTarget = None
        targetProtocol = self.wass.TargetScheme

        self.wass.WassLogging.debug("####Parameters####")
        self.wass.WassLogging.debug("The Scheme is: %s" % self.wass.TargetScheme)
        self.wass.WassLogging.debug("The Target is: %s" % self.wass.TargetDomain)
        self.wass.WassLogging.debug("The Port is: %s" % self.wass.TargetPort)
        self.wass.WassLogging.debug("The Url is: %s" % self.wass.TargetURL)
        self.wass.WassLogging.debug("####Parameters####")
        if ((self.wass.TargetPort == 80) or (self.wass.TargetPort == 443)):
            self.wass.WassLogging.debug("The port is 80 or 443")
            if (self.wass.TargetURL != "/"):
                self.wass.WassLogging.debug("The Url is not /")
                if (self.wass.TargetURL.startswith('/')):
                    self.wass.WassLogging.debug("The Url starts with /")
                    scanTarget = targetProtocol + "://" + self.wass.TargetDomain + self.wass.TargetURL
                else:
                    self.wass.WassLogging.debug("The Url did not start with /")
                    scanTarget = targetProtocol + "://" + self.wass.TargetDomain + "/" + self.wass.TargetURL
            else:
                self.wass.WassLogging.debug("The Url is /")
                scanTarget = targetProtocol + "://" + self.wass.TargetDomain
        else:
            self.wass.WassLogging.debug("The port is not 80 or 443")
            if (self.wass.TargetURL != "/"):
                self.wass.WassLogging.debug("The Url is not /")
                if (self.wass.TargetURL.startswith('/')):
                    self.wass.WassLogging.debug("The Url starts with /")
                    scanTarget = targetProtocol + "://" + self.wass.TargetDomain + ":" + str(self.wass.TargetPort) + self.wass.TargetURL
                else:
                    self.wass.WassLogging.debug("The Url did not start with /")
                    scanTarget = targetProtocol + "://" + self.wass.TargetDomain + ":" + str(self.wass.TargetPort) + "/" + self.wass.TargetURL
            else:
                self.wass.WassLogging.debug("The Url is /")
                scanTarget = targetProtocol + "://" + self.wass.TargetDomain + ":" + str(self.wass.TargetPort)

        self.wass.WassLogging.info("The ScanTarget is: %s" % scanTarget)
        self.wass.WassLogging.info("############### Leaving getScanTarget ###############")
        return scanTarget

    def checkURL(self):
        '''
        Check the final URL to the target to make sure it is valid
        '''
        self.wass.WassLogging.info("############### Entering checkURL ###############")
        self.wass.WassLogging.info("Trying to access the Scan Target: %s" % self.wass.ScanTarget)
        try:
            second_response = HTTPRequest.get(self.wass.ScanTarget)
        except HTTPRequest.ConnectionError as e:
            if hasattr(e, 'reason'):
                self.wass.WassLogging.info("There was an ConnectionError!!!.")
                self.wass.WassLogging.info("Reason: %s" % e.reason)
                print ('Something is wrong check the Log file!!!')
                exit(-1)
            elif hasattr(e, 'code'):
                self.wass.WassLogging.info("The server couldn't fulfill the request.")
                self.wass.WassLogging.info("Error code: %s" % e.code)
                print ('Something is wrong check the Log file!!!')
                exit(-1)
            else:
                print ('There was a Connection Error !!!')
                print ('Check the Log file!!!')
                exit(-1)
        except HTTPRequest.RequestException as e:
            if hasattr(e, 'reason'):
                self.wass.WassLogging.info("There was an RequestException!!!.")
                self.wass.WassLogging.info("Reason: %s" % e.reason)
                print ('Something is wrong check the Log file!!!')
                exit(-1)
            elif hasattr(e, 'code'):
                self.wass.WassLogging.info("The server couldn't fulfill the request.")
                self.wass.WassLogging.info("Error code: %s" % e.code)
                print ('Something is wrong check the Log file!!!')
                exit(-1)
            else:
                print ('There was a Connection Error !!!')
                print ('Check the Log file!!!')
                exit(-1)
        except HTTPRequest.HTTPError as e:
            if hasattr(e, 'reason'):
                self.wass.WassLogging.info("There was an HTTPError!!!.")
                self.wass.WassLogging.info("Reason: %s" % e.reason)
                print ('Something is wrong check the Log file!!!')
                exit(-1)
            elif hasattr(e, 'code'):
                self.wass.WassLogging.info("The server couldn't fulfill the request.")
                self.wass.WassLogging.info("Error code: %s" % e.code)
                print ('Something is wrong check the Log file!!!')
                exit(-1)
            else:
                print ('There was a Connection Error !!!')
                print ('Check the Log file!!!')
                exit(-1)
        else:
            #TODO: If debugging: print the received data as well
            # Fine we have now made the connection to the target with the standard urllib2.request
            # now we do the same with requests (Requests: HTTP for Humans)
            self.wass.WassLogging.info("------------------------------------------------------------")
            self.wass.WassLogging.info("The scanTarget Is OK: %s" % self.wass.ScanTarget)
            self.wass.WassLogging.info("The response contains this URL: %s" % second_response.url)
            self.wass.WassLogging.info("The Status code is: %s" % second_response.status_code)
            self.wass.WassLogging.info("-------------------------Printing Header Information-----------------")
            self.wass.WassLogging.info("Accept: %s " % second_response.headers.get('Accept'))
            self.wass.WassLogging.info("Accept-Charset: %s " % second_response.headers.get('Accept-Charset'))
            self.wass.WassLogging.info("Accept-Encoding: %s " % second_response.headers.get('Accept-Encoding'))
            self.wass.WassLogging.info("Accept-Language: %s " % second_response.headers.get('Accept-Language'))
            self.wass.WassLogging.info("Accept-Ranges: %s " % second_response.headers.get('Accept-Ranges'))
            self.wass.WassLogging.info("Age: %s " % second_response.headers.get('Age'))
            self.wass.WassLogging.info("Allow: %s " % second_response.headers.get('Allow'))
            self.wass.WassLogging.info("Authorization: %s " % second_response.headers.get('Authorization'))
            self.wass.WassLogging.info("Cache-Control: %s " % second_response.headers.get('Cache-Control'))
            self.wass.WassLogging.info("Connection: %s " % second_response.headers.get('Connection'))
            self.wass.WassLogging.info("connection-token: %s " % second_response.headers.get('connection-token'))
            self.wass.WassLogging.info("Content-Encoding: %s " % second_response.headers.get('Content-Encoding'))
            self.wass.WassLogging.info("Content-Language: %s " % second_response.headers.get('Content-Language'))
            self.wass.WassLogging.info("Content-Length: %s " % second_response.headers.get('Content-Length'))
            self.wass.WassLogging.info("Content-Location: %s " % second_response.headers.get('Content-Location'))
            self.wass.WassLogging.info("Content-Type: %s " % second_response.headers.get('Content-Type'))
            self.wass.WassLogging.info("Date: %s " % second_response.headers.get('Date'))
            self.wass.WassLogging.info("Expires: %s " % second_response.headers.get('Expires'))
            self.wass.WassLogging.info("Host: %s " % second_response.headers.get('Host'))
            self.wass.WassLogging.info("Location: %s " % second_response.headers.get('Location'))
            self.wass.WassLogging.info("Referer: %s " % second_response.headers.get('Referer'))
            self.wass.WassLogging.info("Server: %s " % second_response.headers.get('Server'))
            self.wass.WassLogging.info("User-Agent: %s " % second_response.headers.get('User-Agent'))
#            self.wass.WassLogging.debug("-------------------------Start Data Information-------------------")
#            self.wass.WassLogging.debugNoFormatting("%s " %second_response.text)
#            self.wass.WassLogging.debug("-------------------------Stop Data Information-------------------")

        self.wass.WassLogging.info("############### Leaving checkURL ###############")

    def getURLExcludeRegex(self):
        '''
        Create a Regex version of the URLs to exclude from the scan.

        TargetExcludeURLSRegex will by default contain this: (?i)(logout|disconnect|signout|exit)+
        e.g.  -e /Administration/quit will be (?i)(|disconnect|signout|exit|quit)+
        '''
        self.wass.WassLogging.info("############### Entering getURLExcludeRegex ###############")
        exclude_url_regex = '(?i)(logout|disconnect|signout|exit'
        if (self.wass.TargetExcludeURLS is not None):
            nr_of_exclude_urls = len(self.wass.TargetExcludeURLS)
            self.wass.WassLogging.debug("There are %s of URLs to exclude" % nr_of_exclude_urls)
            for excludeurl in self.wass.TargetExcludeURLS:
                self.wass.WassLogging.debug("Working on URL to exclude: %s" % excludeurl)
                current_exclude_url = excludeurl.split()[-1]
                self.wass.WassLogging.debug("Adding URL to exclude: %s" % current_exclude_url)
                exclude_url_regex += '|' + current_exclude_url

        self.wass.TargetExcludeURLSRegex = exclude_url_regex + ')+'
        self.wass.WassLogging.info("The TargetExcludeURLSRegex is now: %s" % self.wass.TargetExcludeURLSRegex)
        self.wass.WassLogging.info("############### Leaving getURLExcludeRegex ###############")

    def enqueue_output(self, out, queue):
        '''
        Que used by the runCommand to get the runtime log for the current running Task.
        '''
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    def runCommand(self, runCMD, runLog):
        '''
        Use sub.Popen to run the command for the Current Task
        '''
        self.wass.WassLogging.info("############### Entering runCommand ###############")
        self.wass.WassLogging.info(self.wass.CurrentTask + " Run Started at: %s " % time.strftime("%Y-%m-%d %H:%M:%S",))
        self.wass.WassLogging.debug("Calling " + self.wass.CurrentTask + " with the following command: %s" % runCMD)
        self.wass.WassLogging.info("Creating the Run log: %s" % runLog)
        if (os.path.isfile(runLog)):
            outputFile = open(runLog, "a", 0)
        else:
            outputFile = open(runLog, "w", 0)

        # Since we have a problem with the Skipfish process in the below run command, we run it the old way
        if (self.wass.CurrentTask == 'Skipfish'):
            self.wass.WassLogging.debug("We are running the old way for Skipfish, since it never stop with the new way!!")
            self.wass.WassLogging.debug("The Run log for Skipfish will be written at the end of the run and not live!!")
            # This was the old way to run the Process
            command_Responce = ""
            p = sub.Popen(runCMD, bufsize=-1, shell=True, stdout=sub.PIPE, stderr=sub.STDOUT)
            for line in p.stdout.readlines():
                command_Responce = command_Responce + line
                retval = p.wait()

            outputFile.writelines(command_Responce)
        else:
            # Check to see if we are running on a Posix system (This should be True for all Linux flavors)
            ON_POSIX = 'posix' in sys.builtin_module_names
            # Setup the Process and write all the output lines from the process to the runLog file
            myProcess = sub.Popen(runCMD, bufsize=-1, shell=True, stdout=sub.PIPE, stderr=sub.STDOUT, close_fds=ON_POSIX)
            myQue = Queue()
            myThread = Thread(target=self.enqueue_output, args=(myProcess.stdout, myQue))
            myThread.daemon = True  # thread dies with the program
            myThread.start()
            while (myThread.isAlive()):
                try:
                    line = myQue.get(block=True, timeout=1)  # or myQue.get_nowait()
                except Empty:
                    time.sleep(2)
                    self.wass.WassLogging.debug("Slept for 2 seconds waiting for output from the process")
                    self.wass.WassLogging.debug("And myThread.isAlive() is: %s" % myThread.isAlive())
                else:
                    outputFile.write(line)

        outputFile.close()
        self.wass.WassLogging.debug("The " + self.wass.CurrentTask + " run should be finished")
        self.wass.WassLogging.info(self.wass.CurrentTask + " Run Done at: %s " % time.strftime("%Y-%m-%d %H:%M:%S",))
        self.wass.WassLogging.info("############### Leaving runCommand ###############")

    def SendEMail(self, body, zipFile=None):
        '''
        Send an EMail with the results in the ZIP File, but if the ZIP File is empty only send the
        '''
        self.wass.WassLogging.info("############### Entering SendEMail ###############")
        self.wass.WassLogging.debug("Constructing the Result Email")
        outer = MIMEMultipart()
        outer['Subject'] = 'WASS - ' + self.wass.CurrentTask + ' scan Done!!!'
        outer['To'] = self.wass.ToEmail
        outer['From'] = self.wass.FromEmail
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        part1 = MIMEText(body, 'plain')

        if (zipFile is not None):
            self.wass.WassLogging.debug("The Zip File Attachment size is: %s" % os.path.getsize(zipFile))
        #    if (os.path.getsize(zipFile) <= 10240000):
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(zipFile)
            if ((ctype is None) or (encoding is not None)):
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            fp = open(zipFile, 'rb')
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            fp.close()
            # Encode the payload using Base64
            encoders.encode_base64(msg)
            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', filename=zipFile)
            outer.attach(part1)
            outer.attach(msg)
        else:
            outer.attach(part1)

        # Now send or store the message
        composed = outer.as_string()
        s = smtplib.SMTP('localhost')
        self.wass.WassLogging.debug("Sending the Result Email")
        s.sendmail(self.wass.FromEmail, self.wass.ToEmail, composed)
        s.quit()
        self.wass.WassLogging.info("############### Leaving SendEMail ###############")

    def createZipFile(self):
        '''
        Create a Zip file with the result files

        return: finalZipFile
        e.g.: ResultDir/CurrentTask_TargetDomain_ReportDate_result.zip
        '''
        self.wass.WassLogging.info("############### Entering createZipFile ###############")
        self.wass.WassLogging.info("Start Creating the Final Result Zip file for the task: %s" % self.wass.CurrentTask)
        finalZipFile = self.wass.ResultDir + "/" + self.wass.CurrentTask + "_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + "_result.zip"
        resultZipFile = zipfile.ZipFile(finalZipFile, 'w', zipfile.ZIP_DEFLATED)
        self.wass.WassLogging.info("The Final Result Zip file is: %s" % finalZipFile)

        # Adding the Result files for the Current Task
        if (self.wass.CurrentTask == "Nmap"):
            self.wass.WassLogging.debug("Before Adding the Nmap XML File: %s" % self.wass.NmapXML)
            if os.path.isfile(self.wass.NmapXML):
                (filepath, filename) = os.path.split(self.wass.NmapXML)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.NmapXML)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.NmapXML, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "Arachni"):
            self.wass.WassLogging.debug("Befor Adding the Arachni AFR File: %s" % self.wass.ArachniAFRReport)
            if os.path.isfile(self.wass.ArachniAFRReport):
                (filepath, filename) = os.path.split(self.wass.ArachniAFRReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ArachniAFRReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ArachniAFRReport, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the Arachni XML File: %s" % self.wass.ArachniXMLReport)
            if os.path.isfile(self.wass.ArachniXMLReport):
                (filepath, filename) = os.path.split(self.wass.ArachniXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ArachniXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ArachniXMLReport, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the Arachni HTML File: %s" % self.wass.ArachniHTMLReport)
            if os.path.isfile(self.wass.ArachniHTMLReport):
                (filepath, filename) = os.path.split(self.wass.ArachniHTMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ArachniHTMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ArachniHTMLReport, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "Fierce"):
            self.wass.WassLogging.debug("Before Adding the Fierce XML File: %s" % self.wass.FierceXMLReport)
            if os.path.isfile(self.wass.FierceXMLReport):
                (filepath, filename) = os.path.split(self.wass.FierceXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.FierceXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.FierceXMLReport, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "Nikto"):
            self.wass.WassLogging.debug("Before Adding the Nikto XML File: %s" % self.wass.NiktoXMLReport)
            if os.path.isfile(self.wass.NiktoXMLReport):
                (filepath, filename) = os.path.split(self.wass.NiktoXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.NiktoXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.NiktoXMLReport, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "OpenVAS"):
            pass
        elif (self.wass.CurrentTask == "Skipfish"):
            self.wass.WassLogging.debug("Before Adding the Skipfish Output Dir: %s" % self.wass.SkipfishOutputDir)
            if os.path.isdir(self.wass.SkipfishOutputDir):
                relroot = os.path.abspath(os.path.join(self.wass.SkipfishOutputDir, os.pardir))
                for dirname, subdirs, files in os.walk(self.wass.SkipfishOutputDir):
                    self.wass.WassLogging.debug("Inside the: dirname, subdirs, files in os.walk(self.wass.SkipfishOutputDir), and the root is: % s" % dirname)
                    # add directory (needed for empty dirs)
                    resultZipFile.write(dirname, os.path.relpath(dirname, relroot))
                    for file in files:
                        filename = os.path.join(dirname, file)
                        self.wass.WassLogging.debug("Inside the: for file in files, and the filename is: % s" % filename)
                        if os.path.isfile(filename):  # regular files only
                            arcname = os.path.join(os.path.relpath(dirname, relroot), file)
                            self.wass.WassLogging.debug("Addining the following arcname, filename is: %s : %s" % (arcname, filename))
                            resultZipFile.write(filename, arcname, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the Skipfish Word List File: %s" % self.wass.SkipfishWordList)
            if os.path.isfile(self.wass.SkipfishWordList):
                (filepath, filename) = os.path.split(self.wass.SkipfishWordList)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.SkipfishWordList)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.SkipfishWordList, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "SSLyze"):
            self.wass.WassLogging.debug("Before Adding the SSLyze XML File: %s" % self.wass.SSLyzeXMLReport)
            if os.path.isfile(self.wass.SSLyzeXMLReport):
                (filepath, filename) = os.path.split(self.wass.SSLyzeXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.SSLyzeXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.SSLyzeXMLReport, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "TheHarvester"):
            self.wass.WassLogging.debug("Before Adding the TheHarvester HTML and XML File Name is: %s" % self.wass.TheHarvesterReportName)
            if os.path.isfile(self.wass.TheHarvesterReportName + '.xml'):
                (filepath, filename) = os.path.split(self.wass.TheHarvesterReportName + '.xml')
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.TheHarvesterReportName + '.xml')
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.TheHarvesterReportName + '.xml', filename, zipfile.ZIP_DEFLATED)
            if os.path.isfile(self.wass.TheHarvesterReportName + '.html'):
                (filepath, filename) = os.path.split(self.wass.TheHarvesterReportName + '.html')
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.TheHarvesterReportName + '.html')
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.TheHarvesterReportName + '.html', filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "W3af"):
            self.wass.WassLogging.debug("Before Adding the W3af XML File: %s" % self.wass.W3afXMLReport)
            if os.path.isfile(self.wass.W3afXMLReport):
                (filepath, filename) = os.path.split(self.wass.W3afXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.W3afXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.W3afXMLReport, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the W3af HTML File: %s" % self.wass.W3afHTMLReport)
            if os.path.isfile(self.wass.W3afHTMLReport):
                (filepath, filename) = os.path.split(self.wass.W3afHTMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.W3afHTMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.W3afXMLReport, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "Wapiti"):
            self.wass.WassLogging.debug("Before Adding the Wapiti XML File: %s" % self.wass.WapitiXMLReport)
            if os.path.isfile(self.wass.WapitiXMLReport):
                (filepath, filename) = os.path.split(self.wass.WapitiXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.WapitiXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.WapitiXMLReport, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "WhatWeb"):
            self.wass.WassLogging.debug("Before Adding the WhatWeb XML File: %s" % self.wass.WhatWebXMLReport)
            if os.path.isfile(self.wass.WhatWebXMLReport):
                (filepath, filename) = os.path.split(self.wass.WhatWebXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.WhatWebXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.WhatWebXMLReport, filename, zipfile.ZIP_DEFLATED)
        elif (self.wass.CurrentTask == "ZAProxy"):
            self.wass.WassLogging.debug("Before Adding the ZAProxy XML File: %s" % self.wass.ZAProxyXMLReport)
            if os.path.isfile(self.wass.ZAProxyXMLReport):
                (filepath, filename) = os.path.split(self.wass.ZAProxyXMLReport)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ZAProxyXMLReport)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ZAProxyXMLReport, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the ZAProxy main Session File: %s" % self.wass.ZAProxySessionFile)
            if os.path.isfile(self.wass.ZAProxySessionFile):
                (filepath, filename) = os.path.split(self.wass.ZAProxySessionFile)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ZAProxySessionFile)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ZAProxySessionFile, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the ZAProxy Session Data File: %s" % self.wass.ZAProxySessionDataFile)
            if os.path.isfile(self.wass.ZAProxySessionDataFile):
                (filepath, filename) = os.path.split(self.wass.ZAProxySessionDataFile)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ZAProxySessionDataFile)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ZAProxySessionDataFile, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the ZAProxy Session LCK File: %s" % self.wass.ZAProxySessionLCKFile)
            if os.path.isfile(self.wass.ZAProxySessionLCKFile):
                (filepath, filename) = os.path.split(self.wass.ZAProxySessionLCKFile)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ZAProxySessionLCKFile)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ZAProxySessionLCKFile, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the ZAProxy Session Log File: %s" % self.wass.ZAProxySessionLogFile)
            if os.path.isfile(self.wass.ZAProxySessionLogFile):
                (filepath, filename) = os.path.split(self.wass.ZAProxySessionLogFile)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ZAProxySessionLogFile)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ZAProxySessionLogFile, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the ZAProxy Session Properties File: %s" % self.wass.ZAProxySessionPropertiesFile)
            if os.path.isfile(self.wass.ZAProxySessionPropertiesFile):
                (filepath, filename) = os.path.split(self.wass.ZAProxySessionPropertiesFile)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ZAProxySessionPropertiesFile)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ZAProxySessionPropertiesFile, filename, zipfile.ZIP_DEFLATED)
            self.wass.WassLogging.debug("Before Adding the ZAProxy Session Script File: %s" % self.wass.ZAProxySessionScriptFile)
            if os.path.isfile(self.wass.ZAProxySessionScriptFile):
                (filepath, filename) = os.path.split(self.wass.ZAProxySessionScriptFile)
                self.wass.WassLogging.debug("Adding resultfile: %s" % self.wass.ZAProxySessionScriptFile)
                self.wass.WassLogging.debug("Adding resultfile as: %s" % filename)
                resultZipFile.write(self.wass.ZAProxySessionScriptFile, filename, zipfile.ZIP_DEFLATED)

        resultZipFile.setpassword(self.wass.ZIPPassword)
        resultZipFile.close()
        self.wass.WassLogging.debug("The old working directory is:  %s" % self.wass.ResultDir)
        self.wass.WassLogging.debug("The zipFile is:  %s" % finalZipFile)
        os.chdir(self.wass.ResultDir)
        self.wass.WassLogging.info("Done Creating the Final Result Zip file for the task: %s" % self.wass.CurrentTask)
        self.wass.WassLogging.info("############### Leaving createZipFile ###############")
        return finalZipFile

    def createResultDir(self):
        '''
        Here we create the locally stored Report / Result Path
        '''
        self.wass.WassLogging.info("############### Entering createResultDir ###############")
        self.wass.WassLogging.debug("The Customer is: %s" % self.wass.Customer)
        self.wass.WassLogging.debug("The TargetDomain is: %s" % self.wass.TargetDomain)
        self.wass.WassLogging.debug("The ToDay is: %s" % self.wass.ToDay)
        self.wass.WassLogging.debug("The runTask is: %s" % self.wass.CurrentTask)
        cwd = os.getcwd()
        self.wass.WassLogging.debug("The current Working Directory is: %s" % cwd)
        resultDir = self.wass.ResultDir + '/results/' + self.wass.Customer + '/' + self.wass.TargetDomain + '/' + self.wass.ToDay + '/' + self.wass.CurrentTask + '/scan_result'
        self.wass.WassLogging.debug("The Final Result Directory should be: %s" % resultDir)
        if not os.path.isdir(resultDir):
            self.wass.WassLogging.info("The Final Result Directory did not Exists: %s" % resultDir)
            self.wass.WassLogging.info("Creating the Final Result Directory: %s" % resultDir)
            os.makedirs(resultDir)
        self.wass.WassLogging.info("############### Leaving createResultDir ###############")
        return resultDir

    def moveResultFile(self, file, resultDir):
        '''
        Here we move the individual result file to locally stored report path
        '''
        self.wass.WassLogging.info("############### Entering moveResultFile ###############")
        if os.path.isfile(file):
            self.wass.WassLogging.debug("It is a file, and it is: %s" % file)
            self.wass.WassLogging.info("Moving the file to the Result Directory: %s" % resultDir)
            shutil.move(file, resultDir)
        elif os.path.isdir(file):
            self.wass.WassLogging.debug("It is a Directory, and it is: %s" % file)
            self.wass.WassLogging.info("Moving the directory to the Result Directory: %s" % resultDir)
            shutil.move(file, resultDir)
        else:
            self.wass.WassLogging.debug("The file sent to moveResultFile did not exist!! the file was: %s" % file)
            self.wass.WassLogging.debug("Moving on we caught it in Time")
        self.wass.WassLogging.info("############### Leaving moveResultFile ###############")

    def moveLogFile(self, logFile, resultDir):
        '''
        Here we move the log file to locally stored report path
        '''
        if (self.wass.LogLevel == "DEBUG"):
            print ('Inside the moveLogFile and the logFile is: %s' % logFile)
            print ('Inside the moveLogFile and the resultDir is: %s' % resultDir)
        shutil.move(logFile, resultDir)

    def printInfo(self):
        '''
        Print the relevant Info for the Current Task
        '''
        self.wass.WassLogging.info("############### The variables used in the script are ###############")
        self.wass.WassLogging.info("The Python Version is: %s" % self.wass.PythonVersion)
        self.wass.WassLogging.info("The System OS is: %s" % self.wass.SystemOS)
        self.wass.WassLogging.info("The OS Version is: %s" % self.wass.OSVersion)
        self.wass.WassLogging.info("The CurrentTask is: %s" % self.wass.CurrentTask)
        self.wass.WassLogging.info("The OrgWorkingDir is: %s" % self.wass.OrgWorkingDir)
        self.wass.WassLogging.info("The ResultDir is: %s" % self.wass.ResultDir)
        self.wass.WassLogging.info("The Program(s) to run is: %s" % self.wass.Program)
        self.wass.WassLogging.info("Should we run Arachni: %s" % self.wass.RunArachni)
        self.wass.WassLogging.info("Should we run Fierce: %s" % self.wass.RunFierce)
        self.wass.WassLogging.info("Should we run Nikto: %s" % self.wass.RunNikto)
        self.wass.WassLogging.info("Should we run Nmap: %s" % self.wass.RunNmap)
        self.wass.WassLogging.info("Should we run OpenVAS: %s" % self.wass.RunOpenVAS)
        self.wass.WassLogging.info("Should we run Skipfish: %s" % self.wass.RunSkipfish)
        self.wass.WassLogging.info("Should we run SSLyze: %s" % self.wass.RunSSLyze)
        self.wass.WassLogging.info("Should we run SSLScan: %s" % self.wass.RunSSLScan)
        self.wass.WassLogging.info("Should we run W3af: %s" % self.wass.RunW3af)
        self.wass.WassLogging.info("Should we run Wapiti: %s" % self.wass.RunWapiti)
        self.wass.WassLogging.info("Should we run WhatWeb: %s" % self.wass.RunWhatWeb)
        self.wass.WassLogging.info("Should we run Whois: %s" % self.wass.RunWhois)
        self.wass.WassLogging.info("Should we run ZAProxy: %s" % self.wass.RunZAProxy)
        self.wass.WassLogging.info("The Customer is: %s" % self.wass.Customer)
        self.wass.WassLogging.info("The TargetDomain is: %s" % self.wass.TargetDomain)
        self.wass.WassLogging.info("The TldDomainName is: %s" % self.wass.TldDomainName)
        self.wass.WassLogging.info("The TargetPort is: %s" % self.wass.TargetPort)
        self.wass.WassLogging.info("The TargetURL is: %s" % self.wass.TargetURL)
        self.wass.WassLogging.info("The Exclude URL is: %s" % self.wass.TargetExcludeURLS)
        self.wass.WassLogging.info("The TargetIP is: %s" % self.wass.TargetIP)
        self.wass.WassLogging.info("The ScanTarget is: %s" % self.wass.ScanTarget)
        self.wass.WassLogging.info("The User Name is: %s" % self.wass.AuthUser)
        self.wass.WassLogging.info("The User Password is: %s" % self.wass.AuthPW)
        self.wass.WassLogging.info("The Authentication Type is: %s" % self.wass.AuthType)
        self.wass.WassLogging.info("The Authentication URL is: %s" % self.wass.AuthURL)
        self.wass.WassLogging.info("The Authentication Verify URL is: %s" % self.wass.AuthVerifyURL)
        self.wass.WassLogging.info("The LogLevel is: %s" % self.wass.LogLevel)
        if (self.wass.SendEmail):
            self.wass.WassLogging.info("The ToEmail is: %s" % self.wass.ToEmail)
            self.wass.WassLogging.info("The FromEmail is: %s" % self.wass.FromEmail)
        self.wass.WassLogging.info("The SendEmail is: %s" % self.wass.SendEmail)
        self.wass.WassLogging.info("The ZIPPassword is: %s" % self.wass.ZIPPassword)
        self.wass.WassLogging.info("The Local ZAProxy Protocol is: %s" % self.wass.LocalZAProxyProtocol)
        self.wass.WassLogging.info("The Local ZAProxy Host is: %s" % self.wass.LocalZAProxyHost)
        self.wass.WassLogging.info("The Local ZAProxy Port is: %s" % self.wass.LocalZAProxyPort)
        self.wass.WassLogging.info("The Local ZAProxy is: %s" % self.wass.LocalZAProxy)
        if (self.wass.CurrentTask == "Arachni"):
            self.wass.WassLogging.info("The Arachni Version is: %s" % self.wass.ArachniVersion)
            self.wass.WassLogging.info("The Arachni CMD is: %s" % self.wass.ArachniCMD)
            self.wass.WassLogging.info("The Arachni AuthedBy is: %s" % self.wass.ArachniAuthedBy)
            self.wass.WassLogging.info("The Arachni AFR Report is: %s" % self.wass.ArachniAFRReport)
            self.wass.WassLogging.info("The Arachni XML Report is: %s" % self.wass.ArachniXMLReport)
            self.wass.WassLogging.info("The Arachni HTML Report is: %s" % self.wass.ArachniHTMLReport)
            self.wass.WassLogging.info("The Arachni Error Log is: %s" % self.wass.ArachniErrorLog)
            self.wass.WassLogging.info("The Arachni Command Line is: %s" % self.wass.ArachniCLI)
            self.wass.WassLogging.info("The Arachni Run Log file is: %s" % self.wass.ArachniRunLog)
            self.wass.WassLogging.info("The Arachni WASS Log is: %s" % self.wass.ArachniWassLog)
        if (self.wass.CurrentTask == "Fierce"):
            self.wass.WassLogging.info("The Fierce Version is: %s" % self.wass.FierceVersion)
            self.wass.WassLogging.info("The Fierce CMD is: %s" % self.wass.FierceCMD)
            self.wass.WassLogging.info("The Fierce Command Line is: %s" % self.wass.FierceCLI)
            self.wass.WassLogging.info("The Fierce Arguments is: %s" % self.wass.FierceArguments)
            self.wass.WassLogging.info("The Fierce XML File is: %s" % self.wass.FierceXMLReport)
            self.wass.WassLogging.info("The Fierce Run Log is: %s" % self.wass.FierceRunLog)
            self.wass.WassLogging.info("The Fierce WASS Log is: %s" % self.wass.FierceWassLog)
        if (self.wass.CurrentTask == "Nikto"):
            self.wass.WassLogging.info("The Nikto Version is: %s" % self.wass.NiktoVersion)
            self.wass.WassLogging.info("The Nikto CMD is: %s" % self.wass.NiktoCMD)
            self.wass.WassLogging.info("The Nikto Command Line is: %s" % self.wass.NiktoCLI)
            self.wass.WassLogging.info("The Nikto Arguments is: %s" % self.wass.NiktoArguments)
            self.wass.WassLogging.info("The Nikto XML File is: %s" % self.wass.NiktoXMLReport)
            self.wass.WassLogging.info("The Nikto Run Log is: %s" % self.wass.NiktoRunLog)
            self.wass.WassLogging.info("The Nikto WASS Log is: %s" % self.wass.NiktoWassLog)
        if (self.wass.CurrentTask == "Nmap"):
            self.wass.WassLogging.info("The Nmap Version is: %s" % self.wass.NmapVersion)
            self.wass.WassLogging.info("The Nmap CMD is: %s" % self.wass.NmapCMD)
            self.wass.WassLogging.info("The Nmap XML File is: %s" % self.wass.NmapXML)
            self.wass.WassLogging.info("The Nmap Arguments are: %s" % self.wass.NmapArguments)
            self.wass.WassLogging.info("The Nmap WASS Log is: %s" % self.wass.NmapWassLog)
        if (self.wass.CurrentTask == "Skipfish"):
            self.wass.WassLogging.info("The Skipfish Version is: %s" % self.wass.SkipfishVersion)
            self.wass.WassLogging.info("The Skipfish CMD is: %s" % self.wass.SkipfishCMD)
            self.wass.WassLogging.info("The Skipfish Command Line is: %s" % self.wass.SkipfishCLI)
            self.wass.WassLogging.info("The Skipfish Scan Word List is: %s" % self.wass.SkipfishScanWordList)
            self.wass.WassLogging.info("The Skipfish Word List is: %s" % self.wass.SkipfishWordList)
            self.wass.WassLogging.info("The Skipfish Output Dir is: %s" % self.wass.SkipfishOutputDir)
            self.wass.WassLogging.info("The Skipfish Run Log is: %s" % self.wass.SkipfishRunLog)
            self.wass.WassLogging.info("The Skipfish WASS Log is: %s" % self.wass.SkipfishWassLog)
        if (self.wass.CurrentTask == "SSLScan"):
            self.wass.WassLogging.info("The SSLScan Version is: %s" % self.wass.SSLScanVersion)
            self.wass.WassLogging.info("The SSLScan CMD is: %s" % self.wass.SSLScanCMD)
            self.wass.WassLogging.info("The SSLScan Command Line is: %s" % self.wass.SSLScanCLI)
            self.wass.WassLogging.info("The SSLScan Arguments List is: %s" % self.wass.SSLScanArguments)
            self.wass.WassLogging.info("The SSLScan XML Report is: %s" % self.wass.SSLScanXMLReport)
            self.wass.WassLogging.info("The SSLScan Run Log is: %s" % self.wass.SSLScanRunLog)
            self.wass.WassLogging.info("The SSLScan WASS Log is: %s" % self.wass.SSLScanWassLog)
        if (self.wass.CurrentTask == "SSLyze"):
            self.wass.WassLogging.info("The SSLyze Version is: %s" % self.wass.SSLyzeVersion)
            self.wass.WassLogging.info("The SSLyze CMD is: %s" % self.wass.SSLyzeCMD)
            self.wass.WassLogging.info("The SSLyze Command Line is: %s" % self.wass.SSLyzeCLI)
            self.wass.WassLogging.info("The SSLyze Arguments is: %s" % self.wass.SSLyzeArguments)
            self.wass.WassLogging.info("The SSLyze XML Report is: %s" % self.wass.SSLyzeXMLReport)
            self.wass.WassLogging.info("The SSLyze Run Log is: %s" % self.wass.SSLyzeRunLog)
            self.wass.WassLogging.info("The SSLyze WASS Log is: %s" % self.wass.SSLyzeWassLog)
        if (self.wass.CurrentTask == "TheHarvester"):
            self.wass.WassLogging.info("The TheHarvester Version is: %s" % self.wass.TheHarvesterVersion)
            self.wass.WassLogging.info("The TheHarvester CMD is: %s" % self.wass.TheHarvesterCMD)
            self.wass.WassLogging.info("The TheHarvester Command Line is: %s" % self.wass.TheHarvesterCLI)
            self.wass.WassLogging.info("The TheHarvester Arguments is: %s" % self.wass.TheHarvesterArguments)
            self.wass.WassLogging.info("The TheHarvester Report Name is: %s" % self.wass.TheHarvesterReportName)
            self.wass.WassLogging.info("The TheHarvester Run Log is: %s" % self.wass.TheHarvesterRunLog)
            self.wass.WassLogging.info("The TheHarvester WASS Log is: %s" % self.wass.TheHarvesterWassLog)
        if (self.wass.CurrentTask == "W3af"):
            self.wass.WassLogging.info("The W3af Version is: %s" % self.wass.W3afVersion)
            self.wass.WassLogging.info("The W3af CMD is: %s" % self.wass.W3afCMD)
            self.wass.WassLogging.info("The W3af Command Line is: %s" % self.wass.W3afCLI)
            self.wass.WassLogging.info("The W3af Command File is: %s" % self.wass.W3afCMDFile)
            self.wass.WassLogging.info("The W3af Profile is: %s" % self.wass.W3afProfile)
            self.wass.WassLogging.info("The W3af XML Report is: %s" % self.wass.W3afXMLReport)
            self.wass.WassLogging.info("The W3af HTML Report is: %s" % self.wass.W3afHTMLReport)
            self.wass.WassLogging.info("The W3af HTTP Out is: %s" % self.wass.W3afHTTPOut)
            self.wass.WassLogging.info("The W3af Responce Out is: %s" % self.wass.W3afRepOut)
            self.wass.WassLogging.info("The W3af Run Log is: %s" % self.wass.W3afRunLog)
            self.wass.WassLogging.info("The W3af WASS Log is: %s" % self.wass.W3afWassLog)
        if (self.wass.CurrentTask == "Wapiti"):
            self.wass.WassLogging.info("The Wapiti Version is: %s" % self.wass.WapitiVersion)
            self.wass.WassLogging.info("The Wapiti CMD is: %s" % self.wass.WapitiCMD)
            self.wass.WassLogging.info("The Wapiti Command Line is: %s" % self.wass.WapitiCLI)
            self.wass.WassLogging.info("The Wapiti XML Report is: %s" % self.wass.WapitiXMLReport)
            self.wass.WassLogging.info("The Wapiti Run Log file is: %s" % self.wass.WapitiRunLog)
            self.wass.WassLogging.info("The Wapiti WASS Log is: %s" % self.wass.WapitiWassLog)
        if (self.wass.CurrentTask == "WhatWeb"):
            self.wass.WassLogging.info("The WhatWeb Version is: %s" % self.wass.WhatWebVersion)
            self.wass.WassLogging.info("The WhatWeb CMD is: %s" % self.wass.WhatWebCMD)
            self.wass.WassLogging.info("The WhatWeb Command Line is: %s" % self.wass.WhatWebCLI)
            self.wass.WassLogging.info("The WhatWeb XML Report is: %s" % self.wass.WhatWebXMLReport)
            self.wass.WassLogging.info("The WhatWeb Run log is: %s" % self.wass.WhatWebRunLog)
            self.wass.WassLogging.info("The WhatWeb WASS Log is: %s" % self.wass.WhatWebWassLog)
        if (self.wass.CurrentTask == "Whois"):
            self.wass.WassLogging.info("The Whois Version is: %s" % self.wass.WhoisVersion)
            self.wass.WassLogging.info("The Whois Target XML Report is: %s" % self.wass.WhoisTargetXMLReport)
            self.wass.WassLogging.info("The Whois Target IP XML Report is: %s" % self.wass.WhoisTargetIPXMLReport)
            self.wass.WassLogging.info("The Whois CMD is: %s" % self.wass.WhoisCMD)
            self.wass.WassLogging.info("The Wois WASS Log is: %s" % self.wass.WhoisWassLog)
        if (self.wass.CurrentTask == "OpenVAS"):
            self.wass.WassLogging.info("The OpenVAS Version is: %s" % self.wass.OpenVASVersion)
            self.wass.WassLogging.info("The OpenVAS CMD is: %s" % self.wass.OpenVASCMD)
            self.wass.WassLogging.info("The OpenVAS User is: %s" % self.wass.OpenVASUser)
            self.wass.WassLogging.info("The OpenVAS Password is: %s" % self.wass.OpenVASPassword)
            self.wass.WassLogging.info("The OpenVAS Host is: %s" % self.wass.OpenVASHost)
            self.wass.WassLogging.info("The OpenVAS PortList is: %s" % self.wass.OpenVASPortListID)
            self.wass.WassLogging.info("The OpenVAS ScanConfig is: %s" % self.wass.OpenVASScanConfig)
            self.wass.WassLogging.info("The OpenVAS WASS Log is: %s" % self.wass.OpenVASWassLog)
        if (self.wass.CurrentTask == "ZAProxy"):
            self.wass.WassLogging.info("The ZAProxy Version is: %s" % self.wass.ZAProxyVersion)
            self.wass.WassLogging.info("The ZAProxy Path is: %s" % self.wass.ZAProxyPath)
            self.wass.WassLogging.info("The ZAProxy CMD is: %s" % self.wass.ZAProxyCMD)
            self.wass.WassLogging.info("The ZAProxy CLI is: %s" % self.wass.ZAProxyCLI)
            self.wass.WassLogging.info("The ZAProxy Daemon is: %s" % self.wass.ZAProxyDaemon)
            self.wass.WassLogging.info("The ZAProxy AttackStrength is: %s" % self.wass.ZAProxyAttackStrength)
            self.wass.WassLogging.info("The ZAProxy Start is: %s" % self.wass.ZAProxyStart)
            self.wass.WassLogging.info("The ZAProxy Stop is: %s" % self.wass.ZAProxyStop)
            self.wass.WassLogging.info("The ZAProxy XMLReport is: %s" % self.wass.ZAProxyXMLReport)
            self.wass.WassLogging.info("The ZAProxy Session file is: %s" % self.wass.ZAProxySessionFile)
            self.wass.WassLogging.info("The ZAProxy Session Data file is: %s" % self.wass.ZAProxySessionDataFile)
            self.wass.WassLogging.info("The ZAProxy Session Lock file is: %s" % self.wass.ZAProxySessionLCKFile)
            self.wass.WassLogging.info("The ZAProxy Session Log file is: %s" % self.wass.ZAProxySessionLogFile)
            self.wass.WassLogging.info("The ZAProxy Session Properties file is: %s" % self.wass.ZAProxySessionPropertiesFile)
            self.wass.WassLogging.info("The ZAProxy Session Scripts file is: %s" % self.wass.ZAProxySessionScriptFile)
            self.wass.WassLogging.info("The ZAProxy WASS Log is: %s" % self.wass.ZAProxyWassLog)
        self.wass.WassLogging.info("The ResultDir is: %s" % self.wass.ResultDir)
        self.wass.WassLogging.info("The reportDate is: %s" % self.wass.ReportDate)
        self.wass.WassLogging.info("The toDay is: %s" % self.wass.ToDay)
        self.wass.WassLogging.info("")
        self.wass.WassLogging.info("")
