from netmiko import ConnectHandler
import netaddr
import re

device = {
    "device_type": "cisco_ios",
    "host": "192.168.126.138",
    "username": "admin",
    "password": "Cisco123",
    "verbose": True,
    "port": "22"
}

session = ConnectHandler(**device)

eigrp_configuration_list = []
interface_names = []
interface_list = []
eigrp_networks = []
wildcards = []
networks = []
netmasks = []


def eigrp_config():
    # --------- Pre-calculation section ---------

    # get interface names
    interfaces = session.send_command("show ip int b")
    for line in interfaces.split("\n"):
        interface_names.append(line.split(" ", 1)[0])
    # interface_names.pop(0)  # remove interface header (not necessary)

    # get cidr connected networks from the routing table
    connected_routes = session.send_command("show ip route | include C")
    connected_networks = re.findall(r'[0-9]+(?:\.[0-9]+){3}/[0-9]+', connected_routes)
    # regex explanation: '+' one and more  match, [0-9] character range, {3} match the preceding expression 3 times
    # '\.' matches a dot escaped by '\', (?: ... ) match everything enclosed, '/' matches the subnet mask identifier

    # get network, netmask and wildcard from cidr using netaddr library
    for item in connected_networks:
        network = str(netaddr.IPNetwork(item).network)
        networks.append(network)
        netmask = str(netaddr.IPNetwork(item).netmask)
        netmasks.append(netmask)
        wildcard = str(netaddr.IPNetwork(item).hostmask)
        wildcards.append(wildcard)

    # construct networks with hostmasks for eigrp network config, e.g. '192.168.1.0 0.0.0.255'
    for item in range(0, len(networks), 1):
        eigrp = str(networks[item] + " " + wildcards[item])
        eigrp_networks.append(eigrp)

    # --------- User Interaction Section ---------

    # prompt the user for an eigrp identifier
    eigrp_identifier = input(str("\nEnter a unique identifier number for EIGRP: "))

    loop = True
    while loop:
        for item in range(1, len(interface_names), 1):  # list interface names to user
            print(item, interface_names[item])
        try:
            eigrp_passive = int(input("\nEnter passive interface number(s) for EIGRP from the list above, or press any "
                                      "other key to skip: "))
            if 1 <= eigrp_passive <= len(interface_names):  # if the input is in between 1 and the length of interfaces
                try:
                    if interface_names[eigrp_passive]:  # if the interface exists
                        interface_list.append(eigrp_passive)  # store the input in a list
                except IndexError:
                    print("Number is outside of scope. Try again.")
        except ValueError:
            loop = False

    # construct and display eigrp summary to the user before applying the configuration
    print("\n-----------------------------------------------")
    print("EIGRP Configuration for device: " + session.host)
    print("-----------------------------------------------")
    eigrp_configuration_list.append("router eigrp " + eigrp_identifier)
    print("router eigrp " + eigrp_identifier)
    eigrp_configuration_list.append("no auto-summary")
    print("no auto-summary")
    for i in interface_list:  # create eigrp passive-interface commands
        eigrp_configuration_list.append("passive-interface " + interface_names[i])
        print("passive-interface " + interface_names[i])
    for j in eigrp_networks:  # create eigrp network commands
        eigrp_configuration_list.append("network " + j)
        print("network " + j)
    print("-----------------------------------------------")

    # applying the configuration can be rejected by the user if desired
    apply_configuration = input("\nApply EIGRP configuration? 'yes' to apply, or press any other key to cancel: ")

    if apply_configuration == 'yes':  # user must type 'yes' to apply eigrp configuration
        apply = session.send_config_set(eigrp_configuration_list)
        print("Applying EIGRP Configuration")
        print(apply)
    elif apply_configuration != 'yes':
        print("Rejecting EIGRP Configuration")

    session.disconnect()  # end session
    print("\nConfiguration Script Done.")


eigrp_config()
