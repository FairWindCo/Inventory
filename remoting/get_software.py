from remoting.data_type_convertion import convert_to_lines, chunks
from remoting.win_remote import *


def get_installed_software(session):
    data = execute_ps(session,
                      '(Get-WmiObject -Class Win32_Product |  Format-List Name, InstallDate, Version)',
                      codepage='cp866')
    if data:
        lines = convert_to_lines(data)
        for line in chunks(lines, 3):
            name, date_installed_str, version = line
            _, *other = name.split(':')
            name = ' '.join(other).strip()
            version = version.split(':')[1].strip()
            date_installed_str = date_installed_str.split(':')[1].strip()
            name = re.sub(f'[-\\s(]*{version}[\\s)]*', '', name)
            date_installed = datetime.datetime(int(date_installed_str[:4]), int(date_installed_str[4:6]),
                                               int(date_installed_str[6:]))

            yield name, date_installed, version
