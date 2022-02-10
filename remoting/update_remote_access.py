from remoting.django_execute import execute_in_django


def update_remote_access(host, user_name, password):
    import logging
    from remoting.get_system_version import connect, get_system_os_name
    if host:
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


def all_servers_check(username, password):
    from info.models import Server

    for server in Server.objects.filter(is_online=True).all():
        update_remote_access(server, username, password)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')
    USER_PASS = os.getenv('USER_PASS')
    execute_in_django(lambda: all_servers_check(USER_NAME, USER_PASS))
