import base64
import datetime
import ipaddress
import json
import math
import os.path
import re
import sys
from urllib.parse import unquote

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
# Create your views here.
from django.middleware import csrf
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from rsa import PrivateKey, decrypt

from dictionary.models import IP, Domain, ServerRoom, SoftwareCatalog, ServerFuture, ServerService, ServerScheduledTask
from info.models import Server, HostInstalledSoftware, Configuration, DiskConfiguration
from info.models.applications import HostScheduledTask
from logview.models import ServerModificationLog
from task_logger.models import ServerTaskReport
from xls.xls_reader import OSManager

task_name_regexps = [
    re.compile(r'(.*)(S-[0-9]-[0-9]-[0-9]{1,2}-[0-9a-fA-F]{5,}-[0-9a-fA-F]{5,}-[0-9a-fA-F]{5,}-[0-9a-fA-F]{3,})'),
    re.compile(r'(.*)(-[0-9a-fA-F]{7,9}-[0-9a-fA-F]{4,5}-[0-9a-fA-F]{4,5}'
               r'-[0-9a-fA-F]{4,}-([0-9a-fA-F]{9,}|_[0-9a-fA-F]{5,10}))'),
    re.compile(r'(.*)(-\{[0-9a-fA-F]{7,9}-[0-9a-fA-F]{4,5}-[0-9a-fA-F]{4,5}'
               r'-[0-9a-fA-F]{4,}-([0-9a-fA-F]{9,}|_[0-9a-fA-F]{5,10})\})'),
    re.compile(r'(.*)(-[0-9a-fA-F]{9,}|_[0-9a-fA-F]{5,10})'),
]


def converting_tasks_service_name(name):
    for reg in task_name_regexps:
        if match := reg.match(name):
            return f'{match[1]} <Users>'
    return name


def load_key(key_path='private.pem'):
    if key_path is None:
        key_path = 'private.pem'
    if isinstance(key_path, str):
        if os.path.exists(key_path) and os.path.isfile(key_path):
            with open(key_path, 'rb') as f:
                key = f.read()
            return PrivateKey.load_pkcs1(key)
    elif isinstance(key_path, (bytes, bytearray)):
        return PrivateKey.load_pkcs1(key_path)


def test_request_body(body_text, key=None, key_field_name='key',
                      control_value_field='host',
                      time_format='%d%m%y%H%M%S',
                      timedelta=600):
    if body_text:
        key = load_key(key)
        if key:
            data = json.loads(unquote(body_text))
            enc_key = data.get(key_field_name, None)
            control_field = data.get(control_value_field, None)
            if enc_key and control_field:
                decoded_key = base64.b64decode(enc_key)
                decoded_key_value_byte = decrypt(decoded_key, key)
                decoded_key_value = decoded_key_value_byte.decode()
                if decoded_key_value.startswith(control_field):
                    print(decoded_key_value, )
                    time_str = decoded_key_value[len(control_field):]
                    print(decoded_key_value, time_str)
                    time_value = datetime.datetime.strptime(time_str, time_format)

                    if (datetime.datetime.now() - time_value).seconds < timedelta:
                        return data


def process_json_report(json_data):
    if json_data:
        server_name = json_data.get('host', None)
        if server_name:
            try:
                server_name = server_name.upper()
                server = Server.objects.get(name=server_name)
                ndt = datetime.datetime.strptime(json_data['time'],
                                                 '%a %b %d %H:%M:%S %Y')
                dt = timezone.make_aware(ndt, timezone.get_current_timezone())
                report = ServerTaskReport(server=server,
                                          info=json_data.get('message', None),
                                          report_date=dt,
                                          is_error=not json_data.get('is_error', False))
                report.save()

                return JsonResponse({'result': 'ok'})
            except Server.DoesNotExist:
                return JsonResponse({'result': 'error', 'message': 'Unknown server:' + server_name})
        else:
            return JsonResponse({'result': 'error', 'message': 'No host name is request'})
    else:
        return HttpResponseForbidden('Incorrect requests')


@csrf_exempt
def process_message(request):
    if request.method == 'POST':
        try:
            body_text = request.body
            json_data = test_request_body(body_text.decode())
            return process_json_report(json_data)
        except BaseException as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return JsonResponse({'result': 'error', 'message': str(e), 'file': fname, 'line': exc_tb.tb_lineno})
    else:
        print('NOT POST REQUESTS')
        return HttpResponseForbidden('Incorrect requests type')


def get_token(request):
    from django.conf import settings
    return JsonResponse({
        'csrf': csrf.get_token(request),
        'header_name': settings.CSRF_HEADER_NAME})


NOW = datetime.datetime.now()
LOCAL_NOW = NOW.astimezone()
LOCAL_TZ = LOCAL_NOW.tzinfo
UTC_TZ = datetime.timezone.utc


