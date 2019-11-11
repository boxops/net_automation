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
    # output = net_connect.send_command("show ip int b")
    # print(output)
    print("Showing Interfaces")


def show_run():  # choice 2
    # output = net_connect.send_command("show run")
    # print(output)
    print("Showing Running-config")


def show_ip_route():  # choice 3
    # output = net_connect.send_command("show ip route")
    # print(output)
    print("Showing Routing Table")


def show_vlan():  # choice 4
    # output = net_connect.send_command("show vlan")
    # print(output)
    print("Showing VLANs")


def show_syslog():  # choice 5
    # output = net_connect.send_command("show syslog")
    # print(output)
    print("Showing Syslog")


def show_ios_version():
    # output = net_connect.send_command("show version")
    # print(output)
    print("Showing iOS Version")


def backup_dev_conf():
    # output = net_connect.send_command("copy run start")
    # print(output)
    print("Backed up Device Configurations")


def compare_run_start():
    # output = net_connect.send_command(" ")
    # print(output)
    print("Comparing Running-config to Startup-config")


def compare_run_back():
    # output = net_connect.send_command(" ")
    # print(output)
    print("Comparing Running-config to Backup-config")


run_options()

print("Config script done!")
print("Connection Closed")
