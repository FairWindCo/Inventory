import datetime

from remoting.django_execute import execute_in_django


def update_future_info(host, user_name, password, futures_manager):
    import logging
    from remoting.get_system_version import connect
    from remoting.get_software import get_server_installed_futures
    from logview.models import ServerModificationLog

    if host:
        print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        installed_roles = set(host.futures.all())
        if s:
            for future_name, description in get_server_installed_futures(s):
                future = futures_manager.get_value(future_name, description=description)
                if future:
                    if future not in host.futures.all():
                        host.futures.add(future)
                        host.save()
                    installed_roles.remove(future)
            for future in installed_roles:
                ServerModificationLog(server=host,
                                      description=f'ROLE {future.name} - removed').save()
                host.futures.remove(future)
        else:
            logging.warning(f"D`ONT CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


def all_servers_get_os_info(username, password):
    from xls.xls_reader import FutureManager
    from info.models import Server

    futures = FutureManager()
    for server in Server.objects.filter(is_online=True, win_rm_access=True).all():
        update_future_info(server, username, password, futures)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')
    USER_PASS = os.getenv('USER_PASS')
    execute_in_django(lambda: all_servers_get_os_info(USER_NAME, USER_PASS))
