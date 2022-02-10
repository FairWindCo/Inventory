import datetime

from remoting.django_execute import execute_in_django


def update_software_info(host, user_name, password, soft_manager):
    import logging
    from remoting.get_system_version import connect
    from remoting.get_software import get_installed_software
    from info.models import HostInstalledSoftware
    from django.utils.timezone import now

    if host:
        print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        if s:
            for sof_name, install_date, version in get_installed_software(s):
                soft = soft_manager.get_value(sof_name)
                if soft:
                    try:
                        host_installed = HostInstalledSoftware.objects.get(server=host, soft=soft)
                        if host_installed.version != version:
                            # TODO: write to event that software was updated
                            host_installed.version = version
                        host_installed.last_check_date = now()
                        host_installed.save()
                    except HostInstalledSoftware.DoesNotExist:
                        host_installed = HostInstalledSoftware(server=host, soft=soft, version=version,
                                                               installation_date=install_date)
                        host_installed.last_check_date = now()
                        host_installed.save()
        else:
            logging.warning(f"D`ONT CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


def all_servers_get_os_info(username, password):
    from xls.xls_reader import SoftManager
    from info.models import Server

    soft = SoftManager()
    for server in Server.objects.filter(is_online=True, win_rm_access=True).all():
        update_software_info(server, username, password, soft)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')
    USER_PASS = os.getenv('USER_PASS')
    execute_in_django(lambda: all_servers_get_os_info(USER_NAME, USER_PASS))
