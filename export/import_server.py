import datetime
import json
import sys

from remoting import run_commandline_args


def update_server(server, obj_dict):
    from django.contrib.auth.models import User
    from dictionary.models import ServerFuture
    from dictionary.models import SoftwareCatalog
    from info.models import HostInstalledSoftware

    server.name = obj_dict['name']
    server.version = obj_dict['version']
    server.pk = obj_dict['id']
    server.is_online = obj_dict['is_online']

    server.virtual_server_name = obj_dict['virtual_server_name']
    server.os_version = obj_dict['os_version']
    server.description = obj_dict['description']
    server.has_internet_access = obj_dict['has_internet_access']
    server.has_monitoring_agent = obj_dict['has_monitoring_agent']
    server.os_last_update = datetime.datetime.strptime(obj_dict['os_last_update'], '%d.%m.%Y %H:%M:%S') if obj_dict.get(
        'os_last_update', None) else None

    server.updated_at = datetime.datetime.strptime(obj_dict['updated_at'], '%d.%m.%Y %H:%M:%S') if obj_dict.get(
        'updated_at', None) else None
    server.created_at = datetime.datetime.strptime(obj_dict['created_at'], '%d.%m.%Y %H:%M:%S') if obj_dict.get(
        'created_at', None) else None
    server.os_update_search = datetime.datetime.strptime(obj_dict['os_update_search'],
                                                         '%d.%m.%Y %H:%M:%S') if obj_dict.get(
        'os_update_search', None) else None
    server.os_installed = datetime.datetime.strptime(obj_dict['os_installed'], '%d.%m.%Y %H:%M:%S') if obj_dict.get(
        'os_installed', None) else None
    server.last_update_id = obj_dict['last_update_id']
    server.version = obj_dict['version']
    server.win_rm_access = obj_dict['win_rm_access']
    if obj_dict['replaced_by_id']:
        replaced_by = User.objects.get(pk=obj_dict['replaced_by_id'])
        if replaced_by.username == obj_dict['replaced_by_name']:
            server.replaced_by = replaced_by
    if obj_dict['updated_by_id']:
        updated_by = User.objects.get(pk=obj_dict['updated_by_id'])
        if updated_by.username == obj_dict['updated_by_name']:
            server.updated_by = updated_by
    server.futures.clear()
    for future in obj_dict['futures']:
        print(future)
        try:
            fut = ServerFuture.objects.get(pk=future['id'])
            if fut.name == future['name']:
                server.futures.add(fut)
            else:
                fut = ServerFuture(name=future['name'])
                fut.save()
                server.futures.add(fut)
        except ServerFuture.DoesNotExist:
            fut = ServerFuture(id=future['id'], name=future['name'])
            fut.save()
            server.futures.add(fut)
    server.installed_soft.clear()
    for soft in obj_dict['host_soft']:
        print(soft)
        try:
            sf = SoftwareCatalog.objects.get(pk=soft['id'])
            if sf.name == soft['name']:
                pass
            else:
                sf = SoftwareCatalog(name=soft['name'])
                sf.save()
        except SoftwareCatalog.DoesNotExist:
            sf = SoftwareCatalog(id=soft['id'], name=soft['name'])
            sf.save()
        host_soft = HostInstalledSoftware(soft=sf,
                                          server=server,
                                          version=soft['version'],
                                          installation_date=datetime.datetime.strptime(soft['installation_date'],
                                                                                       '%d.%m.%Y %H:%M:%S') if soft.get(
                                              'installation_date', None) else None)
        #host_soft.save()

    # server.save()


def import_server(obj_dict):
    from info.models import Server
    server_id = obj_dict['id']
    server_version = obj_dict['version']
    try:
        server = Server.objects.get(pk=server_id)
        if server.version <= server_version:
            print(obj_dict['name'])
            update_server(server, obj_dict)
        else:
            update_server(server, obj_dict)
    except Server.DoesNotExist:
        update_server(Server(), obj_dict)


def import_all():
    with open('export.json', 'rt') as f:
        for line in f:
            import_server(json.loads(line))


if __name__ == '__main__':
    # sys.argv.append('--no-multi_threading')
    # run_commandline_args(export_host, name='Export Server Config')
    sys.argv.append('--django')
    run_commandline_args(import_all, name='Export Server Config')
