# Reference: https://github.com/CiscoDevNet/netprog_basics/blob/master/application_hosting/python_onbox
# /iosxe_guestshell_setup.txt
from netmiko import ConnectHandler

virtual_port = ["iox", "int VirtualPortGroup 0", "ip add 192.168.100.1 255.255.255.0", "no sh", "ip nat inside"]
NAT_ACL = ["ip access-list standard NAT_ACL", "permit 192.168.0.0 0.0.255.255"]
app_hosting = ["ip nat inside source list NAT_ACL interface GigabitEthernet3 overload", "app-hosting appid guestshell",
               "app-vnic gateway1 virtualportgroup 0 guest-interface 0",
               "guest-ipaddress 192.168.100.2 netmask 255.255.255.0"]
app_gate = ["app-hosting appid guestshell", "app-default-gateway 192.168.100.1 guest-interface 0",
            "name-server0 8.8.8.8"]
guest_shell_enable = "guestshell enable"
app_hosting_list = "show app-hosting list"

device = {
    "device_type": "cisco_ios",
    "host": "192.168.126.137",
    "username": "admin",
    "password": "Cisco123",
    "verbose": True,
    "port": "22"
}

session = ConnectHandler(**device)

print(session.send_config_set(virtual_port))
print(session.send_config_set(NAT_ACL))
print(session.send_config_set(app_hosting))
print(session.send_config_set(app_gate))
print(session.send_command(guest_shell_enable))
print(session.send_command(app_hosting_list))

print("Guestshell Configuration Script Done")
