import argparse
import concurrent.futures

from .django_execute import execute_in_django


def run_on_servers_one(username, password, server_list, command, *args, debug=False):
    for server in server_list:
        command(server, username, password, *args, debug=debug)


def run_on_servers_multi(username, password, server_list, command, *args, debug=False):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(command, server, username, password, *args, debug=debug) for server in server_list]
        concurrent.futures.wait(futures)


def get_all_server():
    from info.models import Server
    return Server.objects.filter(is_online=True).all()


def get_active_server():
    from info.models import Server
    return Server.objects.filter(is_online=True, win_rm_access=True).all()


def run(command, *args, debug=False, server_list=None, user_name=None, password=None,
        use_active_server=True,
        use_multi_threading=True):
    import os
    from dotenv import load_dotenv

    load_dotenv()
    user = user_name if user_name else os.getenv('USER_NAME')
    password = password if password else os.getenv('USER_PASS')

    if use_multi_threading:
        def exec_command():
            if server_list is None:
                servers = get_active_server() if use_active_server else get_all_server()
            else:
                servers = server_list
            run_on_servers_multi(user, password, servers, command, *args, debug=debug)
    else:
        def exec_command():
            if server_list is None:
                servers = get_active_server() if use_active_server else get_all_server()
            else:
                servers = server_list
            run_on_servers_one(user, password, servers, command, *args, debug=debug)

    execute_in_django(exec_command)


def run_commandline_args(command, *args, name='', default_active_server=True):
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument('-u', '--user', type=str, default=None, help='Имя пользователя для логина на сервер')
    parser.add_argument('-p', '--password', type=str, default=None, help='Пароль пользователя для логина на сервер')
    parser.add_argument('-s', '--servers', action='append', help='Список серверов')
    parser.add_argument('-m', '--multi_threading', action=argparse.BooleanOptionalAction, default=True,
                        help='Multi Threading')
    parser.add_argument('-a', '--only_active', action=argparse.BooleanOptionalAction, default=default_active_server,
                        help='Use default as active servers')
    parser.add_argument('-d', '--debug', action=argparse.BooleanOptionalAction, default=False,
                        help='verbose output')
    parser.add_argument('-c', '--command', type=str, default=None, help='Имя команды')

    arguments = parser.parse_args()
    if arguments.command:
        command, *args = command(arguments.command)

    run(command,
        *args,
        debug=arguments.debug,
        server_list=arguments.servers,
        user_name=arguments.user,
        password=arguments.password,
        use_active_server=arguments.only_active,
        use_multi_threading=arguments.multi_threading)
