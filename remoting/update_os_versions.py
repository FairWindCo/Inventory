from remoting.executor import run_commandline_args
from remoting.get_system_version import get_update_dates


def update_general_host_info(host, user_name, password, os_manager, debug=False):
    import logging
    from get_system_version import connect, get_system_os_info_full, get_last_update, get_installed_date, \
        get_system_os_name
    if host:
        if debug:
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
                        host.os_version = get_system_os_info_full(s)
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


if __name__ == '__main__':
    from xls.xls_reader import OSManager

    os_manager = OSManager()
    run_commandline_args(update_general_host_info, os_manager, name='Update Os info')
