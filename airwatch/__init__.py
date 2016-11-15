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

    def post(self, relative_url, data=None, **kwargs):
        url = urljoin(self.uribase, relative_url)

        if data:
            response = requests.post(url, auth=self.auth, headers=self.headers,
                json=data, **kwargs)
        else:
            response = requests.post(url, auth=self.auth, headers=self.headers,
                **kwargs)

        verify_response(response)

    def delete(self, relative_url, **kwargs):
        url = urljoin(self.uribase, relative_url)

        response = requests.delete(url, auth=self.auth, headers=self.headers,
            **kwargs)

        verify_response(response)

    def get_device_information(self, id, search_by='serialnumber'):
        choices = [
            'serialnumber',
            'macaddress',
            'udid',
            'imeinumber',
            'easid'
        ]

        verify_choices(search_by, choices)

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

        verify_choices(search_by, choices)

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
        """
        Searches for all profiles applicable using the query information provided.
        """
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

        verify_params(params, choices)

        return self.get('mdm/profiles/search', params=params)

    def get_profile_details(self, profile_id, version=None):
        """
        Gets device profile details identified by the profile Id.
        """
        url = urljoin('mdm/profiles/', profile_id)

        if version:
            url = urljoin(version, url)

        return self.get(url)

    def activate_device_profile(self, profile_id):
        """
        Activates a device profile identified by the profile Id.
        """
        url = urljoin('mdm/profiles/', profile_id, 'activate')
        self.post(url)

    def deactivate_device_profile(self, profile_id):
        """
        Deactivates a device profile identified by the profile Id.
        """
        url = urljoin('mdm/profiles/', profile_id, 'deactivate')
        self.post(url)

    def delete_device_profile(self, profile_id):
        """
        Deletes the device profile identified by the numeric profile Id.
        """
        url = urljoin('mdm/profiles/', profile_id)
        self.delete(url)

    def remove_device_profile(self, profile_id, serial_number=None, udid=None,
                                macaddress=None, device_id=None):
        """
        Removes the profile from the device identified by the device parameter
        provided.

        Usage:
        >>> aw.remove_device_profile(1, serial_number='serial_number')
        >>> aw.remove_device_profile(1, udid='udid')
        >>> aw.remove_device_profile(1, macaddress='macaddress')
        >>> aw.remove_device_profile(1, device_id=121)
        """

        payload = {}

        if serial_number:
            payload['SerialNumber'] = serial_number
        elif udid:
            payload['Udid'] = udid
        elif macaddress:
            payload['MacAddress'] = macaddress
        elif device_id:
            assert isinstance(device_id, (int, ))
            payload['DeviceId'] = device_id

        url = urljoin('mdm/profiles/', profile_id, 'remove')
        self.post(url, data=payload)

    def update_apple_device_profile(self, profile_id, data):
        """
        Updates an Apple device profile identified by its numeric ID.
        """
        url = 'mdm/profiles/platforms/apple/update'

        assert isinstance(profile_id, (int, ))

        if 'General' in data.keys():
            data['General']['ProfileId'] = profile_id
        else:
            data['General'] = {
                'ProfileId': profile_id
            }

        self.post(url, data=data)

    def get_organization_group(self, id):
        return self.get('system/groups/%s' % id)

def verify_choices(search_by, choices):
    if not search_by in choices:
        raise Exception('Not able to search by \'%s\', possible choices: %s'\
            % (search_by, ','.join(choices)))

def verify_params(params, choices):
    if any([p not in choices for p in params.keys()]):
        raise Exception('Bad parameter given')

def verify_response(response):
    if str(response.status_code).startswith('2'):
        return

    errormsg = '%d %s' % (response.status_code, response.reason)

    try:
        response_json = response.json()
    except:
        raise Exception(errormsg)

    if 'Message' in response_json.keys():
        errormsg += ': %s' % response_json['Message']

    raise Exception(errormsg)

def urljoin(*args):
    uri = ''

    for arg in args:
        if not uri.endswith('/') and uri != '':
            uri += '/'

        uri += str(arg)

    return uri
