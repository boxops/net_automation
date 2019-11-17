from device_info import csr1000v2
from ncclient import manager
from pprint import pprint
import xmltodict

netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet1</name>
    </interface>
  </interfaces>
</filter>
"""

m = manager.connect(host=csr1000v2["host"],
                    port=csr1000v2["port"],
                    username=csr1000v2["username"],
                    password=csr1000v2["password"],
                    hostkey_verify=False)

interface_netconf = m.get_config("running", netconf_filter)
interface_python = xmltodict.parse(interface_netconf.xml)["rpc-reply"]["data"]
pprint(interface_python["interfaces"]["interface"]["name"]["#text"])
