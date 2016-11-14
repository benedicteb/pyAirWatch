#!/usr/bin/env python
import requests

from requests.auth import HTTPBasicAuth

__version__ = '0.0.1'

class AirWatch(object):
    def __init__(self, username, password, apicode, host):
        self.uribase = 'https://%s/api/' % host
        self.auth = HTTPBasicAuth(username, password)

        self.headers = {
            'User-Agent': '/'.join(['pyAirWatch', __version__]),
            'aw-tenant-code': apicode,
            'accept': 'application/json'
        }

    def get(self, relative_url):
        url = urljoin(self.uribase, relative_url)

        response = requests.get(url, auth=self.auth, headers=self.headers)
        verify_response(response)

        return response.json()

    def get_device_by_serialnumber(self, serial_number):
        return self.get('mdm/devices/serialnumber/%s' % serial_number)

    def get_device_by_macaddress(self, mac_address):
        return self.get('mdm/devices/macaddress/%s' % mac_address)

    def get_device_by_udid(self, udid):
        return self.get('mdm/devices/UDID/%s' % udid)

    def get_profiles_by_serialnumber(self, serial_number):
        return self.get('mdm/devices/serialnumber/%s/profiles' % serial_number)

    def get_profiles_by_macaddress(self, mac_address):
        return self.get('mdm/devices/macaddress/%s/profiles' % mac_address)

    def get_profiles_by_udid(self, udid):
        return self.get('mdm/devices/udid/%s/profiles' % udid)

    def get_organization_group(self, id):
        return self.get('system/groups/%s' % id)

def verify_response(response):
    if str(response.status_code).startswith('2'):
        return

    errormsg = str(response.status_code) + ' %s' % response.reason
    raise Exception(errormsg)

def urljoin(*args):
    uri = ''

    for arg in args:
        if not uri.endswith('/') and uri != '':
            uri += '/'

        uri += str(arg)

    return uri
