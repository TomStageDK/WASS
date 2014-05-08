## WASS - Web Application Security Scan

Bare in mind that I am not a programmer, and therefore there could be some things that could have been done smarter or better,
but my 1st goal is to have the functions that i need for my self. 

`WASS` is a set of Python scripts and modules that will conduct an automated Web Application Scan and information gathering with the tested tools below.

The goal of WASS is to do a scan of a given site / target application, with all tested tools below, to have a more comprehensive result in the end.
WASS will direct all the traffic from all the web application scanning tools to go thru the ZAProxy (Need to do some stability testing of this, i might be my virtual machine that have the stability issues).

It will scan the target with some default options configure in the application during the scan, and it takes arguments to all the tools as well,
this is configure in the wass.config.

It will create a Log file for each program that is run, and move all the result files in to a given directory structure for the scan target and tool that is run.

It can run each of the tools in a "solo" run, or all of them for a complete run (WARNING this can take a long time to complete).

Another goal of WASS is to unify all the results (ATM only the results that are in XML files).
I considered both of the following formats:

`Simple Software Vulnerability Language (SSVL)`

or 

`OWASP Data Exchange Format`

But since both of these are under development it can change along the way, but for now i have decided to use the DEF format.

`Simple Software Vulnerability Language (SSVL)` - https://github.com/OWASP/SSVL

`OWASP Data Exchange Format` - https://www.owasp.org/index.php/OWASP_Data_Exchange_Format_Project - http://code.google.com/p/owasp-def/

On a side note, i have decided to use the DEF format to create a WASS XML format, which i will develop along the way, and for this purpose i have created
a XSL file for a decent HTML report, but note that i have not created any parsers to this format yet, but my plan is to convert all other XML formats to the DEF format,
and then create the WASS XML for the purpose of a general XML report from the WASS run. 

My plan is also to be able to create a PDF report directly from the WASS run.


## Tested with and Dependencies
	OS:
	CentOS 6.5
	
	Software:
	Python 2.6, 2.7
	
	Arachni 0.4.x Can be downloaded from: http://www.arachni-scanner.com/download/
	Fierce 2.0-r420 Can be downloaded from: http://trac.assembla.com/fierce
	Nikto 2.x Can be downloaded from: https://www.cirt.net/Nikto2
	Nmap 6.x Can be downloaded from: http://nmap.org/download.html
	OpenVAS-6 Can be downloaded from: http://www.openvas.org/download.html
	Skipfish 2.09b, 2.10b Can be downloaded from: https://code.google.com/p/skipfish/downloads/list
	SSLyze 0.9 Can be downloaded from: https://github.com/iSECPartners/sslyze
	SSLScan 1.8.0 Can be downloaded from: https://www.titania.com/freetools?tool=sslscanner
	w3af 1.1, 1.6 Can be downloaded from: http://w3af.org/download
	Wapiti 2.3.0 Can be downloaded from: http://wapiti.sourceforge.net/
	WhatWeb 0.4.7 Can be downloaded from: http://www.morningstarsecurity.com/research/whatweb
	jwhois 4.0 Can be downloaded from: https://www.gnu.org/software/jwhois/
	ZAProxy 2.x Can be downloaded from: http://code.google.com/p/zaproxy/wiki/Downloads?tm=2
    
    Python modules:
    pip 1.5.4 On Centos 6.x the version of pip from epel is 1.3.1 which apparently fails after the installation of the latest version of 
    		 requests so i ran the following command to get pip working once more:  pip install -U pip
    python-owasp-zap-v2 0.0.8 Installation information can be found here: https://pypi.python.org/pypi/python-owasp-zap-v2
    tld 0.6.3 Installation information can be found here: https://pypi.python.org/pypi/tld/
    pythonwhois 2.1.2 Installation information can be found here: https://pypi.python.org/pypi/pythonwhois
    argparse 1.1 Installation information can be found here: https://pypi.python.org/pypi/argparse
    requests 2.2.1 Installation information can be found here: http://docs.python-requests.org/en/latest/user/install/ 
    		 (This was / is part of CentOS 6.x but it is only version 1.1.0, so i updated it to get the latest features, 
    		 at the time of writing this, the version was: 2.2.1, i ran the following command to update: pip install requests --upgrade)
    ipaddr 2.1.11 Installation information can be found here: https://pypi.python.org/pypi/ipaddr/
    reportlab 2.3 Installation information can be found here: https://pypi.python.org/pypi/reportlab/2.3
    PIL 1.1.7 Installation information can be found here: http://www.pythonware.com/products/pil/

## Installation
WASS is developed on Windows 7 with Eclipse and PyDev, for CentOS 6.x and some of the Dependencies are available as native .rpm packages either from base or the Atomicorp yum repositories (http://www.atomicorp.com/channels/).

WASS is mainly dependent on the ZAProxy, since its proxy function is used by many of the other Web Application Scanning tools.

Read the doc/Installing_W3af_1.6_On_CentOS6.x_HowTo.txt for howto install Python 2.7.6 and 3.3.5 on CentOS 6.5.

To use w3af 1.6 you need to have Python 2.7.6


## Code documentation
Read the code;

## Roadmap
Read the doc/TODO to see what i have planned for the future.

## Known bugs and Errors
OpenVAS-6 don´t work, this is because of an error in the responce from the change config command.
Working on getting the W3af automated scan to work.
