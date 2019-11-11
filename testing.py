from netmiko import ConnectHandler  # Import ConnectHandler function to read the dictionary and create an ssh connection
from getpass import getpass  # Import getpass function to prompt the user for password

password = getpass("Enter csr1000v ssh password : ")
secret = getpass("Enter csr1000v enable password : ")

csr1000v = {
    "device_type": "cisco_ios",
    "host": "",
    "username": "admin",
    "password": password,  # getpass() function prompts for password
    "port": 22,  # optional, defaults to 22
    # "secret": "class", # optional, enable if privilege 0
}

net_connect = ConnectHandler(**csr1000v)  # Initialize the connection to the router
print("Connection Successful")


def compare_run_start():
    sh_run = []
    output = net_connect.send_command("sh run")
    sh_run.append(output)
    print(sh_run)
