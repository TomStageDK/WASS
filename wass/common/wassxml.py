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
__updated__ = '2014.05.06'

import os
import base64
import xml.dom.minidom
import xml.parsers
try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree


class WassXML(object):
    '''
    This is the WassXML class
    '''

    def __init__(self, wass):
        '''
        Initialize WassXML module
        '''
        self.wass = wass

    def classifyOWASPVulnerability(self):
        '''
        Reclassify Vulnerability
        This will reclassify a Vulnerability acording to the OWASP top 10 2013:
        A1-Injections = Critical
        A2-Broken Authentication and Session Management = Critical
        A3-Cross-Site Scripting (XSS) = Critical
        A4-Insecure Direct Object References = 
        A5-Security Misconfiguration = 
        A6-Sensitive Data Exposure = Critical
        A7-Missing Function Level Access Control = 
        A8-Cross-Site Request Forgery (CSRF) = 
        A9-Using Components with Known Vulnerabilities = 
        A10-Unvalidated Redirects and Forwards = 
        '''
        self.wass.WassLogging.info("############### classifyVulnerability Starting ###############")
        self.wass.WassLogging.info("############### classifyVulnerability Done ###############")

    def CheckForSQLInjection(self):
        '''
        Check the XML file for the Currents Task and look for possible SQL Injections.
        If an SQL Injection is found in the result file for the Current Task we run SQLMap against it.
        '''
        self.wass.WassLogging.info("############### CheckForSQLInjection Run Starting ###############")
        if (self.wass.CurrentTask == 'Arachni'):
            pass
        elif (self.wass.CurrentTask == 'Nikto'):
            pass
        elif (self.wass.CurrentTask == 'W3af'):
            pass
        elif (self.wass.CurrentTask == 'Wapiti'):
            pass
        elif (self.wass.CurrentTask == 'ZAProxy'):
            pass
        self.wass.WassLogging.info("############### CheckForSQLInjection Run Done ###############")

    def ConvertToDEF(self):
        '''
        Convert the XML file for the Currents Task into the OWASP Data Exchange Format.
        '''
        self.wass.WassLogging.info("############### ConvertToDEF Run Starting ###############")
        if (self.wass.CurrentTask == 'Arachni'):
            pass
        elif (self.wass.CurrentTask == 'Nikto'):
            pass
        elif (self.wass.CurrentTask == 'Nmap'):
            pass
        elif (self.wass.CurrentTask == 'OpenVAS'):
            pass
        elif (self.wass.CurrentTask == 'W3af'):
            pass
        elif (self.wass.CurrentTask == 'Wapiti'):
            pass
        elif (self.wass.CurrentTask == 'ZAProxy'):
            pass
        self.wass.WassLogging.info("############### ConvertToDEF Run Done ###############")

    def DEFtoWASSXML(self):
        '''
        Convert the XML file for the Currents Task into the WASS XML Format (DEF Extended).
        '''
        self.wass.WassLogging.info("############### ConvertToDEF Run Starting ###############")
        if (self.wass.CurrentTask == 'Arachni'):
            pass
        elif (self.wass.CurrentTask == 'Nikto'):
            pass
        elif (self.wass.CurrentTask == 'Nmap'):
            pass
        elif (self.wass.CurrentTask == 'OpenVAS'):
            pass
        elif (self.wass.CurrentTask == 'W3af'):
            pass
        elif (self.wass.CurrentTask == 'Wapiti'):
            pass
        elif (self.wass.CurrentTask == 'ZAProxy'):
            pass
        self.wass.WassLogging.info("############### ConvertToDEF Run Done ###############")

    def ConvertToSSVL(self):
        '''
        Convert the XML file for the Currents Task into the Simple Software Vulnerability Language (SSVL).
        '''
        self.wass.WassLogging.info("############### ConvertToSSVL Run Starting ###############")
        if (self.wass.CurrentTask == 'Arachni'):
            pass
        elif (self.wass.CurrentTask == 'Nikto'):
            pass
        elif (self.wass.CurrentTask == 'Nmap'):
            pass
        elif (self.wass.CurrentTask == 'OpenVAS'):
            pass
        elif (self.wass.CurrentTask == 'W3af'):
            pass
        elif (self.wass.CurrentTask == 'Wapiti'):
            pass
        elif (self.wass.CurrentTask == 'ZAProxy'):
            pass
        self.wass.WassLogging.info("############### ConvertToSSVL Run Done ###############")

    def createWhoisXML(self, whois, target, report):
        '''
        Create an XML file from the Whois query
        '''
        self.wass.WassLogging.info("############### Whois WASS XML Starting ###############")
        #if (self.wass.LogLevel == 'DEBUG'):
        #    print whois
            #if (os.path.isfile(self.wass.OrgWorkingDir+'/whois_object_'+ target + '.txt')):
            #    whois_dict = open(self.wass.OrgWorkingDir+'/whois_object_'+ target + '.txt', "a", 0 )
            #    whois_dict.writelines(whois)
            #else:
            #    whois_dict = open(self.wass.OrgWorkingDir+'/whois_object_'+ target + '.txt', "w", 0 )
            #    whois_dict.writelines(whois)

        _xmldoc = xml.dom.minidom.Document()
        _topElement = _xmldoc.createElement("Whois")
        _topElement.setAttribute("SpecVersion", "0.1")
        target_element = _xmldoc.createElement("target")
        target_data = _xmldoc.createTextNode(target)
        target_element.appendChild(target_data)
        _topElement.appendChild(target_element)

        version_element = _xmldoc.createElement("version")
        version_data = _xmldoc.createTextNode(self.wass.WhoisVersion)
        version_element.appendChild(version_data)
        _topElement.appendChild(version_element)

        if ('id' in whois and not (whois['id'] is None)):
            domainid_element = _xmldoc.createElement("domainids")
            for value in whois['id']:
                domainid_elements = _xmldoc.createElement("id")
                domainid_data = _xmldoc.createTextNode(value)
                domainid_elements.appendChild(domainid_data)
                domainid_element.appendChild(domainid_elements)
            _topElement.appendChild(domainid_element)

        if ('status' in whois and not (whois['status'] is None)):
            status_element = _xmldoc.createElement("status")
            for value in whois['status']:
                status_elements = _xmldoc.createElement("status")
                status_data = _xmldoc.createTextNode(value)
                status_elements.appendChild(status_data)
                status_element.appendChild(status_elements)
            _topElement.appendChild(status_element)

        if ('creation_date' in whois and not (whois['creation_date'] is None)):
            creation_date_element = _xmldoc.createElement("creation_date")
            for value in whois['creation_date']:
                creation_date_elements = _xmldoc.createElement("creation_date")
                creation_date_data = _xmldoc.createTextNode(str(value))
                creation_date_elements.appendChild(creation_date_data)
                creation_date_element.appendChild(creation_date_elements)
            _topElement.appendChild(creation_date_element)

        if ('expiration_date' in whois and not (whois['expiration_date'] is None)):
            expiration_date_element = _xmldoc.createElement("expiration_date")
            for value in whois['expiration_date']:
                expiration_date_elements = _xmldoc.createElement("expiration_date")
                expiration_date_data = _xmldoc.createTextNode(str(value))
                expiration_date_elements.appendChild(expiration_date_data)
                expiration_date_element.appendChild(expiration_date_elements)
            _topElement.appendChild(expiration_date_element)

        if ('updated_date' in whois and not (whois['updated_date'] is None)):
            updated_date_element = _xmldoc.createElement("updated_date")
            for value in whois['updated_date']:
                updated_date_elements = _xmldoc.createElement("updated_date")
                updated_date_data = _xmldoc.createTextNode(str(value))
                updated_date_elements.appendChild(updated_date_data)
                updated_date_element.appendChild(updated_date_elements)
            _topElement.appendChild(updated_date_element)

        if ('registrar' in whois and not (whois['registrar'] is None)):
            registrar_element = _xmldoc.createElement("registrar")
            for value in whois['registrar']:
                registrar_elements = _xmldoc.createElement("registrar")
                registrar_data = _xmldoc.createTextNode(value)
                registrar_elements.appendChild(registrar_data)
                registrar_element.appendChild(registrar_elements)
            _topElement.appendChild(registrar_element)

        if ('whois_server' in whois and not (whois['whois_server'] is None)):
            whois_server_element = _xmldoc.createElement("whois_server")
            for value in whois['whois_server']:
                whois_server_elements = _xmldoc.createElement("whois_server")
                whois_server_data = _xmldoc.createTextNode(value)
                whois_server_elements.appendChild(whois_server_data)
                whois_server_element.appendChild(whois_server_elements)
            _topElement.appendChild(whois_server_element)

        if ('nameservers' in whois and not (whois['nameservers'] is None)):
            nameservers_element = _xmldoc.createElement("nameservers")
            for value in whois['nameservers']:
                nameservers_elements = _xmldoc.createElement("nameserver")
                nameservers_data = _xmldoc.createTextNode(value)
                nameservers_elements.appendChild(nameservers_data)
                nameservers_element.appendChild(nameservers_elements)
            _topElement.appendChild(nameservers_element)

        if ('emails' in whois and not (whois['emails'] is None)):
            emails_element = _xmldoc.createElement("emails")
            for value in whois['emails']:
                emails_elements = _xmldoc.createElement("email")
                emails_data = _xmldoc.createTextNode(value)
                emails_elements.appendChild(emails_data)
                emails_element.appendChild(emails_elements)
            _topElement.appendChild(emails_element)

        if ('contacts' in whois and not (whois['contacts'] is None)):
            if ('admin' in whois['contacts'] and not (whois['contacts']['admin'] is None)):
                admin_element = _xmldoc.createElement("admin")
                for value in whois['contacts']['admin']:
                    admin_elements = _xmldoc.createElement("admin")
                    admin_data = _xmldoc.createTextNode(value)
                    admin_elements.appendChild(admin_data)
                    admin_element.appendChild(admin_elements)
                _topElement.appendChild(admin_element)

        if ('contacts' in whois and not (whois['contacts'] is None)):
            if ('tech' in whois['contacts'] and not (whois['contacts']['tech'] is None)):
                tech_element = _xmldoc.createElement("tech")
                for value in whois['contacts']['tech']:
                    tech_elements = _xmldoc.createElement("tech")
                    tech_data = _xmldoc.createTextNode(value)
                    tech_elements.appendChild(tech_data)
                    tech_element.appendChild(tech_elements)
                _topElement.appendChild(tech_element)

        if ('contacts' in whois and not (whois['contacts'] is None)):
            if ('registrant' in whois['contacts'] and not (whois['contacts']['registrant'] is None)):
                registrant_element = _xmldoc.createElement("registrant")
                for value in whois['contacts']['registrant']:
                    registrant_elements = _xmldoc.createElement("registrant")
                    registrant_data = _xmldoc.createTextNode(value)
                    registrant_elements.appendChild(registrant_data)
                    registrant_element.appendChild(registrant_elements)
                _topElement.appendChild(registrant_element)

        if ('contacts' in whois and not (whois['contacts'] is None)):
            if ('billing' in whois['contacts'] and not (whois['contacts']['billing'] is None)):
                billing_element = _xmldoc.createElement("billing")
                for value in whois['contacts']['billing']:
                    billing_elements = _xmldoc.createElement("billing")
                    billing_data = _xmldoc.createTextNode(value)
                    billing_elements.appendChild(billing_data)
                    billing_element.appendChild(billing_elements)
                _topElement.appendChild(billing_element)

        if ('handle' in whois and not (whois['handle'] is None)):
            handle_element = _xmldoc.createElement("handle")
            for value in whois['handle']:
                handle_elements = _xmldoc.createElement("handle")
                handle_data = _xmldoc.createTextNode(value)
                handle_elements.appendChild(handle_data)
                handle_element.appendChild(handle_elements)
            _topElement.appendChild(handle_element)

        if ('name' in whois and not (whois['name'] is None)):
            name_element = _xmldoc.createElement("name")
            for value in whois['name']:
                name_elements = _xmldoc.createElement("name")
                name_data = _xmldoc.createTextNode(value)
                name_elements.appendChild(name_data)
                name_element.appendChild(name_elements)
            _topElement.appendChild(name_element)

        if ('organization' in whois and not (whois['organization'] is None)):
            organization_element = _xmldoc.createElement("organization")
            for value in whois['organization']:
                organization_elements = _xmldoc.createElement("organization")
                organization_data = _xmldoc.createTextNode(value)
                organization_elements.appendChild(organization_data)
                organization_element.appendChild(organization_elements)
            _topElement.appendChild(organization_element)

        if ('street' in whois and not (whois['street'] is None)):
            street_element = _xmldoc.createElement("street")
            for value in whois['street']:
                street_elements = _xmldoc.createElement("street")
                street_data = _xmldoc.createTextNode(value)
                street_elements.appendChild(street_data)
                street_element.appendChild(street_elements)
            _topElement.appendChild(street_element)

        if ('postalcode' in whois and not (whois['postalcode'] is None)):
            postalcode_element = _xmldoc.createElement("postalcode")
            for value in whois['postalcode']:
                postalcode_elements = _xmldoc.createElement("postalcode")
                postalcode_data = _xmldoc.createTextNode(value)
                postalcode_elements.appendChild(postalcode_data)
                postalcode_element.appendChild(postalcode_elements)
            _topElement.appendChild(postalcode_element)

        if ('city' in whois and not (whois['city'] is None)):
            city_element = _xmldoc.createElement("city")
            for value in whois['city']:
                city_elements = _xmldoc.createElement("city")
                city_data = _xmldoc.createTextNode(value)
                city_elements.appendChild(city_data)
                city_element.appendChild(city_elements)
            _topElement.appendChild(city_element)

        if ('state' in whois and not (whois['state'] is None)):
            state_element = _xmldoc.createElement("state")
            for value in whois['state']:
                state_elements = _xmldoc.createElement("state")
                state_data = _xmldoc.createTextNode(value)
                state_elements.appendChild(state_data)
                state_element.appendChild(state_elements)
            _topElement.appendChild(city_element)

        if ('country' in whois and not (whois['country'] is None)):
            country_element = _xmldoc.createElement("country")
            for value in whois['country']:
                country_elements = _xmldoc.createElement("country")
                country_data = _xmldoc.createTextNode(value)
                country_elements.appendChild(country_data)
                country_element.appendChild(country_elements)
            _topElement.appendChild(country_element)

        if ('email' in whois and not (whois['email'] is None)):
            email_element = _xmldoc.createElement("email")
            for value in whois['email']:
                email_elements = _xmldoc.createElement("email")
                email_data = _xmldoc.createTextNode(value)
                email_elements.appendChild(email_data)
                email_element.appendChild(email_elements)
            _topElement.appendChild(email_element)

        if ('phone' in whois and not (whois['phone'] is None)):
            phone_element = _xmldoc.createElement("phone")
            for value in whois['phone']:
                phone_elements = _xmldoc.createElement("phone")
                phone_data = _xmldoc.createTextNode(value)
                phone_elements.appendChild(phone_data)
                phone_element.appendChild(phone_elements)
            _topElement.appendChild(phone_element)

        if ('fax' in whois and not (whois['fax'] is None)):
            fax_element = _xmldoc.createElement("fax")
            for value in whois['fax']:
                fax_elements = _xmldoc.createElement("fax")
                fax_data = _xmldoc.createTextNode(value)
                fax_elements.appendChild(fax_data)
                fax_element.appendChild(fax_elements)
            _topElement.appendChild(fax_element)

        if ('raw' in whois and not (whois['raw'] is None)):
            for value in whois['raw']:
                raw_element = _xmldoc.createElement("raw")
                raw_data = _xmldoc.createTextNode(value)
                raw_element.appendChild(raw_data)
            _topElement.appendChild(raw_element)

        xmlfile = open(report, "w", 0)
        _xmldoc.appendChild(_topElement)
        _xmldoc.writexml(xmlfile, addindent=" " * 4, newl="\n", encoding="UTF-8")
        xmlfile.close()

        self.wass.WassLogging.info("############### Whois WASS XML Done ###############")

    def ConvertArachniXML(self):
        '''
        Convert Arachni XML file to DEF XML
        '''
        self.wass.WassLogging.info("############### ConvertArachniXML Starting ###############")
        dictArachni = {'Title': None,
                        'generated_on': None,
                        'version': None,
                        'revision': None,
                        'start_datetime': None,
                        'finish_datetime': None,
                        'delta_time': None,
                        'url': None,
                        'user_agent': None,
                        'vulnerabilities': []
                        }

        dictVulnerability = {'url': None,
                        'elem': None,
                        'method': None,
                        'name': None,
                        'description': None,
                        'cwe': None,
                        'cwe_url': None,
                        'severity': None,
                        'remedy_guidance': None,
                        'mod_name': None,
                        'cvssv2': None,
                        'internal_modname': None,
                        '_hash': None,
                        'digest': None,
                        'unique_id': None,
                        'tags': [],
                        'references': [],
                        'variations': [],
                        }

        arachnixmldoc = etree.parse(self.wass.ArachniXMLReport)

        self.wass.WassLogging.info("############### ConvertArachniXML Done ###############")
