'''
wapiti.py

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


class WassSQLMap(object):
    '''
    This is the WassSQLMap class
    '''

    def __init__(self, wass):
        '''
        Initialize WassSQLMap module
        '''
        self.wass = wass

    def RunSQLMap(self):
        '''
        Run the SQLMap CLI Command
        '''
        # Setup the logging, we are about to use it in wasslib.WassCommon.Common !!!!!
        self.wass.SQLMapWassLog = "SQLMap_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"
        self.wass.SQLMapRunLog = "SQLMap_Run_" + self.wass.TargetDomain + "_" + self.wass.ReportDate + ".log"        
        self.wass.WassLogging.CreateLogfile(self.wass.SQLMapWassLog)
        self.wass.WassCommon.printInfo()
        # Get the Dynamic parameters
        self.wass.WassCommon.getDynamic()

        self.wass.WassLogging.info("############### SQLMap WASS Run Starting ###############")

        self.wass.WassLogging.info("############### SQLMap WASS Run Done ###############")
