'''
wassexception.py

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


class WassException(Exception):
    '''
    This is the WASS Exception class
    '''

    def __init__(self, value):
        '''
        Initialize WassException module
        '''
        Exception.__init__(self)
        self.value = str(value)

    def __str__(self):
        return self.value
