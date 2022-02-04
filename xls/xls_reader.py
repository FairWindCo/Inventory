import re

from openpyxl import load_workbook
import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))

os.environ['DJANGO_SETTINGS_MODULE'] = 'Inventarisation.settings'
django.setup()

from info.models import ServerRoom, Domain, IP, InstalledSoftware, OS, Server
from django.contrib.auth.models import User


class BaseManager:
    cache = {}

    def check_name(self, name):
        return True if name and name is not None else False

    def clean_name(self, name):
        return name.strip()

    def get_value(self, name):
        if not self.check_name(name):
            return None
        name = self.clean_name(name)
        value = self.cache.get(name, None)
        if value:
            return value
        value = self.get_from_db(name)
        if value:
            self.cache[name] = value
        return value

    def find_in_db(self, name):
        pass

    def create_in_db(self, name):
        pass

    def get_from_db(self, name):
        value = self.find_in_db(name)
        if value:
            return value
        else:
            return self.create_in_db(name)


class RoomManager(BaseManager):
    matcher = (
        (re.compile(r'[Бб]ълижняя'), 'Ближняя'),
        (re.compile(r'[Лл]окальная'), 'Локальная'),
        (re.compile(r'[Дд]альняя[\s]*[НнHh]'), 'Дальняя H'),
        (re.compile(r'[Дд]альняя[\s]*[АфAa]'), 'Дальняя A'),
    )

    def clean_name(self, name):
        name = super().clean_name(name)
        for match, new_name in self.matcher:
            if match.match(name):
                return new_name
        return name

    def find_in_db(self, name):
        try:
            return ServerRoom.objects.get(name=name)
        except ServerRoom.DoesNotExist:
            return None

    def create_in_db(self, name):
        room = ServerRoom(name=name)
        room.save()
        return room


class DomainManager(BaseManager):

    def clean_name(self, name):
        return super().clean_name(name).lower()

    def find_in_db(self, name):
        try:
            return Domain.objects.get(name=name)
        except Domain.DoesNotExist:
            return None

    def create_in_db(self, name):
        domain = Domain(name=name)
        domain.save()
        return domain


class IPManager(BaseManager):

    def check_name(self, name):
        valid = super().check_name(name)
        if valid:
            try:
                import ipaddress
                ipaddress.ip_address(name)
                return True
            except ValueError:
                return False
        else:
            return False

    def find_in_db(self, name):
        try:
            return IP.objects.get(ip_address=name)
        except IP.DoesNotExist:
            return None

    def create_in_db(self, name):
        ip = IP(ip_address=name)
        ip.save()
        return ip


class SoftManager(BaseManager):

    def find_in_db(self, name):
        try:
            return InstalledSoftware.objects.get(name=name)
        except InstalledSoftware.DoesNotExist:
            return None

    def create_in_db(self, name):
        soft = InstalledSoftware(name=name)
        soft.save()
        return soft


class OSManager(BaseManager):
    matcher = (
        (re.compile(r'.*[Ss]erver.*2012[\s]*R2.*'), 'Windows Server 2012 R2 Ver 6.3'),
        (re.compile(r'.*[Ss]erver.*2012.*'), 'Windows Server 2012 Ver 6.2'),
        (re.compile(r'.*[Ss]erver[\s]*2016[\s]*[Dd]ata[Cc]enter.*'), 'Windows Server DataCenter 2016'),
        (re.compile(r'.*[Ss]erver[\s]*2016.*'), 'Windows Server Standard 2016'),
        (re.compile(r'.*[Ss]erver[\s]*2019[\s]*[Dd]ata[Cc]enter.*'), 'Windows Server DataCenter 2019'),
        (re.compile(r'.*[Ss]erver[\s]*2019.*'), 'Windows Server Standard 2019'),
        (re.compile(r'.*[Ss]erver[\s]*2022[\s]*[Dd]ata[Cc]enter.*'), 'Windows Server DataCenter 2022'),
        (re.compile(r'.*[Ss]erver[\s]*2022.*'), 'Windows Server Standard 2022'),
        (re.compile(r'.*2008.*'), 'Windows Server Enterprise 2008 R2 SP1'),
        (re.compile(r'.*2003.*'), 'Windows Server 2003'),
    )

    def clean_name(self, name):
        name = super().clean_name(name)
        for match, new_name in self.matcher:
            if match.match(name):
                return new_name
        return name

    def find_in_db(self, name):
        try:
            return OS.objects.get(name=name)
        except OS.DoesNotExist:
            return None

    def create_in_db(self, name):
        os = OS(name=name)
        os.save()
        return os


if __name__ == "__main__":
    rooms = RoomManager()
    domains = DomainManager()
    ipsm = IPManager()
    softm = SoftManager()
    osm = OSManager()
    admin_user = User.objects.get(pk=1)
    softs_re = re.compile(r'([\r\n]|[\s]{2,})')

    wb = load_workbook(r'\\bs.local.erc\IT\BSPD\IT infrastructure\ERC_BS_Servers_2022_1_3.xlsx')
    print(wb.sheetnames)
    ws = wb['SERVERS']
    for x in range(2, 84):
        room = rooms.get_value(ws.cell(row=x, column=1).value)
        if not room:
            print(f"ROW {x} NO ROOM NAME")
            continue
        domain = domains.get_value(ws.cell(row=x, column=3).value)
        if not domain:
            print(f"ROW {x} NO DOMAIN NAME")
            continue
        ip_list = ws.cell(row=x, column=2).value
        ips = [ipsm.get_value(ip) for ip in ip_list.split('\n')]

        name = ws.cell(row=x, column=4).value

        if not name:
            print(f"ROW {x} NO NAME")
            continue
        else:
            name = name.split("\n")[0]
        spft_list = ws.cell(row=x, column=12).value
        if spft_list:
            list_installed_soft = softs_re.split(spft_list)
            list_installed_soft = filter(lambda a: True if len(a.strip()) >= 1 else False, list_installed_soft)
            softs = [softm.get_value(soft.strip()) for soft in list_installed_soft]
        else:
            softs = []

        os_info = ws.cell(row=x, column=6).value
        if not os_info:
            print(f"ROW {x} NO OS")
            continue
        os_desc = os_info.split('\n')
        os = osm.get_value(os_desc[0])

        ver = os_desc[1] if len(os_desc) > 1 else None

        zabix = True if ws.cell(row=x, column=8).value == '+' else False
        comments = ws.cell(row=x, column=14).value
        virtual_machine = ws.cell(row=x, column=5).value
        virtual_machine = virtual_machine.strip() if virtual_machine else None
        server = Server(name=name.upper(),
                        domain=domain,
                        room=room,
                        os_name=os,
                        virtual_server_name=virtual_machine,
                        os_version=ver,
                        description=comments,
                        has_monitoring_agent=zabix,
                        updated_by=admin_user,
                        )
        server.save()
        server.ip_addresses.set(ips)
        server.installed_soft.set(softs)
        server.save()