def process_time(installed):
    for format_time in [
        '%Y%m%d',
        '%Y/%m/%d',
        '%Y.%m.%d',
        '%d%m%Y',
        '%d/%m/%Y',
        '%d.%m.%Y',
        '%Y%m%d%H%M%S.%f',
        '%d.%m.%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%m.%d.%Y %H:%M:%S',
        '%H:%M:%S %d.%m.%Y',
        '%H:%M:%S %d/%m/%Y',
        '%H:%M:%S %m/%d/%Y',
        '%H:%M:%S %m.%d.%Y',
    ]:
        if installed == '01.01.0001 0:00:00':
            return None
        try:
            return make_aware(timezone.datetime.strptime(installed, format_time), timezone.get_current_timezone())
            # return datetime.datetime.strptime(installed, format_time).astimezone(LOCAL_TZ)
        except Exception as e:
            # print(e)
            pass


def process_hotfix(server, hotfix_list):
    sorted_hos_fix = sorted(
        [(hotfix_id, process_time(date_install)) for hotfix_id, date_install in hotfix_list],
        key=lambda a: a[1].timestamp() if a[1] else 0
    )
    hotfix_id, installed = sorted_hos_fix[-1]
    server.last_update_id = hotfix_id
    server.os_last_update = installed


def process_soft(server, soft_info):
    check_date = make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    installed_softs = HostInstalledSoftware.objects.filter(server=server).count() > 0
    for soft in soft_info:
        # print(soft)
        if soft['name'] is None:
            continue
        try:
            soft_i = SoftwareCatalog.objects.get(name=soft['name'])
        except SoftwareCatalog.DoesNotExist:
            soft_i = SoftwareCatalog(name=soft['name'])
            soft_i.save()

        try:
            host_info = HostInstalledSoftware.objects.get(soft=soft_i,
                                                          server=server)
            host_info.last_check_date = check_date
            if host_info.is_removed:
                log = ServerModificationLog(server=server,
                                            log_type=ServerModificationLog.LogType.INSTALL,
                                            topic=ServerModificationLog.LogTopic.SOFT,
                                            description=f're install soft {soft_i.name} '
                                                        f'from {host_info.version} to {soft["version"]}')
                log.save()
                host_info.is_removed = False
            elif host_info.version != soft['version']:
                log = ServerModificationLog(server=server,
                                            log_type=ServerModificationLog.LogType.UPDATE,
                                            topic=ServerModificationLog.LogTopic.SOFT,
                                            description=f'update soft {soft_i.name} '
                                                        f'from {host_info.version} to {soft["version"]}')
                log.save()
            host_info.version = soft['version']
            host_info.installation_date = process_time(soft['installed'])
        except HostInstalledSoftware.DoesNotExist:
            if installed_softs:
                log = ServerModificationLog(server=server,
                                            log_type=ServerModificationLog.LogType.INSTALL,
                                            topic=ServerModificationLog.LogTopic.SOFT,
                                            description=f'installed new soft {soft_i.name}')
                log.save()
            host_info = HostInstalledSoftware(soft=soft_i,
                                              server=server,
                                              version=soft['version'],
                                              installation_date=process_time(soft['installed']),
                                              last_check_date=check_date
                                              )
        host_info.save()
    # for host_soft in HostInstalledSoftware.objects.filter(server=server).filter(
    #         Q(last_check_date__lt=check_date) | Q(last_check_date__isnull=True)).all():
    #     log = ServerModificationLog(server=server, description=f'remove soft {host_soft.name}')
    #     log.save()
    # HostInstalledSoftware.objects.filter(server=server).filter(
    #     Q(last_check_date__lt=check_date) | Q(last_check_date__isnull=True)).update(is_removed=True)
    remove_deleted_info(HostInstalledSoftware, check_date, server, 'soft', 'soft.name',
                        ServerModificationLog.LogTopic.SOFT)


def remove_deleted_info(info_class, check_date, server, info_type, name_path='name',
                        topic=ServerModificationLog.LogTopic.OTHER):
    for obj in info_class.objects.filter(server=server, is_removed=False).filter(
            Q(last_check_date__lt=check_date) | Q(last_check_date__isnull=True)).all():
        name = get_attribute(obj, name_path)
        log = ServerModificationLog(server=server,
                                    log_type=ServerModificationLog.LogType.REMOVED,
                                    topic=topic,
                                    description=f'remove {info_type} {name}')
        log.save()
    info_class.objects.filter(server=server).filter(
        Q(last_check_date__lt=check_date) | Q(last_check_date__isnull=True)).update(is_removed=True)


