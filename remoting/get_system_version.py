import datetime
import re

from urllib3.exceptions import MaxRetryError, NewConnectionError
from winrm.exceptions import WinRMError, WinRMTransportError, WinRMOperationTimeoutError, AuthenticationError, \
    BasicAuthDisabledError, InvalidCredentialsError
import logging
import winrm

now = datetime.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo


def connect(host, user, password):
    if host and user:
        try:
            return winrm.Session(host, auth=(user, password), transport='ntlm')
        except BasicAuthDisabledError as e:
            logging.error(f"REMOTING ERROR: {e}")
        except InvalidCredentialsError as e:
            logging.error(f"REMOTING ERROR: {e}")
        except AuthenticationError as e:
            logging.error(f"REMOTING ERROR: {e}")
        except NewConnectionError as e:
            logging.error(f"cod n`t connect")
        except ConnectionRefusedError as e:
            logging.error(f"Connection Refused ERROR: {e}")
        except ConnectionError as e:
            logging.error(f"Connection ERROR: {e}")
        except Exception as e:
            logging.error(f"ERROR: {e}")
    else:
        logging.error(f"NO PASSWORD for {host}")


def execute_ps(session, command):
    if session is None:
        return None
    try:
        res = session.run_ps(command)
        if res.status_code != 0:
            logging.warning(f"WARNING REMOTING ERROR: {res.status_code}")
            return None
        else:
            return res.std_out.decode()
    except WinRMError as e:
        logging.error(f"REMOTING ERROR: {e}")
    except WinRMTransportError as e:
        logging.error(f"REMOTING TRANSPORT ERROR: {e}")
    except WinRMOperationTimeoutError as e:
        logging.error(f"REMOTING TIMEOUT ERROR: {e}")
    except NewConnectionError as e:
        logging.error(f"cod n`t connect")
    except ConnectionRefusedError as e:
        logging.error(f"Connection Refused ERROR: {e}")
    except ConnectionError as e:
        logging.error(f"Connection ERROR: {e}")
    except Exception as e:
        logging.error(f"ERROR: {e}")


def execute_cmd(session, command):
    if session is None:
        return None
    try:
        res = session.run_cmd(command)
        if res.status_code != 0:
            logging.warning(f"WARNING REMOTING ERROR: {res.status_code}")
            return None
        else:
            return res.std_out.decode()
    except WinRMError as e:
        logging.error(f"REMOTING ERROR: {e}")
    except WinRMTransportError as e:
        logging.error(f"REMOTING TRANSPORT ERROR: {e}")
    except WinRMOperationTimeoutError as e:
        logging.error(f"REMOTING TIMEOUT ERROR: {e}")
    except ConnectionRefusedError as e:
        logging.error(f"Connection Refused ERROR: {e}")
    except ConnectionError as e:
        logging.error(f"Connection ERROR: {e}")
    except NewConnectionError as e:
        logging.error(f"cod n`t connect")
    except Exception as e:
        logging.error(f"{e}")


LINE_BREAK = re.compile(r'([\r\n]|\r|\n])')
LINE_TO_DOTS = re.compile(r'[\s]+')


def convert_to_lines(text):
    lines = LINE_BREAK.split(text)
    return [line.strip() for line in lines if line not in ['', '\r', '\n']]


def get_system_os_info(session):
    data = execute_ps(session, '[System.Environment]::OSVersion.Version')
    if data:
        return LINE_TO_DOTS.sub('.', convert_to_lines(data)[2])


def get_system_os_name(session):
    data = execute_ps(session, '(Get-WmiObject Win32_OperatingSystem).Caption')
    if data:
        return convert_to_lines(data)[0]


def convert_date(string, formats=None, with_timezone=True):
    if formats is None:
        formats = (
            '%d.%m.%Y',
            '%m/%d/%Y',
            '%d/%m/%Y'
        )
    for _format in formats:
        try:
            dt = datetime.datetime.strptime(string, _format)
            return dt.astimezone(local_tz) if with_timezone else dt
        except ValueError:
            pass
    print('DON`T CONVERT ', string)


def convert_datetime(string, formats=None, with_timezone=True):
    if formats is None:
        formats = (
            '%d.%m.%Y %H:%M:%S',
            '%m/%d/%Y %I:%M:%S %p',
        )
    return convert_date(string, formats, with_timezone)


def get_last_update(session):
    data = execute_ps(session, '(Get-HotFix | select InstalledOn,HotFixId | sort-object InstalledOn)[-1]')
    if data:
        response = convert_to_lines(data)[2].split(' ')
        dt = convert_date(response[0])
        kb = response[-1]
        print(f'Updated {dt} as {response[0]} {kb}')
        return dt, kb
    return None, None


def get_installed_date(session):
    data = execute_ps(session, 'gcim Win32_OperatingSystem | select InstallDate')
    if data:
        response = convert_to_lines(data)[2]
        dt = convert_datetime(response)
        print(f'Installed {dt} as {data}')
        return dt
