import json
import sys
from typing import Iterable

from remoting import run_commandline_args


def get_all_fields(obj):
    if isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, bool):
        return obj
    elif isinstance(obj, Iterable):
        return obj
    elif isinstance(obj, dict):
        return obj
    elif isinstance(obj, object):
        if hasattr(obj, '__dict__') and obj.__dict__:
            return {name: get_all_fields(getattr(obj, name)) for name in obj.__dict__}
        elif hasattr(obj, '__slots__') and obj.__slots__:
            return {name: get_all_fields(getattr(obj, name)) for name in obj.__slots__}


def convert_server_to_json(server):
    try:
        response = {
            'id': server.pk,
            'name': server.name,
            'domain_name': server.domain.name,
            'domain_id': server.domain_id,
            'os_name': server.os_name.name,
            'os_name_id': server.os_name_id,
            'room_name': server.room.name,
            'room_id': server.room_id,
            'virtual_server_name': server.virtual_server_name,
            'os_version': server.os_version,
            'description': server.description,
            'has_internet_access': server.has_internet_access,
            'has_monitoring_agent': server.has_monitoring_agent,
            'is_online': server.is_online,
            'replaced_by_id': server.replaced_by.pk if server.replaced_by else None,
            'replaced_by_name': server.replaced_by.username if server.replaced_by else None,
            'updated_at': server.updated_at.strftime('%d.%m.%Y %H:%M:%S') if server.updated_at else '',
            'created_at': server.created_at.strftime('%d.%m.%Y %H:%M:%S') if server.created_at else '',
            'updated_by_id': server.updated_by.pk if server.updated_by else None,
            'updated_by_name': server.updated_by.username if server.updated_by else None,
            'os_last_update': server.os_last_update.strftime('%d.%m.%Y %H:%M:%S') if server.os_last_update else '',
            'os_update_search': server.os_update_search.strftime(
                '%d.%m.%Y %H:%M:%S') if server.os_update_search else '',
            'last_update_id': server.last_update_id,
            'os_installed': server.os_installed.strftime('%d.%m.%Y %H:%M:%S') if server.os_installed else '',
            'version': server.version,
            'win_rm_access': server.win_rm_access,

            'futures': [{'id': future.pk, 'name': future.name} for future in server.futures.all()],
            'ip_addresses': [{'id': ip_addresses.pk, 'ip': ip_addresses.ip_address} for ip_addresses in
                             server.ip_addresses.all()],
            'applications': [{'id': application.pk, 'name': application.name} for application in
                             server.applications.all()],
            'host_soft': [{
                'id': installed_soft.pk,
                'name': installed_soft.soft.name,
                'version': installed_soft.version,
                'installation_date': installed_soft.installation_date.strftime(
                    '%d.%m.%Y %H:%M:%S') if installed_soft.installation_date else '',
            } for installed_soft in
                server.host_soft.all()],
            'app_info': [{
                'id': app.id,
                'app_name': app.application.name,
                'app_id': app.application.pk,
                'description': app.description,
                'server_specifications': [
                    {'server_role_id': spec.pk,
                     'server_role_name': spec.name,
                     'server_role_description': spec.description,
                     }
                    for spec in app.specifications.all()
                ]

            } for app in server.app_info.all()],
            'hardware': [
                {'id': hardware.id,
                 'platform_name': hardware.platform_name,
                 'num_cpu': hardware.num_cpu,
                 'num_cores': hardware.num_cores,
                 'num_virtual': hardware.num_virtual,
                 'cpu_type': hardware.cpu_type,
                 'ram': hardware.ram,
                 'description': hardware.description,
                 'disks': [{
                     'id': disk.id,
                     'pool_name': disk.pool_name,
                     'hdd_size': disk.hdd_size,
                     'hdd_type': disk.hdd_type,
                     'raid_type': disk.raid_type,
                 } for disk in hardware.disks.all()]
                 }
                for hardware in server.hardware.all()]

        }

        # dict_obj = get_all_fields(server)
        # dict_obj = serializers.serialize('json', [server])
        # print(dict_obj)
        # json_str = json.dumps(dict_obj)

        json_str = json.dumps(response)
        # print(json_str)
    except Exception as e:
        print(e, server)
        json_str = None

    return json_str


def export_host(host, user_name, password, debug=False):
    if debug:
        print(host.name)
    line = convert_server_to_json(host)
    if debug:
        print(line)
    return line


def export_all():
    from info.models import Server
    with open('export.json', 'wt') as f:
        for server in Server.objects.all():
            jsons = export_host(server, '', '')
            print(jsons)
            f.write(jsons + '\n')


if __name__ == '__main__':
    # sys.argv.append('--no-multi_threading')
    # run_commandline_args(export_host, name='Export Server Config')
    sys.argv.append('--django')
    run_commandline_args(export_all, name='Export Server Config')
