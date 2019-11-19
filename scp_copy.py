import os
from device_info import csr1000v1


def scp_copy():
    username = csr1000v1["username"]
    host = csr1000v1["host"]
    absolute = input("Absolute Path to the file: ")
    copy_name = input("Name the File to store in flash: ")
    password = csr1000v1["password"]
    # example -> scp C:\Users\olahb\Documents\backup.txt admin@192.168.181.129:flash:backup
    scp = "scp %s %s@%s:flash:%s" % (absolute, username, host, copy_name)

    print(scp)
    os.system(scp)


scp_copy()
