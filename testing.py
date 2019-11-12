# Python network automation tool for establishing ssh connections and pulling output from Cisco IOS
# Append the output to a file like so: python netmiko_print_conf.py >> ios_conf

from netmiko import ConnectHandler  # Import ConnectHandler function to read the dictionary and create an ssh connection
from getpass import getpass  # Import getpass function to prompt the user for password
import json

device_ls = []
ip_ls = []
usr_ls = []
pw_ls = []
en_ls = []


def var_def():
    # Define variables to be used in the login process
    usr_res = input(str("Enter the name of the device storage file (.json) or enter N to create a new file: "))
    if usr_res != "N":
        try:
            with open(usr_res, "r") as js:
                dev_node = json.load(js)

        except IOError:
            print("Config file is broken or name entered incorrectly")
            print("Program will quit")
            exit()

    elif usr_res == "N" or "n":
        # if login info doesn't exist create it
        x = True
        print("Creating new configuration file.")
        usr_res = input(str("Enter a name for this device configuration file: "))
        if usr_res.endswith(".json"):
            print("File created")
        else:
            usr_res = usr_res + ".json"
        while x:
            device_ls.append(input(str("Enter a device name to identify this device: ")))
            ip_ls.append(input(str("Enter a device IP: ")))
            usr_ls.append(input(str("Enter a username: ")))
            pw_ls.append(input(str("Enter a password for VTY: ")))
            en_ls.append(input(str("Enter a enable password: ")))
            add_dev = input(str("Would you like to add more devices [Y/N]? "))
            if add_dev == "Y":
                continue
            if add_dev == "N":
                with open(usr_res, "w") as node:
                    dev_node = {"device": device_ls, "ip": ip_ls, "usr": usr_ls, "pw": pw_ls, "en": en_ls}
                    json.dump(dev_node, node)
                break

    return dev_node

#password = getpass("Enter csr1000v ssh password : ")
#secret = getpass("Enter csr1000v enable password : ")


net_connect = ConnectHandler(**var_def(dev_node)  # Initialize the connection to the router
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
    print(" ")
    # print("Press any Key to roll back : " # option to roll back if part of the script fails
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
        if choice == 1:
            show_int()
        elif choice == 2:
            show_run()
        elif choice == 3:
            show_ip_route()
        elif choice == 4:
            show_vlans()
        elif choice == 5:
            show_syslog()
        elif choice == 6:
            show_ios_version()
        elif choice == 7:
            backup_dev_conf()
        elif choice == 8:
            compare_run_start()
        elif choice == 9:
            compare_run_back()
        elif choice == 0:
            loop = False


def show_int():  # choice 1
    output = net_connect.send_command("show ip int b")
    print(output)
    print("Done Showing IP Int Brief")


def show_run():  # choice 2
    output = net_connect.send_command("show running-config")
    print(output)
    print("Done Showing Running-config")


def show_ip_route():  # choice 3
    output = net_connect.send_command("show ip route")
    print(output)
    print("Done Showing IP Route")


def show_vlans():  # choice 4
    output = net_connect.send_command("show vlans")
    print(output)
    print("Done Showing VLANs")


def show_syslog():  # choice 5
    output = net_connect.send_command("show logging")
    print(output)
    print("Done Showing Syslog")


def show_ios_version():  # choice 6
    output = net_connect.send_command("show version")
    print(output)
    print("Done Showing iOS Version")


def backup_dev_conf():  # choice 7
    output = net_connect.send_command("wr")
    print(output)
    print("Done Backing up Device Configurations")


def compare_run_start():  # choice 8
    output = net_connect.send_command("show archive config differences system:running-config nvram:startup-config")
    print(output)
    print("Done Comparing Running-config to Startup-config")


def compare_run_back():  # choice 9
    output = net_connect.send_command("show archive config differences system:running-config http:[file2path]")
    print(output)
    print("Done Comparing Running-config to Backup-config")


run_options()

print("Config script done!")
print("Connection Closed")

