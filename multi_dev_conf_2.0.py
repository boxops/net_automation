import json
import netmiko
from netmiko import ConnectHandler
import os

devices_file = input(str("Enter the name of the devices file : "))
backup = "sh run"

try:
    with open(devices_file, "r") as js:
        devices_file = json.load(js)
except IOError:
    print("Config file is broken or name entered incorrectly")
    print("Program will quit")
    exit()


def multi_dev():
    for i in range(0, len(devices_file["device"]), 1):
        file_name = str(devices_file["device"][i] + '_backup_conf')
        file = open(file_name, 'w+')
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ping = os.system('ping -n 4 ' + devices_file["ip"][i])  # ping device
        if ping == 0:
            print(" ")
            print("Pinged Device: ", devices_file["ip"][i])
            # file.write("IP address: " + device["host"] + "\n")

            try:  # if ping was successful: try connecting to the device
                session = netmiko.ConnectHandler(device_type=devices_file["device"][i], host=devices_file["ip"][i],
                                                 username=devices_file["usr"][i], password=devices_file["pw"][i],
                                                 secret=devices_file["en"][i])
            except netmiko.ssh_exception.AuthenticationException:
                print("SSH Connection Unsuccessful")
                continue  # if connection failed: print(failed connection) and continue
            except ValueError:
                print("Either ip or host must be set")
                continue

            # if the connection was successful: print(successful connection)
            print("SSH Connection Successful")
            output = session.send_command(backup)
            print(f"Device type: {devices_file['device'][i]} \n\n")
            print(output)
            file.write(output)
            session.disconnect()  # (important) close connection

        else:
            print(" ")
            print("Failed to Ping Device: ", devices_file["ip"][i])
            continue  # if the connection failed: carry on connecting to other devices without interruption
        file.close()


multi_dev()
