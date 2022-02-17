from typing import Iterable

from remoting import run_commandline_args


def update_hardware(host, user_name, password, debug=False):
    import logging
    from remoting.win_remote import connect
    from remoting.get_hardware_info import get_platform_name, get_cpu, get_mem, get_physical_disk_space
    from info.models.configurations import Configuration, DiskConfiguration, HDDType
    from logview.models import ServerModificationLog

    def add_discs_to_config(config, disk_desc):
        disk_info = DiskConfiguration(configuration=config, pool_name=disk_desc['model'],
                                      hdd_size=round(disk_desc['Size']))
        if disk_desc['model'] and disk_desc['model'].find('irtual') >= 0:
            disk_info.hdd_type = HDDType.VIRTUAL
        disk_info.save()

    def process_add_discs_to_config(config, disks):
        if not isinstance(disks, dict) and isinstance(disks, Iterable):
            for disk in disks:
                add_discs_to_config(config, disk)
        else:
            add_discs_to_config(config, disks)

    def update_discs_config(config, disks):

        disks_set = set(config.disks.all())

        def search_disk(disk_set, name, size):
            for disk in disk_set:
                if disk.pool_name == name and disk.hdd_size == size:
                    return disk

        def process_disk(disk_desc):
            name = disk_desc['model']
            size = round(disk_desc['Size'])
            installed_disk = search_disk(disks_set, name, size)
            if installed_disk:
                disks_set.remove(installed_disk)
            else:
                add_discs_to_config(config, disk_desc)
                ServerModificationLog(server=host, description=f'Disk added {name} {size}').save()

        if not isinstance(disks, dict) and isinstance(disks, Iterable):
            for disk in disks:
                process_disk(disk)
        else:
            process_disk(disks)

        for disk in disks_set:
            ServerModificationLog(server=host, description=f'Disk removed {disk.pool_name} {disk.hdd_size}').save()
            disk.delete()

    if host:
        if debug:
            print(host.canonical_name)
        s = connect(host.canonical_name, user_name, password)
        if s:
            platform_name = get_platform_name(s)[0]
            cpu = get_cpu(s)
            if not cpu:
                return
            if not isinstance(cpu, dict) and isinstance(cpu, Iterable):
                cpu_count = len(cpu)
                if cpu_count == 0:
                    return
                cpu = cpu[0]
            else:
                cpu_count = 1
            mem = round(float(get_mem(s)[0].replace(',', '.')))

            disks = get_physical_disk_space(s)
            if host.hardware.count() == 0:
                config = Configuration(server=host)
                config.platform_name = f"{platform_name}  {cpu['Name']}"
                config.ram = round(float(mem))
                config.num_cores = cpu['NumberOfCores']
                config.num_virtual = cpu['NumberOfLogicalProcessors']
                config.save()
                process_add_discs_to_config(config, disks)
            else:
                config = host.hardware.first()
                changed = False
                if config.ram != mem:
                    config.ram = mem
                    changed = True
                if config.num_cores != cpu['NumberOfCores']:
                    config.num_cores = cpu['NumberOfCores']
                    changed = True
                if config.num_virtual != cpu['NumberOfLogicalProcessors']:
                    config.num_virtual = cpu['NumberOfLogicalProcessors']
                    changed = True
                if changed:
                    ServerModificationLog(server=host, description='Hardware Changed')
                    config.platform_name = f"{platform_name}  {cpu['Name']}"
                    config.save()
                if config.disks.count() == 0:
                    process_add_discs_to_config(config, disks)
                else:
                    update_discs_config(config, disks)
        else:
            logging.warning(f"D`ONT CONNECT {host}")
    else:
        logging.warning(f"NO SERVER")


if __name__ == '__main__':
    run_commandline_args(update_hardware, name='Update Server Roles')
