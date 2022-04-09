import base64
import datetime
import json
import math
import os.path
import sys
from urllib.parse import unquote

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
# Create your views here.
from django.middleware import csrf
from django.utils import timezone
from django.utils.timezone import make_aware
from rsa import PrivateKey, decrypt

from dictionary.models import IP, Domain, ServerRoom, SoftwareCatalog, ServerFuture, ServerService
from info.models import Server, HostInstalledSoftware, Configuration, DiskConfiguration
from task_logger.models import ServerTaskReport
from xls.xls_reader import OSManager


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
            if enc_key:
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


# @csrf_exempt
def post_request(request):
    if request.method == 'POST':
        body_text = request.body
        try:
            json_data = test_request_body(body_text.decode())
            if json_data:
                server_name = json_data.get('host', None)
                if server_name:
                    try:
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
                return HttpResponseForbidden()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return JsonResponse({'result': 'error', 'message': str(e), 'file': fname, 'line': exc_tb.tb_lineno})


def get_token(request):
    return JsonResponse({
        'csrf': csrf.get_token(request)})


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
        '%Y%m%d%H%M%S.%f'
    ]:
        try:
            return make_aware(timezone.datetime.strptime(installed, format_time), timezone.get_current_timezone())
            # return datetime.datetime.strptime(installed, format_time).astimezone(LOCAL_TZ)
        except Exception:
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
    for soft in soft_info:
        #print(soft)
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
            host_info.version = soft['version']
            host_info.installation_date = process_time(soft['installed'])
        except HostInstalledSoftware.DoesNotExist:
            host_info = HostInstalledSoftware(soft=soft_i,
                                              server=server,
                                              version=soft['version'],
                                              installation_date=process_time(soft['installed']),
                                              last_check_date=check_date
                                              )
        host_info.save()
    HostInstalledSoftware.objects.filter(server=server).filter(
        Q(last_check_date__lt=check_date) | Q(last_check_date__isnull=True)).update(is_removed=True)


def process_domain(server, domain_info):
    try:
        domain = Domain.objects.get(name=domain_info)
    except Domain.DoesNotExist:
        domain = Domain(name=domain_info)
        domain.save()
    server.domain = domain


def process_ip(server, ip_info):
    for ip in server.ip_addresses.all():
        ip.delete()
    server.save()
    for ip in ip_info:
        try:
            adr = IP.objects.get(ip_address=ip)
        except IP.DoesNotExist:
            adr = IP(ip_address=ip)
            adr.save()
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
    server.daemons.clear()
    for daemon in daemons:
        try:
            fut = ServerService.objects.get(name=daemon)
        except ServerService.DoesNotExist:
            fut = ServerService(name=daemon)
            fut.save()
        server.daemons.add(fut)


def process_host_json(request):
    if request.method == 'POST':
        try:
            body_text = request.body
            json_data = test_request_body(body_text.decode())
            if json_data:
                host = json_data['host'].upper()
                try:
                    server = Server.objects.get(name=host)
                except Server.DoesNotExist:
                    server = Server(name=host)
                    server.room = ServerRoom.objects.first()
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
                process_ip(server, json_data['ip'])
                process_soft(server, json_data['soft'])
                process_futures(server, json_data.get('futures', []))
                process_daemons(server, json_data.get('services', []))
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
                    cpu.description = json_data.get('SystemFamily', None)
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
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return JsonResponse({'result': 'error', 'message': str(e), 'file': fname, 'line': exc_tb.tb_lineno})
    return HttpResponseForbidden()
