from remoting import run_commandline_args


def update_future_info(host, user_name, password, futures_manager, debug=False):
    import logging
    from remoting.get_system_version import connect
    from remoting.get_software import get_server_installed_futures
    from logview.models import ServerModificationLog

    if host:
        if debug:
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


if __name__ == '__main__':
    from xls.xls_reader import FutureManager

    futures = FutureManager()

    run_commandline_args(update_future_info, futures, name='Update Server Roles')
