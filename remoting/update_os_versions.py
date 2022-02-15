from remoting.django_execute import execute_in_django
from remoting.get_system_version import get_update_dates


def update_general_host_info(host, user_name, password, os_manager):
    import logging
    from remoting.get_system_version import connect, get_system_os_info, get_last_update, get_installed_date, \
        get_system_os_name
    if host:
        print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        if s:
            need_update = False
            if not host.os_name or not host.os_version:
                win_name = get_system_os_name(s)
                if win_name:
                    win = os_manager.get_value(win_name)
                    if host.os_name != win:
                        host.os_name = win
                        need_update = True
                    if not host.os_version:
                        host.os_version = get_system_os_info(s)
                        need_update = True
            if host.os_installed is None:
                host.os_installed = get_installed_date(s)
                need_update = True
            search_date, install_date = get_update_dates(s)
            if search_date and (host.os_update_search is None or host.os_update_search < search_date):
                host.os_update_search = search_date
                need_update = True
            if install_date and (host.os_last_update is None or host.os_last_update < install_date):
                host.os_last_update = install_date
                _, kb_id = get_last_update(s)
                print(kb_id)
                if kb_id:
                    host.last_update_id = kb_id
                need_update = True

            if need_update:
                host.save()
        else:
            logging.warning(f"DON`T CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


def all_servers_get_os_info(username, password):
    from xls.xls_reader import OSManager
    from info.models import Server

    os_manager = OSManager()
    for server in Server.objects.filter(is_online=True, win_rm_access=True).all():
        update_general_host_info(server, username, password, os_manager)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')
    USER_PASS = os.getenv('USER_PASS')
    execute_in_django(lambda: all_servers_get_os_info(USER_NAME, USER_PASS))
