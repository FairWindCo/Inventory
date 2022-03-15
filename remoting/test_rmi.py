import os

from dotenv import load_dotenv


from get_system_version import connect, get_system_os_info, get_system_os_name

load_dotenv()

HOST_NAME = os.getenv('HOST_NAME')
USER_NAME = os.getenv('USER_NAME')
USER_PASS = os.getenv('USER_PASS')

if __name__ == '__main__':
    session = connect(HOST_NAME, USER_NAME, USER_PASS)
    print(get_system_os_info(session))
    print(get_system_os_name(session))
