from device_info import csr1000v2
from ncclient import manager

if __name__ == '__main__':
    with manager.connect(host=csr1000v2["host"],
                         port=csr1000v2["port"],
                         username=csr1000v2["username"],
                         password=csr1000v2["password"],
                         hostkey_verify=False) as m:

        print("Here are the NETCONF Capabilities")
        for capability in m.server_capabilities:
            print(capability)
