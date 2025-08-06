from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from django_helpers.request_processor import RequestValue
from export.export_server import convert_server_to_json, convert_server_to_json_short, convert_server_ip_to_json_short
from info.models import Server


class ServerHealth(ListView):
    model = Server





def get_servers_info(request):
    name = RequestValue.get_from_request(request, 'name')
    family = RequestValue.get_from_request(request, 'family')
    search = RequestValue.get_from_request(request, 'search')
    if name[1]:
        print(name)
        servers = Server.objects.filter(name=name[0])
    elif family[1]:
        servers = Server.objects.filter(os_name__family__icontains=family[0])
    elif search[1]:
        servers = Server.objects.filter(name__icontains=search[0])
    else:
        servers = Server.objects.all()
    json_servers = [{
        "name": server.name,
        "domain":server.domain.name,
        'os_name': server.os_name.name,
        'family': server.os_name.family,
        'room_name': server.room.name,
        'os_version': server.os_version,
        'status': server.status,        
        "ips": [ip_addresses.ip_address for ip_addresses in
                server.ip_addresses.all()]
    } for server in servers]

    return JsonResponse({"servers":json_servers})

def get_windows_ip(request):
    search = RequestValue.get_from_request(request, 'search')
    servers = Server.objects.filter(os_name__family__icontains='Windows').filter(status=Server.ServerState.WORK)
    if search[1]:
        servers = servers.filter(name__icontains=search[0])
    json_servers = [{
        "name": server.name,
        "domain":server.domain.name,
        "ips": [ip_addresses.ip_address for ip_addresses in
                server.ip_addresses.all()],
        'room_name': server.room.name,
                     } for server in servers]
    return JsonResponse({"servers":json_servers})
    
        