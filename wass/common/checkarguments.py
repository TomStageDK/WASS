'''
checkarguments.py

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


class WassCheckArguments(object):
    '''
    This is the WassCheckArguments class
    '''

    def __init__(self, wass):
        '''
        Initialize WassCheckArguments module
        '''
        self.wass = wass

    def checkArachniArguments(self):
        '''
        Check the arguments Arachni from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.ArachniArguments
        '''
        for used_arguments in ['--authed-by', '--exclude', '--proxy', '--proxy-type', '--report=afr:outfile']:
            assert not used_arguments in self.wass.ArachniArguments, 'There is is an error with the arguments for Arachni in the wass.config file'

    def checkFierceArguments(self):
        '''
        Check the arguments Fierce from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.FierceArguments
        '''
        for used_arguments in ['-dns', '-format', '-output', '-template', '-debug']:
            assert not used_arguments in self.wass.FierceArguments, 'There is is an error with the arguments for Fierce in the wass.config file'

    def checkNiktoArguments(self):
        '''
        Check the arguments Nikto from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.NiktoArguments
        '''
        for used_arguments in ['-h', '-vhost', '-port', '-root', '-useproxy', '-ask', '-output', '-Format']:
            assert not used_arguments in self.wass.NiktoArguments, 'There is is an error with the arguments for Nikto in the wass.config file'

    def checkNmapArguments(self):
        '''
        Check the arguments Nmap from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.NmapArguments
        '''
        for used_arguments in ['-oX', '-oA', '-p']:
            assert not used_arguments in self.wass.NmapArguments, 'There is is an error with the arguments for Nmap in the wass.config file'

    def checkSkipfishArguments(self):
        '''
        Check the arguments Skipfish from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.SkipfishArguments
        '''
        for used_arguments in ['-I', '-o', '-W', '-S', '-x']:
            assert not used_arguments in self.wass.NmapArguments, 'There is is an error with the arguments for Skipfish in the wass.config file'

    def checkSSLyzeArguments(self):
        '''
        Check the arguments SSLyze from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.SSLyzeArguments
        '''
        for used_arguments in ['--xml_out', '--regular', '--https_tunnel', '--certinfo']:
            assert not used_arguments in self.wass.SSLyzeArguments, 'There is is an error with the arguments for SSLyze in the wass.config file'

    def checkSSLScanArguments(self):
        '''
        Check the arguments SSLScan from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.SSLScanArguments
        '''
        for used_arguments in ['--xml']:
            assert not used_arguments in self.wass.SSLScanArguments, 'There is is an error with the arguments for SSLScan in the wass.config file'

    def checkTheHarvesterArguments(self):
        '''
        Check the arguments TheHarvester from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.TheHarvesterArguments
        '''
        for used_arguments in ['-d', '-f']:
            assert not used_arguments in self.wass.TheHarvesterArguments, 'There is is an error with the arguments for TheHarvester in the wass.config file'

    def checkWapitiArguments(self):
        '''
        Check the arguments Wapiti from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.WapitiArguments
        '''
        for used_arguments in ['-x', '-p', '-f', '-o']:
            assert not used_arguments in self.wass.WapitiArguments, 'There is is an error with the arguments for Wapiti in the wass.config file'

    def checkWhatWebArguments(self):
        '''
        Check the arguments WhatWeb from the wass.config file to make sure that the once,
        that are hard coded in WASS is not defined there as well!!!

        cheks: self.wass.WhatWebArguments
        '''
        for used_arguments in ['--log-xml', '--proxy', '--color']:
            assert not used_arguments in self.wass.WhatWebArguments, 'There is is an error with the arguments for WhatWeb in the wass.config file'
