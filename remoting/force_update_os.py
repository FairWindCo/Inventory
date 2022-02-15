from remoting.django_execute import execute_in_django


def update_general_host_info(host, user_name, password):
    import logging
    from remoting.get_system_version import connect, get_system_os_info, get_last_update_alt
    if host:
        print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        if s:
            host.os_version = get_system_os_info(s)
            _, kb_id = get_last_update_alt(s)
            print(kb_id)
            if kb_id:
                host.last_update_id = kb_id
            host.save()
        else:
            logging.warning(f"DON`T CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


def all_servers_force_get_os_info(username, password):
    from info.models import Server

    for server in Server.objects.filter(is_online=True, win_rm_access=True).all():
        update_general_host_info(server, username, password)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')
    USER_PASS = os.getenv('USER_PASS')
    execute_in_django(lambda: all_servers_force_get_os_info(USER_NAME, USER_PASS))
