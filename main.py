import time
import Device_JSON
import Parameter_Monitoring
from threading import Thread as Daemon
from netmiko import file_transfer


def main_menu(session):
    #  Function to create and display the main menu options to the user
    option = None
    print("____________________________________________________________________________________________")
    print("                          Welcome to the Configuration Menu                                 ")
    print("                          Device type: " + session.device_type)
    print("                          IP Address: " + session.host)
    print("--------------------------------------------------------------------------------------------")
    print("                         Please select an option listed below:                              ")
    print("____________________________________________________________________________________________")
    print("1 - Show Interfaces                             2 - Show Running-config")
    print("3 - Backup Device Configuration                 4 - Compare Running-config to Startup-config")
    print("5 - Compare Running-config to Backup-config     6 - Connect to a different device")
    print("7 - Retrieve Syslog from Database               8 - Retrieve IOS Version from Database")
    print("9 - Retrieve Routes from Database               10 - Retrieve VLANs from Database")
    print("                        0 - Exit from Configuration Menu                         ")
    loop = True
    while loop:  # while loop checks for correct user input
        try:
            option = int(input("\n Choose your option: "))
            if 0 <= option <= 10:  # valid values are ranged from 0 to 10
                loop = False
            else:
                print("\n The value has to be in between 0 and 10")
        except ValueError:
            print("\n Invalid value. Try Again.")
    return option


def run_options(session):
    loop = True
    while loop:
        choice = main_menu(session)
        if choice == 1:  # show interfaces
            output = session.send_command("show ip int b")
            print("Done Showing IP Int Brief")
            print(output)
        elif choice == 2:  # show running-config
            output = session.send_command("show run")
            print("Done Showing Running-config")
            print(output)
        elif choice == 3:  # backup running-config
            output = session.send_command("wr")
            print("Done Backing up Device Configurations")
            print(output)
        elif choice == 4:  # compare the running configuration of a network device with the start-up configuration
            output = session.send_command(
                "show archive config differences system:running-config nvram:startup-config")
            print("Done Comparing Running-config to Startup-config")
            print(output)
            # (+) means that the configuration line exists in the startup-config but not in the running-config
            # (-) means that the configuration line exists in running-config but not in startup-config
        elif choice == 5:  # compare the running configuration of a network device with a local offline version
            select = input(str("Select or Copy a backup file to flash: ? (S) or (C) "))
            if select == "S":
                backup = input(str("Input the Name of the backup file stored in flash: "))
                output = session.send_command("show archive config differences system:running-config flash:" + backup)
                print("Done Comparing Running-config to Backup-config")
                print(output)
            elif select == "C":  # use netmiko file_transfer function to copy a backup file to flash
                source_file = input(str("Enter the Name of the backup file to copy: "))
                dest_file = input(str("Enter the Name of the backup file to store: "))
                scp = file_transfer(session,
                                    source_file=source_file,
                                    dest_file=dest_file,
                                    file_system='flash:',
                                    direction='put',
                                    overwrite_file=True)
                print(scp)
                print("Comparing the running configuration with a local offline version")
                output = session.send_command("show archive config differences system:running-config flash:" + dest_file)
                print("Done Comparing Running-config to Backup-config")
                print(output)
        elif choice == 6:  # Switch session between devices
            session.disconnect()  # disconnect from the original device
            Parameter_Monitoring.thread_flag = 1  # Kill original thread
            j = -1  # Start index position < 0
            print("Devices in list")
            for i in dev["ip"]:  # Get all IPs of devices in list
                j += 1  # Increase index position represented
                print(str(j) + " : " + i)  # Print Device IP and index position
            decision = input(str("Please enter the number of the device IP you would like to connect to: "))
            result = int(decision)  # Convert the device chosen to index position in list
            new_condition = input(str("Please choose SSH (S) or Telnet (T): "))  # SSH or telnet user input
            session = Device_JSON.start_session(dev, new_condition, result)  # Open a new session to device
            Parameter_Monitoring.thread_flag = 0  # Allow new thread
            background_ps(session)  # Create a new background process to monitor variables
            # New session created

        elif choice == 7:
            # Print out the system log
            print(Parameter_Monitoring.get_syslog(session)[0])
            time.sleep(5)

        elif choice == 8:
            # Print out the IOS version
            print(Parameter_Monitoring.get_version(session)[0])
            time.sleep(5)

        elif choice == 9:
            # Print out the routing table
            print(Parameter_Monitoring.get_route(session)[0])
            time.sleep(5)

        elif choice == 10:
            #  Print out the vlan table
            print(Parameter_Monitoring.get_vlan(session)[0])
            time.sleep(5)

        elif choice == 0:  # end script
            Parameter_Monitoring.thread_flag = 1  # Kill daemon thread
            session.disconnect()  # Disconnect from currently connected device
            exit(-1)


def background_ps(session):
    time_thread = Daemon(target=Parameter_Monitoring.tasks, args=(session, 1800))
    # Create new thread for every 30 minutes
    time_thread.start()  # Start the thread
    return time_thread  # Return the thread


dev = Device_JSON.var_def()  # Set variables and retrieve json file
condition = input(str("Please select SSH (S) or Telnet(T): "))  # Choose telnet or ssh protocol
session = Device_JSON.start_session(dev, condition, 0)  # Initially connect to first device in json
background_ps(session)  # Start monitoring parameters
run_options(session)  # Run the main menu and pass the session variable
