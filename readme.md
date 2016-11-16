# pyAirWatch

This is a python library for communicating with VMWare AirWatch via their REST
API.

Their API has many endpoints and not all of them are implemented with functions.
However the library has a `get`, `post` and `delete`-functions that you can feed
arbitrary URL's.

I've tried to document what data you can send when. However the structure of the
data you get back and how the data you send for example in POST-requests is not
documented here. You should instead consult your AirWatch REST API guide.

The URL's might also be a bit different based on which version of AirWatch
you're running. This library is tested with version 8.4. If it doesn't work as
is try prepending `v1` or `v2` to the URL's you use.

## Install

Install by cloning the repo and run `setup.py`.

```bash
$ python setup.py install --user
```

## Add an API user

You have to create a specific API user in order to use the API. Do this by going
into "Groups & Settings" > "All settings" > "System" > "Advanced" > "API" >
"REST API". This screen will also let you choose between authentication types.
This library uses the HTTP Basic authentication.

## Usage

To initialize do the following.

```python
from airwatch import AirWatch
aw = AirWatch('api-username', 'api-password', 'api-code', 'hostname')
```

Hostname is without "https" or something like that. For example:

```python
aw = AirWatch('apiuser', 'mypassword', '123', 'airwatchconsole.mydomain.com')
```

Here are some examples on what you can do with the built-in functions.

```python
aw.get(relative_url, params=params)
aw.post(relative_url, data=data)
aw.delete(relative_url)

# Information about a device
#
# You can search by 'serialnumber', 'macaddress', 'udid', 'imeinumber' or
# 'easid' by changing the search_by parameter. Serial number is default.
aw.get_device_information('search-parameter', search_by='serialnumber'):

# Get a device's profiles
#
# You can search by 'serialnumber', 'macaddress', 'udid' or 'imeinumber' in the
# same way as for device_information. search_by, page and page_size are
# optional.
aw.get_device_profiles('search-parameter', search_by, page, page_size)
aw.get_device_profiles('my-serial-number')

# Search for profiles
#
# Available parameters are
# - type,
# - profilename,
# - organizationgroupid,
# - platform,
# - status,
# - ownership,
# - orderby,
# - sortorder,
# - pagesize,
# - page
aw.search_for_profile(param1=param1, param2=param2)

# Get details about a profile
aw.get_profile(profile_id)

# Activate or deactivate a profile
aw.activate_device_profile(profile_id)
aw.deactivate_device_profile(profile_id)

# Removes the profile from the device identified by the device parameter
# provided.
#
# You can only use one of the parameters for at a time for specifying the
# device.
aw.remove_device_profile(profile_id, serial_number='serial_number')
aw.remove_device_profile(profile_id, udid='udid')
aw.remove_device_profile(profile_id, macaddress='macaddress')
aw.remove_device_profile(profile_id, device_id=121)

# Alter a device profile's settings.
#
# The data dictionary you send here has to have a certain structure. So check
# out the API reference. You don't need to supply the "General"-key.
aw.update_apple_device_profile(profile_id, data)

# Get info about an organization group
aw.get_organization_group(id)

# Search for a product
#
# Available parameters are
# - name,
# - organizationgroupid,
# - managedbyorganizationgroupid,
# - platform,
# - smartgroupid,
# - orderby,
# - sortorder,
# - pagesize,
# - page
aw.search_for_product(param1=param1, param2=param2)

# Get details about a product
aw.get_product(product_id)

# Activate or deactivate a product
aw.activate_product(product_id)
aw.deactivate_product(product_id)

# Alter a product's metadata
#
# Check out the API reference for the structure of the dictionary data.
aw.update_product(product_id, data)

# Search for files or actions
#
# Available parameters are
# - organizationgroupid,
# - platform,
# - lastmodifiedon,
# - lastmodifiedtill,
# - pagesize,
# - page
aw.search_files_or_actions(param1=param1, param2=param2)
```
