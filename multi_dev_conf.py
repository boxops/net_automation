from netmiko import Netmiko
from getpass import getpass

cisco1 = {
    "host": "cisco1.twb-tech.com",
    "username": "pyclass",
    "password": password,
    "device_type": "cisco_ios"
    "secret": secret,
}

cisco2 = {
    "host": "cisco2.twb-tech.com",
    "username": "pyclass",
    "password": password,
    "device_type": "cisco_ios",
}

nxos1 = {
    "host": "nxos1.twb-tech.com",
    "username": "pyclass",
    "password": password,
    "device_type": "cisco_nxos",
}

srx1 = {
    "host": "srx1.twb-tech.com",
    "username": "pyclass",
    "password": password,
    "device_type": "juniper_junos",
}

password = getpass("Enter " + device_name + "password : ")
secret = getpass("Enter " + device_name + " enable secret : ")


for device in (cisco1, cisco2, nxos1, srx1):
    net_connect = Netmiko(**device)
    print(net_connect.find_prompt())


def main_menu():
    global option
    print("Configuration Menu.")
    print(" ")
    print("1 - Show Interfaces")
    print("2 - Show Running-config")
    print("3 - Show IP Routes")
    print("4 - Backup Device Configurations")
    print("5 - Simultaneous Configuration of Multiple Devices")
    print(" ")
    # print("Press any Key to roll back : " # option to roll back if part of the script fails
    loop = True
    while loop:  # while loop prevents the program from crashing
        option = None
        option = input("Enter Option").strip()
    if option == str:
        loop = False
        return
    elif option == int:
        if 1 <= option <= 5:  # input value 1, 2, 3, 4, 5
            loop = False
            return option
        else:
            print("Invalid input.")
    else:
        pass


def run_options():
    loop = 1
    while loop == 1:
        choice = main_menu()
        if choice == 1:
            ShowInt()
        elif choice == 2:
            ShowRun()
        elif choice == 3:
            ShowIPRoute()
        elif choice == 4:
            BackupDev()
        elif choice == 5:
            SimConfAll()
        else:
            loop = 0


