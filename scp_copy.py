import os


def scp_copy():
    username = input(str("Select Source username : "))
    ip_address = input(str("Select Source IP Address : "))
    absolute_path = input(str("Input the Absolute Path to the file : "))
    backup = input(str("Name the File to store : "))
    # example -> scp C:\Users\olahb\Documents\backup.txt admin@192.168.181.129:flash:backup
    scp = "scp " + absolute_path + " " + username + "@" + ip_address + ":" + "flash:" + backup
    os.system(scp)
    return backup
