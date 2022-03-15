from executor import run_commandline_args


def update_os_info_full(host, user_name, password, debug=False):
    import logging
    from get_system_version import connect, get_system_os_info_full
    if host:
        if debug:
            print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        if s:
            version = get_system_os_info_full(s)
            host.os_version = version
            host.save()
        else:
            logging.warning(f"D`ONT CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


if __name__ == '__main__':
    run_commandline_args(update_os_info_full, name='Update os infos')
