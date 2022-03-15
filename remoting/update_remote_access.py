from executor import run_commandline_args


def update_remote_access(host, user_name, password, debug=False):
    import logging
    from get_system_version import connect, get_system_os_name
    if host:
        if debug:
            print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        if s:
            win_name = get_system_os_name(s)
            remote_access = True if win_name else False
            if host.win_rm_access != remote_access:
                host.win_rm_access = remote_access
                host.save()
        else:
            logging.warning(f"D`ONT CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


if __name__ == '__main__':
    run_commandline_args(update_remote_access, name='Test Remote Access', default_active_server=False)
