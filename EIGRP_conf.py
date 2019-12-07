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

session = ConnectHandler(**device)

interface_names = []
eigrp_networks = []
wildcards = []
networks = []
netmasks = []

# get interface names
interfaces = session.send_command("show ip int b")
for line in interfaces.split("\n"):
    interface_names.append(line.split(" ", 1)[0])
interface_names.pop(0)  # remove interface header
# print(interface_names)

# get cidr connected networks
connected_routes = session.send_command("show ip route | include C")
connected_networks = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)", connected_routes)
# print(connected_networks)

# get netmask from cidr connected networks
for item in connected_networks:
    # print(item)
    network = str(netaddr.IPNetwork(item).network)
    networks.append(network)
    netmask = str(netaddr.IPNetwork(item).netmask)
    netmasks.append(netmask)
    wildcard = str(netaddr.IPNetwork(item).hostmask)
    wildcards.append(wildcard)

# print(networks)
# print(netmasks)
# print(wildcards)

# construct eigrp networks
for item in range(1, len(networks), 1):
    eigrp = str(networks[item] + " " + wildcards[item])
    eigrp_networks.append(eigrp)

print(eigrp_networks)

eigrp_identifier = input(str("Enter a unique identifier number for EIGRP: "))
eigrp_passive = input((str(interface_names)) + "\nChoose passive interfaces for EIGRP from the list: ")

eigrp_config_commands = ["router eigrp " + eigrp_identifier,
                         "no auto-summary",
                         passive_interfaces,
                         eigrp_networks]


def device_configuration():
    print(session.send_config_set(eigrp_config_commands))


device_configuration()
session.disconnect()
