# Reference: https://github.com/CiscoDevNet/netprog_basics/blob/master/application_hosting/python_onbox
# /iosxe_guestshell_setup.txt
from netmiko import ConnectHandler

virtual_port_interface = "VirtualPortGroup 0"
virtual_port_group_address = "192.168.200.1 255.255.255.0"
ACL_name = "NAT_ACL"
ACL_permit_address = "192.168.0.0 0.0.255.255"
NAT_inside_interface = "GigabitEthernet 3"
guest_IP_address = "192.168.200.2 netmask 255.255.255.0"
app_default_gateway = "192.168.200.1"
name_server = "8.8.8.8"

virtual_port = ["iox", "int " + virtual_port_interface, "ip add " + virtual_port_group_address, "no sh", "ip nat inside"]
NAT_ACL = ["ip access-list standard " + ACL_name, "permit " + ACL_permit_address]
app_hosting = ["ip nat inside source list " + ACL_name + " interface " + NAT_inside_interface + " overload",
               "app-hosting appid guestshell", "app-vnic gateway1 " + virtual_port_interface + " guest-interface 0",
               "guest-ipaddress " + guest_IP_address]
app_gate = ["app-hosting appid guestshell", "app-default-gateway " + app_default_gateway + " guest-interface 0",
            "name-server0 " + name_server]
guest_shell_enable = "guestshell enable"
app_hosting_list = "show app-hosting list"

device = {
    "device_type": "cisco_ios",
    "host": "192.168.126.138",
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
