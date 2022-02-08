import django
import os
import sys

from remoting.get_system_version import *
from xls.xls_reader import OSManager
from dotenv import load_dotenv

load_dotenv()

USER_NAME = os.getenv('USER_NAME')
USER_PASS = os.getenv('USER_PASS')

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.abspath(BASE_DIR))
    sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Inventarisation.settings'

    django.setup()
    from info.models import Server

    os = OSManager()
    for server in Server.objects.filter(is_online=True).all():
        print(server.canonical_name)
        s = connect(server.canonical_name, USER_NAME, USER_PASS)
        if s:
            modif = False
            if not server.os_name or not server.os_version:
                win_name = get_system_os_name(s)
                if win_name:
                    win = os.get_value(win_name)
                    if server.os_name != win:
                        server.os_name = win
                        modif = True
                    if not server.os_version:
                        server.os_version = get_system_os_info(s)
                        modif = True
            #if server.os_installed is None:
            server.os_installed = get_installed_date(s)
            modif = True

            update_date, kb_id = get_last_update(s)
            if update_date:
                if server.os_last_update is None or server.os_last_update < update_date:
                    server.os_last_update = update_date
                    server.last_update_id = kb_id
                    modif = True

            if modif:
                server.save()
        else:
            logging.warning(f"D`ONT CONNECT {server}")
