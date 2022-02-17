from remoting.win_remote import powershell_json, powershell


def get_logical_disk_space(session):
    return powershell_json(session,
                           'Get-WmiObject -Class win32_logicaldisk | select DeviceId, MediaType, '
                           '@{n="Size";e={[math]::Round($_.Size/1GB,2)}},@{n="FreeSpace";'
                           'e={[math]::Round($_.FreeSpace/1GB,2)}} | convertto-json')


def get_physical_disk_space(session):
    return powershell_json(session,
                           'Get-WMIObject -Class Win32_DiskDrive '
                           '| select model,@{n="Size";e={[math]::Round($_.Size/1GB,2)}} | convertto-json')


def get_cpu(session):
    return powershell_json(session,
                           'Get-WmiObject -class Win32_processor|select Name,NumberOfCores,NumberOfLogicalProcessors | convertto-json')


def get_mem(session):
    return powershell(session,
                           '(Get-WmiObject -Class Win32_ComputerSystem '
                           '| select @{n="Size";e={[math]::Round($_.TotalPhysicalMemory/1GB,2)}}).Size')


def get_platform_name(session):
    return powershell(session, '(Get-WmiObject Win32_OperatingSystem).OSArchitecture')
