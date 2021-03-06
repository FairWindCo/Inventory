from .update_installed_soft import update_software_info
from .update_os_versions import update_general_host_info
from .update_installed_roles import update_future_info
from .update_remote_access import update_remote_access
from .update_info_update import update_update_date


def command_getter(name):
    if name == 'update_os':
        from xls.xls_reader import OSManager
        os_manager = OSManager()
        return update_general_host_info, os_manager
    elif name == 'update_roles':
        from xls.xls_reader import FutureManager
        futures = FutureManager()
        return update_future_info, futures
    elif name == 'update_soft':
        from xls.xls_reader import SoftManager
        soft = SoftManager()
        return update_software_info, soft
    elif name == 'check_update':
        return update_update_date,
    elif name == 'check_remote':
        return update_remote_access,
    # elif name == 'update_hardware':
    else:
        def echo(host, user_name, password, *args, debug=True):
            print(host, user_name, password, *args, debug)

        return echo,
