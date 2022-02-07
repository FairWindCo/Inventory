import os

import winrm
from dotenv import load_dotenv
from winrm.exceptions import WinRMError, WinRMTransportError, AuthenticationError, WinRMOperationTimeoutError, \
    BasicAuthDisabledError, InvalidCredentialsError

load_dotenv()

HOST_NAME = os.getenv('HOST_NAME')
USER_NAME = os.getenv('USER_NAME')
USER_PASS = os.getenv('USER_PASS')

if __name__ == '__main__':
    try:
        print(HOST_NAME, USER_NAME, USER_PASS)
        s = winrm.Session(HOST_NAME, auth=(USER_NAME, USER_PASS), transport='ntlm')
        r = s.run_cmd('ipconfig', ['/all'])
        if r.status_code == 0:
            print(r.std_out)
        r = s.run_ps('[System.Environment]::OSVersion.Version')
        if r.status_code == 0:
            print(r.std_out)
    except AuthenticationError | BasicAuthDisabledError | InvalidCredentialsError as e:
        print('AuthenticationError: ' + e)
    except WinRMError | WinRMTransportError | WinRMOperationTimeoutError as e:
        print(e)
