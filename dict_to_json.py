import json

csr1000v = {
    "device_type": "cisco_ios",
    "host": "40.120.49.51",
    "username": "csr1",
    "password": "password",
    "port": 22,
}

app_json = json.dumps(csr1000v)
print(app_json)
