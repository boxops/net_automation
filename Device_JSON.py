import json
import netmiko
import telnetlib

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

    elif usr_res == "N":
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


def start_session(dev, con_type, dev_no):
    # Con_type to decide whether to use telnet or ssh
    while True:
        if con_type == "T":
            print("Connecting via Telnet")
            session = telnetlib.Telnet(dev["ip"][dev_no])
            session.read_until(b'Username: ')
            session.write((dev["usr"][dev_no] + "\n").encode('ascii'))
            session.read_until(b'Password: ')
            session.write((dev["pw"][dev_no] + "\n").encode('ascii'))
            session.write(b'enable')
            session.write((dev["en"][dev_no] + "\n").encode('ascii'))
            session.write(b'\n')
            prompt = session.read_very_eager()
            print(prompt)
            print("Warning! Telnet is an unsecure protocol!")
            while True:
                decision = input(str("Would you like to use SSH to connect instead (y/n)? "))
                if decision == "y":
                    con_type = "S"
                    break
                if decision == "n":
                    print("Telnet is unsupported, shutting down")
                    quit()
                else:
                    continue

        elif con_type == "S":
            device = 'cisco_ios'
            print("Connecting to device(s) via SSH")
            session = netmiko.ConnectHandler(device_type=device, host=dev["ip"][dev_no], username=dev["usr"][dev_no],
                                             password=dev["pw"][dev_no], secret=dev["en"][dev_no])
            session.find_prompt() + "\n"
            print("Device found and successfully connected with SSH!")
            session.enable()
            print("Enabled Privileged Mode")
            print("Device Connected")
            return session
