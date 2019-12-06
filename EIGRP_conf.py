from netmiko import ConnectHandler
import netaddr
import re

device = {
    "device_type": "cisco_ios",
    "host": "192.168.126.137",
    "username": "admin",
    "password": "Cisco123",
    "verbose": True,
    "port": "22"
}

eigrp_config_commands = ["router eigrp 10",
                         "network 10.0.100.0 0.0.0.255",
                         "network 192.168.100.0 0.0.0.255",
                         "network 192.168.126.0 0.0.0.255"]

session = ConnectHandler(**device)
# print(session.send_config_set(eigrp))
command = session.send_command("show ip route | include C")
connected_routes = str(command)
session.disconnect()

ip_list = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)", connected_routes)


def wildcard_conversion(subnet):
    wildcard = []
    for octet in subnet.split('.'):
        inverse = 255 - int(octet)
        wildcard.append(str(inverse))
    wildcard = '.'.join(wildcard)
    return wildcard


def eigrp_network():
    for item in ip_list:
        cidr = netaddr.IPNetwork(item)
        subnet = str(cidr.netmask)
        print(cidr.ip, wildcard_conversion(subnet))


eigrp_network()