def process_tasks(server, task_info):
    def check_system_task(name, task):
        if 'author' in task and task['author']:
            author_lower = task['author'].lower()
            if author_lower.find('microsoft') >= 0 or author_lower.find('микрософт') >= 0:
                return True
        path = (task['new_path'] if 'new_path' in task else task['path']).lower()
        if path.find('powershell.exe') >= 0:
            return False
        if path == 'com\d-com task':
            return True
        if path.startswith('%systemroot%'):
            return True
        if path.startswith('%windir%'):
            return True
        check_name = name.lower()
        if check_name == 'user_feed_synchronization':
            return True
        if check_name.startswith('windows defender'):
            return True
        return False

    check_date = make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    installed_tasks = HostScheduledTask.objects.filter(server=server).count() > 0
    for task in task_info:
        try:
            print(task)
            if task['name'] is None or not task['name'] or task['task'] is None:
                continue
            if not task['name']:
                name = task['task']
            else:
                name = task['name']
                last_index = name.rfind('\\')
                if last_index >= 0:
                    name = name[last_index + 1:]
            name = converting_tasks_service_name(name)
            path = task['new_path'] if len(task['new_path']) < 255 else task['task']
            try:
                task_i = ServerScheduledTask.objects.get(name=name, execute_path=path)
                task_i.execute_path = path
                if len(task['new_path']) > 255:
                    task_i.description += task['new_path']
                task_i.silent = check_system_task(name, task)
                task_i.save()
            except ServerScheduledTask.DoesNotExist:
                print("Create Task", name)
                task_i = ServerScheduledTask(name=name, execute_path=path,
                                             description=f"{task['comment']} {task['new_path'] if len(task['new_path']) else ''}")
                task_i.silent = check_system_task(name, task)
                task_i.save()

            try:
                host_info = HostScheduledTask.objects.get(task=task_i,
                                                          server=server)
                if host_info.is_removed:
                    log = ServerModificationLog(server=server,
                                                log_type=ServerModificationLog.LogType.INSTALL,
                                                topic=ServerModificationLog.LogTopic.TASK,
                                                description=f're setup task {name}')
                    log.save()
                elif host_info.exit_code != str(task['last_result']) or host_info.status != str(task['status']):
                    log = ServerModificationLog(server=server,
                                                log_type=ServerModificationLog.LogType.UPDATE,
                                                topic=ServerModificationLog.LogTopic.TASK,
                                                description=f'task {name}  change status {task["status"]} or '
                                                            f'exit code {task["last_result"]}')
                    log.save()
                host_info.last_check_date = check_date
                host_info.installation_date = process_time(task['start_time'])
                host_info.next_run = process_time(task['next_run'])
                host_info.last_run = process_time(task['last_run'])
                host_info.run_user = task['runas']
                host_info.author = task['author']
                host_info.schedule_type = task['schedule_type'] if \
                    len(task['schedule_type']) < 255 else task['schedule_type'][:250] + '...'
                host_info.exit_code = task['last_result']
                host_info.status = task['status']
                host_info.schedule = task['schedule']
                host_info.is_removed = False
            except HostScheduledTask.DoesNotExist:
                if installed_tasks:
                    log = ServerModificationLog(server=server,
                                                log_type=ServerModificationLog.LogType.INSTALL,
                                                topic=ServerModificationLog.LogTopic.TASK,
                                                description=f'new task {name}')
                    log.save()
                host_info = HostScheduledTask(task=task_i,
                                              server=server,
                                              installation_date=process_time(task['start_time']),
                                              next_run=process_time(task['next_run']),
                                              last_run=process_time(task['last_run']),
                                              run_user=task['runas'],
                                              author=task['author'],
                                              schedule_type=task['schedule_type'],
                                              exit_code=task['last_result'],
                                              status=task['status'],
                                              schedule=task['schedule'],
                                              last_check_date=check_date,
                                              )
            host_info.save()
        except Exception as e:
            print(e, task)
    # for host_task in HostScheduledTask.objects.filter(server=server).filter(
    #         Q(last_check_date__lt=check_date) | Q(last_check_date__isnull=True)).all():
    #     log = ServerModificationLog(server=server, description=f'delete task {host_task.name}')
    #     log.save()
    #
    # HostScheduledTask.objects.filter(server=server).filter(
    #     Q(last_check_date__lt=check_date) | Q(last_check_date__isnull=True)).update(is_removed=True)
    remove_deleted_info(HostScheduledTask, check_date, server, 'task', 'task.name', ServerModificationLog.LogTopic.TASK)


def process_domain(server, domain_info):
    try:
        domain = Domain.objects.get(name=domain_info)
    except Domain.DoesNotExist:
        domain = Domain(name=domain_info)
        domain.save()
    server.domain = domain


