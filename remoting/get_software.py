import datetime
import re

from remoting.data_type_convertion import convert_to_lines, chunks, LOCAL_TZ
from remoting.win_remote import *


def get_installed_software(session):
    data = execute_ps(session,
                      '(Get-WmiObject -Class Win32_Product |  Format-List Name, InstallDate, Version)',
                      codepage='cp866')
    if data:
        lines = convert_to_lines(data)
        # for line in chunks(lines, 3):
        #     name, date_installed_str, version = line
        #     _, *other = name.split(':')
        #     name = ' '.join(other).strip()
        #
        #     if version.find(':') > 0:
        #         version = version.split(':')[1].strip()
        #         name = re.sub(f'[-\\s(]*{version}[\\s)]*', '', name)
        #     else:
        #         version = ''
        #     date_installed = None
        #     if date_installed_str.find(':') > 0:
        #         date_installed_str = date_installed_str.split(':')[1].strip()
        #         if date_installed_str:
        #             try:
        #                 date_installed = datetime.datetime(int(date_installed_str[:4]),
        #                                                    int(date_installed_str[4:6]),
        #                                                    int(date_installed_str[6:]),
        #                                                    tzinfo=LOCAL_TZ)
        #             except ValueError:
        #                 print(date_installed_str)
        #                 pass
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
    data = execute_ps(session,
                      'Get-WindowsFeature | Where-Object {$_. installstate -eq "installed"} | Format-List Name',
                      codepage='cp866')
    if data:
        lines = convert_to_lines(data)
        for line in lines:
            name = line.split(':')[1].strip()
            yield name, ''
