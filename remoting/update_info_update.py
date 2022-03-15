from .executor import run_commandline_args


def update_update_date(host, user_name, password, debug=False):
    import logging
    from remoting.get_system_version import connect, get_update_dates
    if host:
        if debug:
            print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        if s:
            search_date, install_date = get_update_dates(s)
            if install_date:
                host.os_update_search = search_date
                host.os_last_update = install_date
                host.save()
        else:
            logging.warning(f"D`ONT CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


if __name__ == '__main__':
    run_commandline_args(update_update_date, name='Update Server Roles')
