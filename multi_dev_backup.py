import json
import netmiko
import os

devices_file = input(str("Enter the name of the devices file : "))
backup = "sh run"
failed_ping = []
failed_ssh = []
ping_count = str(4)

try:
    with open(devices_file, "r") as js:
        devices_file = json.load(js)  # open and convert file to json format
except IOError:
    print("Config file is broken or name entered incorrectly")
    print("Program will quit")
    exit()  # end script if file was not found


def multi_dev():
    for i in range(0, len(devices_file["device"]), 1):
        ping = os.system("ping -n " + ping_count + " " + devices_file["ip"][i])  # ping '-n' on Windows, '-c' on Linux

        if ping == 0:
            print(" ")
            print("Pinged Device: ", devices_file["ip"][i])

            # ssh "username"@"ip" -c aes128-cbc (Windows and Linux ssh command used to force exchange a private ssh key)
            try:  # if ping was successful: try connecting to the device
                session = netmiko.ConnectHandler(device_type=devices_file["device"][i], host=devices_file["ip"][i],
                                                 username=devices_file["usr"][i], password=devices_file["pw"][i],
                                                 secret=devices_file["en"][i])
            except netmiko.ssh_exception.AuthenticationException:
                print("SSH Connection Unsuccessful")
                failed_ssh.append(devices_file["ip"][i])
                continue  # if connection failed: print(failed connection) and continue
            except netmiko.ssh_exception.NetMikoTimeoutException:
                print("SSH Connection Timed Out")
                failed_ssh.append(devices_file["ip"][i])
                continue
            except ValueError:
                print("Either ip or host must be set")
                failed_ssh.append(devices_file["ip"][i])
                continue

            # if the connection was successful: print(successful connection)
            print("SSH Connection Successful")
            file_name = str(devices_file["ip"][i] + "_" + devices_file["device"][i] + "_backup_conf.txt")
            file = open(file_name, "w+")
            output = session.send_command(backup)
            print(f"Device type: {devices_file['device'][i]} \n\n")
            print(output)
            file.write(output)
            session.disconnect()  # (important) close connection
            file.close()

        else:
            print(" ")
            print("Failed to Ping Device: ", devices_file["ip"][i])
            failed_ping.append(devices_file["ip"][i])
            continue  # if the connection failed: carry on connecting to other devices without interruption


multi_dev()

if len(failed_ping) != 0:
    print(" ")
    print("Failed to ping device(s): ")
    print(failed_ping)
elif len(failed_ping) == 0:
    print(" ")
    print("All devices were pinged successfully!")

if len(failed_ssh) != 0:
    print(" ")
    print("Failed to connect to device(s): ")
    print(failed_ssh)
elif len(failed_ssh) == 0:
    print(" ")
    print("All devices were connected successfully!")
