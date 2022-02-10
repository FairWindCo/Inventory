from remoting.django_execute import execute_in_django


def update_update_date(host, user_name, password):
    import logging
    from remoting.get_system_version import connect, get_update_dates
    if host:
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


def all_servers_check(username, password):
    from info.models import Server

    for server in Server.objects.filter(is_online=True, win_rm_access=True).all():
        update_update_date(server, username, password)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')
    USER_PASS = os.getenv('USER_PASS')
    execute_in_django(lambda: all_servers_check(USER_NAME, USER_PASS))
