from __future__ import print_function, unicode_literals
from getpass import getpass
from netmiko import ConnectHandler, file_transfer
import device_info

# password = getpass("Input SSH Password : ")

source_file = 'cisco_ios_backup.txt'
dest_file = 'backup'
file_system = 'flash:'
direction = 'put'


def scp_copy():
    for net_device in (device_info.csr1000v1, device_info.csr1000v2):
        # Create the Netmiko SSH connection
        session = ConnectHandler(**net_device)
        scp = file_transfer(session,
                            source_file=source_file,
                            dest_file=dest_file,
                            file_system=file_system,
                            direction=direction,
                            overwrite_file=True)
        print(scp)


scp_copy()
