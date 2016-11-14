# pyAirWatch

This is a python library for communicating with VMWare AirWatch via their REST
API.

## Install

Install by cloning the repo and run `setup.py`.

```bash
$ python setup.py install --user
```

## Usage

First of all you have to create an API user in the AirWatch Console. Do this by
going into "Groups & Settings" > "All settings" > "System" > "Advanced" > "API" >
"REST API". This screen will also let you choose between authentication types.
This library uses the HTTP Basic authentication.

You can do get requests to an arbitrary URL or use one of the built-in
functions.

The AirWatch API has a lot of endpoints and it will take some time before the
library has functions for each.

```python
from airwatch import AirWatch
aw = AirWatch('api-username', 'api-password', 'api-code', 'hostname')

# To get information about a device
aw.get_device_by_serialnumber('serial_number')
aw.get_device_by_macaddress('mac_address')
aw.get_device_by_udid('udid')

# Get installed profiles
aw.get_profiles_by_serialnumber('serial_number')
aw.get_profiles_by_macaddress('mac_address')
aw.get_profiles_by_udid('udid')

# Get to arbitrary relative url
aw.get('mdm/devices/serialnumber/__SERIAL_NUMBER__/content')
```

Feel free to contribute! The idea is to make it as simple as possible to use
their API.
