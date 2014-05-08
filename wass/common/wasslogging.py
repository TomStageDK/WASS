'''
wasslogging.py

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
#

__author__ = 'Tom Stage (voronwe@voronwe.dk)'
__updated__ = '2014.04.27'

import sys
import time


class WassLogging(object):
    '''
    This is the WASS LogFile class

    This class will handle all the logging done by the application.
    It will create an log file for each process that is run.
    '''

    def __init__(self, wass):
        '''
        Initialize WassLogging module
        '''
        self.wass = wass
        # File handlers
        self._task_log = None

    def CreateLogfile(self, taskLogFile):
        '''
        Create the LogFile for the Current running task

        @parameter taskLogFile: The Log file to create.
        '''
        # Lets try and open the WASS Task Log file
        try:
            self._task_log = open(taskLogFile, "w", 0)
        except IOError, io:
            msg = 'Can\'t open the Log File for Writing, the error is: "'
            msg += ': "' + io.strerror + '".'
            raise self.wass.WassException.WassException(msg)
        except Exception, e:
            msg = 'Can\'t open the Log File for Writing, the error is: "'
            msg += str(e) + '".'
            raise self.wass.WassException.WassException(msg)

    def stopLogging(self):
        '''
        Create the LogFile for the Current running task
        '''
        if (self._task_log is not None):
            self._task_log.close()
        # File handlers
        # Make sure that it gets reset each time we call this function!!
        self._task_log = None

    def _cleanString(self, stringToClean):
        '''
        @parameter stringToClean: A string that should be cleaned before using it in a message object.
        '''
        #('\n','\\n'), ('\r','\\r')
        for char, replace in [('\0', '\\0'), ('\t', '\\t')]:
            stringToClean = stringToClean.replace(char, replace)
        return stringToClean

    def _write_to_file(self, msg):
        '''
        Write to the log files

        @parameter msg: The text to write
        '''
        writeToFile = self._cleanString(msg)
        try:
            self._task_log.write(writeToFile)
        except Exception as e:
            print ('An exception was raised while trying to write to the Current Task WASS Log: %s' % e)
            sys.exit(-1)

    def debug(self, message, newLine=True):
        '''
        This method is called from the output object. The output object was called from a plugin
        or from the framework. This method should take an action for debug messages.

        @parameter message: The text to write.
        @parameter newLine: Whether or not to write \n at the end of the message
        '''
        if (self.wass.LogLevel == "DEBUG"):
            to_print = message

            now = time.localtime(time.time())
            the_time = time.strftime("%c", now)
            timestamp = '[ ' + the_time + ' - debug ] '

            to_print = timestamp + to_print
            to_print = to_print.replace('\n', '\n' + timestamp)
            if newLine == True:
                to_print += '\n'

            self._write_to_file(to_print)

    def info(self, message, newLine=True):
        '''
        This method is called from the output object. The output object was called from a plugin
        or from the framework. This method should take an action for informational messages.

        @parameter message: The text to write.
        @parameter newLine: Whether or not to write \n at the end of the message
        '''
        to_print = message

        now = time.localtime(time.time())
        the_time = time.strftime("%c", now)
        timestamp = '[ ' + the_time + ' - information ] '

        to_print = timestamp + to_print
        to_print = to_print.replace('\n', '\n' + timestamp)

        if newLine == True:
            to_print += '\n'

        self._write_to_file(to_print)

    def error(self, message, newLine=True):
        '''
        This method is called from the output object. The output object was called from a plugin
        or from the framework. This method should take an action for error messages.

        @parameter message: The text to write.
        @parameter newLine: Whether or not to write \n at the end of the message
        '''
        if (self.wass.LogLevel == "ERROR"):
            to_print = message
            if newLine == True:
                to_print += '\n'

            now = time.localtime(time.time())
            the_time = time.strftime("%c", now)
            timestamp = '[ ' + the_time + ' - error ] '

            self._write_to_file(timestamp + to_print)

    def infoNoFormatting(self, msg):
        '''
        Write to the log file without any formatting.

        @parameter msg: The text to write.
        '''
        try:
            self._task_log.write(msg)
        except Exception as e:
            print ('An exception was raised while trying to write infoNoFormatting output to the Log file: %s' % e)
            sys.exit(1)

    def debugNoFormatting(self, msg):
        '''
        Write to the log file without any formatting.

        @parameter msg: The text to write.
        '''
        if (self.wass.LogLevel == "DEBUG"):
            try:
                self._task_log.write(msg)
            except Exception, e:
                print ('An exception was raised while trying to write debugNoFormatting output to the Log file: %s' % e)
                sys.exit(1)
