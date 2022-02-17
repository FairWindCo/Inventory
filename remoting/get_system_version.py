import re

from remoting.data_type_convertion import UTC_TZ, convert_date, LINE_TO_DOTS, convert_date_json
from remoting.win_remote import *

KB_EXTRACT = re.compile(r'(KB[0-9]{7,10})')


def get_system_os_info(session):
    data = execute_ps(session, '[System.Environment]::OSVersion.Version')
    if data:
        return LINE_TO_DOTS.sub('.', convert_to_lines(data)[2])


def get_system_os_info_full(session):
    data = execute_ps(session, '(Get-ItemProperty -Path c:\windows\system32\hal.dll).VersionInfo.FileVersion')
    if data:
        return convert_to_lines(data)[0].split(' ')[0]


def get_system_os_name(session):
    data = execute_ps(session, '(Get-WmiObject Win32_OperatingSystem).Caption')
    if data:
        return convert_to_lines(data)[0]


def get_last_update_simple(session):
    data = execute_ps(session, '(Get-HotFix | select InstalledOn,HotFixId | sort-object InstalledOn)[-1]')
    if data:
        response = convert_to_lines(data)[2].split(' ')
        dt = convert_date(response[0], tz=UTC_TZ)
        kb = response[-1]
        print(f'Updated {dt} as {response[0]} {kb}')
        return dt, kb
    return None, None


def get_last_update(session):
    data = execute_ps(session,
                      '$m=(Get-HotFix | select InstalledOn,HotFixId | sort-object InstalledOn)[-1]; if($m) {$m[-1]| ConvertTo-Json}')
    if data:
        update = json.loads(data)
        if 'Title' in update:
            kb = update['HotFixId']
            dt = convert_date_json(update['InstalledOn']['value'])
            return dt, kb
    return None, None


def get_updates(session):
    data = execute_ps(session,
                      '((New-Object -ComObject Microsoft.Update.Session).CreateupdateSearcher())'
                      '.Search("IsAssigned=1 and IsHidden=0 and IsInstalled=1 and Type=\'Software\'").Updates '
                      '| select title, LastDeploymentChangeTime | sort-object LastDeploymentChangeTime)[-1]')
    if data:
        response = convert_to_lines(data)[2].split(' ')
        dt = convert_date(response[0], tz=UTC_TZ)
        kb = response[-1]
        print(f'Updated {dt} as {response[0]} {kb}')
        return dt, kb
    return None, None


def get_last_update_alt(session):
    data = execute_ps(session, '''$m=((New-Object -ComObject Microsoft.Update.Session).CreateupdateSearcher())\
.Search("IsAssigned=1 and IsHidden=0 and IsInstalled=1 and Type='Software'").Updates \
| select title, LastDeploymentChangeTime | sort-object LastDeploymentChangeTime; if($m) {$m[-1]| ConvertTo-Json}''')
    if data:
        update = json.loads(data)
        if 'Title' in update:
            result = KB_EXTRACT.search(update['Title'])
            kb = result.group(1) if result else ''
            dt = convert_date_json(update['LastDeploymentChangeTime'])
            return dt, kb

    else:
        return get_last_update(session)


def has_update_assigned(session):
    data = execute_ps(session,
                      '((New-Object -ComObject Microsoft.Update.Session).CreateupdateSearcher())'
                      '.Search("IsAssigned=1 and IsHidden=0 and IsInstalled=0 and Type=\'Software\'").Updates '
                      '| select title')
    if data:
        response = convert_to_lines(data)[2].split(' ')
        dt = convert_date(response[0], tz=UTC_TZ)
        kb = response[-1]
        print(f'Updated {dt} as {response[0]} {kb}')
        return dt, kb
    return None, None


def get_installed_date(session):
    data = execute_ps(session, 'gcim Win32_OperatingSystem | select InstallDate| ConvertTo-Json')
    if data:
        installed = json.loads(data)
        if 'InstallDate' in installed:
            dt = convert_date_json(installed['InstallDate'])
            return dt


def get_update_dates(session):
    update_info = powershell_json(session,
                                  '(New-Object -ComObject Microsoft.Update.AutoUpdate).Results | ConvertTo-Json')
    if update_info:
        search_date, install_date = None, None
        if 'LastSearchSuccessDate' in update_info:
            search_date = convert_date_json(update_info['LastSearchSuccessDate'])
        if 'LastInstallationSuccessDate' in update_info:
            install_date = convert_date_json(update_info['LastInstallationSuccessDate'])
        return search_date, install_date
    return None, None
