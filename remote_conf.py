# Python network automation tool for establishing ssh connections and pulling output from Cisco IOS
# Append the output to a file like so: python netmiko_print_conf.py >> ios_conf

from netmiko import ConnectHandler  # Import ConnectHandler function to read the dictionary and create an ssh connection
from getpass import getpass  # Import getpass function to prompt the user for password

password = getpass("Enter csr1000v ssh password : ")
secret = getpass("Enter csr1000v enable password : ")

csr1000v = {
    "device_type": "cisco_ios",
    "host": "40.120.49.51",
    "username": "csr1",
    "password": password,  # getpass() function prompts for password
    "port": 22,  # optional, defaults to 22
    # "secret": "class", # optional, enable if privilege 0
}

net_connect = ConnectHandler(**csr1000v)  # Initialize the connection to the router
print("Connection Successful")


def main_menu():
    option = None
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
            show_vlan()
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
    print("Done Showing IP int brief")
    print(output)


def show_run():  # choice 2
    output = net_connect.send_command("show run")
    print("Done Showing Running-config")
    print(output)


def show_ip_route():  # choice 3
    output = net_connect.send_command("show ip route")
    print("Done Showing IP Route")
    print(output)


def show_vlan():  # choice 4
    output = net_connect.send_command("show vlan")
    print("Done Showing VLANs")
    print(output)


def show_syslog():  # choice 5
    output = net_connect.send_command("show syslog")
    print("Done Showing Syslog")
    print(output)


def show_ios_version():  # choice 6
    output = net_connect.send_command("show version")
    print("Done Showing iOS Version")
    print(output)


def backup_dev_conf():  # choice 7
    output = net_connect.send_command("copy run start")
    print("Done Backing up Device Configurations")
    print(output)


def compare_run_start():  # choice 8
    sh_run = []
    output = net_connect.send_command("sh run")
    sh_run.append(output)

    sh_start = open("router_startup_conf").read()

    for runline in sh_run:
        for startline in sh_start:
            if runline != startline:
                print("Unmatched config at line : " + sh_run[runline] + "!")
                print(runline)
                print(startline)

    print("Done Comparing Running-config to Startup-config")


def compare_run_back():  # choice 9
    sh_run = []
    output = net_connect.send_command("sh run")
    sh_run.append(output)

    sh_back = open("router_backup_conf").read()

    for runline in sh_run:
        for backline in sh_back:
            if runline != backline:
                print("Unmatched config at line : " + sh_run[runline] + "!")
                print(runline)
                print(backline)
    print("Done Comparing Running-config to Backup-config")


run_options()

print("Config script done!")
print("Connection Closed")
