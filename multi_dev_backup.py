import json
import netmiko
import os

# Customise variables before running the script
# ---------------------------------------------------------------------------------------------------------
commands = ["sh run", "sh vlan", "sh logging"]  # cisco ios commands to execute and write output into a file
operating_system = "Windows"  # choose the operating system the script is running on: Windows, Linux or Mac
ping_count = str(4)  # alter the number of pings to speed up or slow down the script
# ---------------------------------------------------------------------------------------------------------

devices_file = input(str("Enter the name of the devices file: "))  # input the name of the file to read from
failed_ping = []  # collection of IP addresses that the script failed to ping
failed_ssh = []  # collection of IP addresses that the script failed to connect to

try:
    with open(devices_file, "r") as js:  # get the content of the file provided by the user
        devices_file = json.load(js)  # open and convert file to json format
except IOError:
    print("Config file is broken or name entered incorrectly")
    print("Program will quit")
    exit()  # end script if file was not found


def multi_dev():
    for i in range(0, len(devices_file["device"]), 1):  # get the length of a value pair and loop through the dictionary
        # ping '-n' option on Windows; ping '-c' option on Linux and Mac
        ping = None
        if operating_system == "Windows":  # ping command option changes based on different operating systems
            ping = os.system("ping -n " + ping_count + " " + devices_file["ip"][i])
        elif operating_system == "Linux" or operating_system == "Mac":
            ping = os.system("ping -c " + ping_count + " " + devices_file["ip"][i])
        else:
            print("Unknown Operating System. Exiting script.")
            exit()  # end script if operating system variable is not valid

        if ping == 0:  # if ping was successful: try connecting to the device
            print(" ")
            print("Pinged Device: ", devices_file["ip"][i])

            # ssh "username"@"ip" -c aes128-cbc (Windows and Linux ssh command used to force exchange a private ssh key)
            try:  # values from the dictionary are passed to netmiko for establishing an ssh connection
                session = netmiko.ConnectHandler(device_type=devices_file["device"][i], host=devices_file["ip"][i],
                                                 username=devices_file["usr"][i], password=devices_file["pw"][i],
                                                 secret=devices_file["en"][i], verbose=True)
            except netmiko.ssh_exception.AuthenticationException:  # incorrect ssh credentials
                print("SSH Connection Unsuccessful")
                failed_ssh.append(devices_file["ip"][i])  # if connection fails: append IP to a variable for later use
                continue  # if connection failed: print(failed connection) and continue to the next device
            except netmiko.ssh_exception.NetMikoTimeoutException:  # ssh connection timeout
                print("SSH Connection Timed Out")
                failed_ssh.append(devices_file["ip"][i])
                continue
            except ValueError:  # incorrect values given, such as IP address
                print("Either IP or Host must be set")
                failed_ssh.append(devices_file["ip"][i])
                continue

            for command in commands:  # loop through a list of commands
                file_name = str(devices_file["ip"][i] + "_" + devices_file["device"][i] +
                                "_" + '_'.join(command.split(' ')[::1]) + "_conf.txt")
                file = open(file_name, "w+")  # open a file to write to, create one if it doesn't exist
                output = session.send_command(command)  # sends a command through the current session
                print(f"Device type: {devices_file['device'][i]} \n")
                print(f"Writing command output into a file: " + command)
                print(output)
                file.write(output)  # appends the output to the open file
                print("\nSuccessfully saved " + command + " command output to '" + file_name + "' file!")
                file.close()  # (important) close file

            session.disconnect()  # (important) close connection

        else:
            print(" ")
            print("Failed to Ping Device: ", devices_file["ip"][i])
            failed_ping.append(devices_file["ip"][i])  # if ping fails: append IP to a variable for the report
            continue  # if the ping fails: carry on pinging other devices without interruption


multi_dev()

# print a report of failed pings and ssh connections
if len(failed_ping) != 0:
    print(" ")
    print("------------- Ping Report -------------")
    print("Failed to Ping device(s): ")
    print(failed_ping)
    pings = open("failed_pings.txt", "w+")  # write the failed pings to a file
    for p in failed_ping:
        pings.write(p)
        pings.write(',')
    pings.close()
elif len(failed_ping) == 0:
    print(" ")
    print("------------- Ping Report -------------")
    print("All devices were Pinged successfully!")

if len(failed_ssh) != 0:
    print(" ")
    print("------------- SSH Report -------------")
    print("Failed to Connect to device(s): ")
    print(failed_ssh)
    connections = open("failed_connections.txt", "w+")  # write the failed connections to a file
    for s in failed_ssh:
        connections.write(s)
        connections.write(',')
    connections.close()
elif len(failed_ssh) == 0:
    print(" ")
    print("------------- SSH Report -------------")
    print("All devices were Connected successfully!")
