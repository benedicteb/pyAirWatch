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

    def get(self, relative_url, **kwargs):
        url = urljoin(self.uribase, relative_url)

        response = requests.get(url, auth=self.auth, headers=self.headers, **kwargs)
        verify_response(response)

        return response.json()

    def get_device_information(self, id, search_by='serialnumber'):
        choices = [
            'serialnumber',
            'macaddress',
            'udid',
            'imeinumber',
            'easid'
        ]

        self._verify_choices(search_by, choices)

        params = {
            'id': id,
            'searchby': search_by
        }

        return self.get('mdm/devices', params=params)

    def get_device_profiles(self, id, search_by='serialnumber', page=None, page_size=None):
        choices = [
            'serialnumber',
            'macaddress',
            'udid',
            'imeinumber'
        ]

        self._verify_choices(search_by, choices)

        params = {
            'id': id,
            'searchby': search_by
        }

        if page_size:
            params['pagesize'] = page_size

        if page:
            params['page'] = page

        return self.get('mdm/devices/profiles', params=params)

    def get_profile(self, **params):
        choices = [
            'type',
            'profilename',
            'organizationgroupid',
            'platform',
            'status',
            'ownership',
            'orderby',
            'sortorder',
            'pagesize',
            'page'
        ]

        self._verify_params(params, choices)

        return self.get('mdm/profiles/search', params=params)

    def get_profile_details(self, profile_id):
        return self.get(urljoin('mdm/profiles/', profile_id))

    def get_organization_group(self, id):
        return self.get('system/groups/%s' % id)

    def _verify_choices(self, search_by, choices):
        if not search_by in choices:
            raise Exception('Not able to search by \'%s\', possible choices: %s'\
                % (search_by, ','.join(choices)))

    def _verify_params(self, params, choices):
        if any([p not in choices for p in params.keys()]):
            raise Exception('Bad parameter given')

def verify_response(response):
    try:
        response.json()
    except Exception:
        raise Exception('Unable to parse response as json')

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
