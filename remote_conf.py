# Python network automation tool for establishing ssh connections and pulling output from devices
from netmiko import ConnectHandler  # import ConnectHandler function to create an ssh connection
from getpass import getpass  # import getpass function to prompt the user for password
import napalm
import json  # import json library to work with dictionaries

# device_type = []  # create empty lists
# host = []
# username = []
# password = []
# port = []
# secret = []

# device = {"device_type": device_type, "host": host, "username": username, "password": password, "port": port}

with open("device.json", "r") as f:  # read device info from a file
    # node = f.read()
    device = json.load(f)

# device_type.append(input(str("Enter device type : ")))
# host.append(input(str("Enter device IP address : ")))
# username.append(str(input("Enter device username : ")))
# password.append(getpass("Enter device ssh password : "))
# port.append(input(str("Enter device port : ")))
# secret.append(getpass("Enter device enable password : "))

net_connect = ConnectHandler(**device)  # Initialize the ssh connection to the device
print("Connection Successful")


def main_menu():
    option = None
    print(" ")
    print("Configuration Menu.")
    print(" ")
    print("1 - Show Interfaces")
    print("2 - Show Running-config")
    print("3 - Show IP Routes")
    print("4 - Show VLANs")
    print("5 - Show Syslog messages")
    print("6 - Show iOS Version")
    print("7 - Backup Device Configuration")
    print("8 - Compare Running-config to Startup-config")
    print("9 - Compare Running-config to Backup-config")
    print("0 - Exit from Configuration Menu")
    loop = 1
    while loop == 1:  # while loop checks for correct user input
        try:
            option = int(input("\n Choose your option: "))
            if 0 <= option <= 9:  # valid values are ranged from 0 to 9
                loop = 0
            else:
                print("\n The value has to be in between 0 and 9")
        except ValueError:
            print("\n Invalid value. Try Again.")
    return option


def run_options():
    loop = True
    while loop:
        choice = main_menu()
        if choice == 1:  # show interfaces
            output = net_connect.send_command("show ip int b")
            print("Done Showing IP Int Brief")
            print(output)
        elif choice == 2:  # show running-config
            output = net_connect.send_command("show run")
            print("Done Showing Running-config")
            print(output)
        elif choice == 3:  # show routing table
            output = net_connect.send_command("show ip route")
            print("Done Showing IP Route")
            print(output)
        elif choice == 4:  # show vlans
            output = net_connect.send_command("show vlans")
            print("Done Showing VLANs")
            print(output)
        elif choice == 5:  # show syslog
            output = net_connect.send_command("show logging")
            print("Done Showing Syslog")
            print(output)
        elif choice == 6:  # show ios version
            output = net_connect.send_command("show version")
            print("Done Showing iOS Version")
            print(output)
        elif choice == 7:  # backup running-config
            output = net_connect.send_command("wr")
            print("Done Backing up Device Configurations")
            print(output)
        elif choice == 8:  # compare the running configuration of a network device with the start-up configuration
            output = net_connect.send_command(
                "show archive config differences system:running-config nvram:startup-config")
            print("Done Comparing Running-config to Startup-config")
            print(output)
            # (+) means that the configuration line exists in the startup-config but not in the running-config
            # (-) means that the configuration line exists in running-config but not in startup-config
        elif choice == 9:  # compare the running configuration of a network device with a local offline version
            output = net_connect.send_command("show archive config differences system:running-config http:[file2path]")
            print("Done Comparing Running-config to Backup-config")
            print(output)
        elif choice == 0:  # end script
            loop = False


run_options()

print("Config script done!")
print("Connection Closed")
