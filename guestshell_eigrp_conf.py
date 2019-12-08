import cli
import sys
import netaddr
import re

eigrp_configuration_list = []
interface_names = []
interface_list = []
eigrp_networks = []
eigrp_passive = []
wildcards = []
networks = []
netmasks = []

# get interface names
interfaces = cli.executep("show ip int b")
for line in interfaces.split("\n"):
    interface_names.append(line.split(" ", 1)[0])
# interface_names.pop(0)  # remove interface header

# get cidr connected networks from the routing table
connected_routes = cli.executep("show ip route | include C")
connected_networks = re.findall(r'[0-9]+(?:\.[0-9]+){3}', connected_routes)

# get network, netmask and wildcard from cidr using netaddr library
for item in connected_networks:
    network = str(netaddr.IPNetwork(item).network)
    networks.append(network)
    netmask = str(netaddr.IPNetwork(item).netmask)
    netmasks.append(netmask)
    wildcard = str(netaddr.IPNetwork(item).hostmask)
    wildcards.append(wildcard)

# construct eigrp connected networks
for item in range(0, len(networks), 1):
    eigrp = str(networks[item] + " " + wildcards[item])
    eigrp_networks.append(eigrp)

eigrp_identifier = input(str("\nEnter a unique identifier number for EIGRP: "))

loop = True
while loop:
    for item in range(1, len(interface_names), 1):
        print(item, interface_names[item])
    try:
        eigrp_passive = int(input("\nEnter passive interface number(s) for EIGRP from the list above, or press any "
                                  "other key to skip: "))
        if 1 <= eigrp_passive <= 100:
            interface_list.append(eigrp_passive)
    except ValueError:
        loop = False

print("\n--------------------")
print("EIGRP Configuration: ")
print("--------------------")
eigrp_configuration_list.append("router eigrp " + eigrp_identifier)
print("router eigrp " + eigrp_identifier)
eigrp_configuration_list.append("no auto-summary")
print("no auto-summary")
for i in interface_list:
    eigrp_configuration_list.append("passive-interface " + interface_names[i])
    print("passive-interface " + interface_names[i])
for j in eigrp_networks:
    eigrp_configuration_list.append("network " + j)
    print("network " + j)
print("--------------------")

apply_configuration = input("\nApply EIGRP configuration? 'yes' to apply, or press any other key to cancel: ")

if apply_configuration == 'yes':
    apply = cli.configurep(eigrp_configuration_list)
    print("Applying EIGRP Configuration")
    print(apply)
elif apply_configuration != 'yes':
    print("Rejecting EIGRP Configuration")

print("\nConfiguration Script Done.")
