# Reference: https://github.com/CiscoDevNet/netprog_basics/blob/master/application_hosting/python_onbox
# /iosxe_guestshell_setup.txt
from netmiko import ConnectHandler

iox = ["configure terminal",
       "iox",
       "int VirtualPortGroup 0",
       "ip add 192.168.100.1 255.255.255.0"
       "no sh",
       "ip nat inside",
       "exit",
       "int GigabitEthernet 3",
       "ip nat outside",
       "exit",
       "ip access-list standard NAT_ACL",
       "permit 192.168.0.0 0.0.255.255",
       "exit",
       "ip nat inside source list NAT_ACL interface GigabitEthernet3 overload",
       "app-hosting appid guestshell",
       "app-vnic gateway1 virtualportgroup 0 guest-interface 0",
       "guest-ipaddress 192.168.100.2 netmask 255.255.255.0",
       "exit"
       "app-default-gateway 192.168.100.1 guest-interface 0",
       "name-server0 8.8.8.8",
       "end",
       "wr",
       "guestshell enable",
       "show app-hosting list"]

device = {
    "device_type": "cisco_ios",
    "host": "192.168.126.137",
    "username": "admin",
    "password": "Cisco123",
    "port": "22"
}

session = ConnectHandler(**device)

for command in iox:
    output = session.send_command(command)
    print(output)

print("Guestshell Configuration Script Done")
