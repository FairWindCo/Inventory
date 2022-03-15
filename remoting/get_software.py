import datetime
import re

from .data_type_convertion import LOCAL_TZ
from .win_remote import *


def get_installed_software(session):
    lines = powershell(session, '(Get-WmiObject -Class Win32_Product |  Format-List Name, InstallDate, Version)')
    name = None
    date_installed = None
    version = None
    for line in lines:
        if line.startswith('Name'):
            if name:
                yield name, date_installed, version
                date_installed = None
                version = None
            _, *other = line.split(':')
            name = ' '.join(other).strip()
        elif line.startswith('InstallDate'):
            if line.find(':') > 0:
                date_installed_str = line.split(':')[1].strip()
                if date_installed_str:
                    try:
                        date_installed = datetime.datetime(int(date_installed_str[:4]),
                                                           int(date_installed_str[4:6]),
                                                           int(date_installed_str[6:]),
                                                           tzinfo=LOCAL_TZ)
                    except ValueError:
                        print(date_installed_str)
                        pass
        elif line.startswith('Version'):
            if line.find(':') > 0:
                version = line.split(':')[1].strip()
                name = re.sub(f'[-\\s(]*{version}[\\s)]*', '', name)
                yield name, date_installed, version
                name = None
                date_installed = None
                version = None
    if name:
        yield name, date_installed, version


def get_server_installed_futures(session):
    lines = powershell(session,
                       'Get-WindowsFeature | Where-Object {$_. installstate -eq "installed"} | Format-List Name')
    for line in lines:
        name = line.split(':')[1].strip()
        yield name, ''
