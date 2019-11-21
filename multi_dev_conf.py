import netmiko  # import connection libraries and device_info.py file
from netmiko import ConnectHandler
import device_info
import socket
import os


# (optional) prompt the user for "backup multiple configuration" option in the main file
# or run the "multi_dev_conf.py" file separately
# (optional) print a list of devices from device_info.py file to choose from


def multi_dev():
    devices_list = [device_info.csr1000v1, device_info.csr1000v2]
    config_commands = "sh run"

    file = open('backup_conf', 'w+')
    for device in devices_list:  # for device in (chosen devices): connect to device
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ping = os.system('ping -n 1 ' + device["host"])  # ping device
        if ping == 0:
            print(" ")
            print("Pinged Device: ", device["host"])
            file.write("IP address: " + device["host"] + "\n")

            try:  # if ping was successful: try connecting to the device
                session = ConnectHandler(**device)
            except netmiko.ssh_exception.AuthenticationException:
                print("SSH Connection Unsuccessful")
                continue  # if connection failed: print(failed connection) and continue
            except ValueError:
                print("Either ip or host must be set")
                continue

            # if the connection was successful: print(successful connection)
            print("SSH Connection Successful")
            output = session.send_command(config_commands)
            print(f"Device type: {device['device_type']} \n\n")
            print(output)
            file.write(f"Device type: {device['device_type']} \n\n")  # backup running configuration to a file
            file.write(output)
            file.write("\n")
            session.disconnect()  # (important) close connection
        else:
            print("Failed to Ping Device: ", device["host"])
            continue  # if the connection failed: carry on connecting to other devices without interruption
    file.close()

# (optional) print(list of failed devices to connect)
# (optional) print(list of failed devices to backup)


multi_dev()
