import datetime

from remoting.django_execute import execute_in_django


def update_software_info(host, user_name, password, soft_manager):
    import logging
    from remoting.get_system_version import connect
    from remoting.get_software import get_installed_software
    from info.models import HostInstalledSoftware
    from logview.models import ServerModificationLog
    from django.utils.timezone import now

    if host:
        print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        installed_soft = set(host.hostinstalledsoftware_set.all())
        if s:
            for sof_name, install_date, version in get_installed_software(s):
                print(sof_name, install_date, version)
                soft = soft_manager.get_value(sof_name)
                if soft:
                    try:
                        host_installed = HostInstalledSoftware.objects.get(server=host, soft=soft)
                        try:
                            installed_soft.remove(host_installed)
                        except KeyError:
                            ServerModificationLog(server=host, description=f'New soft {soft.name}').save()
                        if host_installed.version != version:
                            log = ServerModificationLog(server=host,
                                                        description=f'UPDATED {soft.name} from {host_installed.version} to {version}')
                            log.save()
                            host_installed.version = version
                        host_installed.last_check_date = now()
                        host_installed.save()
                    except HostInstalledSoftware.DoesNotExist:
                        host_installed = HostInstalledSoftware(server=host, soft=soft, version=version,
                                                               installation_date=install_date)
                        host_installed.last_check_date = now()
                        host_installed.save()
            for soft in installed_soft:
                log = ServerModificationLog(server=host,
                                            description=f'UNINSTALL {soft.soft.name}')
                log.save()
        else:
            logging.warning(f"D`ONT CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


def all_servers_get_os_info(username, password):
    from xls.xls_reader import SoftManager
    from info.models import Server

    soft = SoftManager()
    for server in Server.objects.filter(is_online=True, win_rm_access=True).order_by('name').all()[24:]:
        update_software_info(server, username, password, soft)
    # server = Server.objects.get(name='BT01')
    # update_software_info(server, username, password, soft)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')
    USER_PASS = os.getenv('USER_PASS')
    execute_in_django(lambda: all_servers_get_os_info(USER_NAME, USER_PASS))