def get_attribute(obj, name):
    names = name.split('.')
    for n in names:
        if hasattr(obj, n):
            obj = getattr(obj, n)
        elif n in obj:
            obj = obj[n]
        else:
            obj = 'unknown'
    return obj


def process_ip(server, ip_info, process_net=None):
    for ip in server.ip_addresses.all():
        ip.delete()
    server.save()
    for ip in ip_info:
        try:
            adr = IP.objects.get(ip_address=ip)
        except IP.DoesNotExist:
            adr = IP(ip_address=ip)
            adr.save()
        if process_net:
            cur_ip = ipaddress.ip_address(adr.ip_address)
            for network in process_net:
                net_address = ipaddress.ip_network(f'{str(network.ip_address)}/{network.mask}')
                if cur_ip in net_address:
                    try:
                        rooms = network.room.first()
                        if rooms:
                            server.room = rooms
                    except Exception:
                        pass

        server.ip_addresses.add(adr)
        server.save()


def process_futures(server, futures):
    server.futures.clear()
    for future in futures:
        try:
            fut = ServerFuture.objects.get(name=future)
        except ServerFuture.DoesNotExist:
            fut = ServerFuture(name=future)
            fut.save()
        server.futures.add(fut)


def process_daemons(server, daemons):
    def check_silent_service(name):
        check_name = name.lower()

        if check_name.startswith('windows push notifications'):
            return True
        if check_name.startswith('clipboard user'):
            return True
        if check_name.startswith('connected devices platform'):
            return True
        if check_name.startswith('user data access'):
            return True
        return False

    server.daemons.clear()
    for daemon in daemons:
        name = converting_tasks_service_name(daemon)
        try:
            fut = ServerService.objects.get(name=name)
        except ServerService.DoesNotExist:
            fut = ServerService(name=name)
            fut.silent = check_silent_service(name)
            fut.save()
        server.daemons.add(fut)


def process_json_info(json_data):
    if json_data:
        host = json_data['host'].upper()
        try:
            server = Server.objects.get(name=host)
            networks = None
        except Server.DoesNotExist:
            server = Server(name=host)
            server.room = ServerRoom.objects.first()
            networks = IP.objects.filter(mask__lt=32).all()
            server.updated_by = User.objects.first()
        if server.os_version is None:
            version_os = json_data.get('Version', None)
            build = json_data.get('BuildNumber', None)
            if version_os:
                version_os = version_os + '.' + build if build else version_os
            server.os_version = version_os
        install_time = json_data.get('InstallDate', None)
        if server.os_installed is None and install_time:
            server.os_installed = process_time(install_time[:-4])
        # print(json_data['sysname'])
        sys_name = json_data.get('sysname', None)
        if sys_name:
            osm = OSManager()
            sys_name = osm.get_value(sys_name)
            server.os_name = sys_name
        process_domain(server, json_data['Domain'])
        server.save()
        process_ip(server, json_data['ip'], networks)
        process_soft(server, json_data.get('soft', []))
        process_futures(server, json_data.get('futures', []))
        process_daemons(server, json_data.get('services', []))
        process_tasks(server, json_data.get('tasks', []))
        process_hotfix(server, json_data.get('hotfix', []))
        if json_data['Manufacturer']:
            if server.hardware.first():
                cpu = server.hardware.first()
            else:
                cpu = Configuration(server=server)

            cpu.platform_name = ' '.join([json_data.get('Manufacturer', ''),
                                          json_data.get('Model', ''),
                                          ])
            cpu.num_cpu = json_data.get('NumberOfProcessors', 1)
            if json_data['cpu_count'] >= 1:
                cpu.num_cores = json_data['cpu_info'][0].get('NumberOfCores', 1)
                cpu.num_virtual = json_data['cpu_info'][0].get('ThreadCount', 1)
                cpu.cpu_type = json_data['cpu_info'][0].get('model', '')
            cpu.description = json_data.get('SystemFamily', '')
            cpu.ram = math.ceil(int(json_data.get('TotalPhysicalMemory', 0)) / (1024 * 1024 * 1024))
            for disk in cpu.disks.all():
                disk.delete()
            cpu.save()
            for disk_info in json_data['hdd_info']:
                d = DiskConfiguration(configuration=cpu)
                d.pool_name = disk_info['model']
                d.hdd_size = math.ceil(int(disk_info['size']) / (1024 * 1024 * 1024))
                d.save()
            cpu.save()

        server.save()

        return JsonResponse({'result': 'ok'})


@csrf_exempt
def process_host_info_json(request):
    if request.method == 'POST':
        try:
            body_text = request.body
            json_data = test_request_body(body_text.decode())
            return process_json_info(json_data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return JsonResponse({'result': 'error', 'message': str(e), 'file': fname, 'line': exc_tb.tb_lineno})
    return HttpResponseForbidden()
