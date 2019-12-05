import sqlite3
import os
# Module to allow SQLLite Database connections


def sql_create():
    result = sqlite3.connect('DeviceMonitor.db', check_same_thread=False)
    sql_create_table = """CREATE TABLE IF NOT EXISTS Device_Info_Table(
                                        Device_Name text PRIMARY KEY,
                                        Route text,
                                        VLAN text,
                                        IOSVersion real,
                                        log_msg text);"""
    exe = result.cursor()
    exe.execute(sql_create_table)
    result.commit()
    return result


ExDB = os.path.exists("DeviceMonitor.db")
if not ExDB:
    database = sql_create()

else:
    database = sqlite3.connect('DeviceMonitor.db', check_same_thread=False)  # Connect to database


dbcsr = database.cursor()  # Create cursor to execute commands


def commit_changes():
    database.commit()


def retrieve_route(device):
    # Function that retrieves the routes from the DB
    data = dbcsr.execute('SELECT Route FROM Device_Info_Table WHERE Device_Name = ?'
                         , (device,))
    res = data.fetchall()
    return res


def log_route(device, routes):
    # Function for logging routes into the DB
    dbcsr.execute('INSERT OR IGNORE INTO Device_Info_Table (Device_Name, Route) VALUES (?, ?); ', (device, routes))
    dbcsr.execute('UPDATE Device_Info_Table SET Route=? WHERE Device_Name=?;', (routes, device))
    commit_changes()

def log_vlan(device, vlan_db):
    # Function for logging VLANs into DB
    dbcsr.execute('INSERT OR IGNORE INTO Device_Info_Table (Device_Name, VLAN) VALUES (?, ?); ', (device, vlan_db))
    dbcsr.execute('UPDATE Device_Info_Table SET VLAN=? WHERE Device_Name=?;', (vlan_db, device))
    commit_changes()


def get_vlans(device):
    # Function for retrieving device VLANs from DB
    data = dbcsr.execute('SELECT VLAN FROM Device_Info_Table WHERE Device_Name = ?', (device,))
    res = data.fetchall()
    return res


def sys_logger(device, log_msg):
    # Function for logging messages into DB
    dbcsr.execute('INSERT OR IGNORE INTO Device_Info_Table (Device_Name, log_msg) VALUES (?, ?); ',
                  (device, log_msg))
    dbcsr.execute('UPDATE Device_Info_Table SET log_msg=? WHERE Device_Name=?;', (log_msg, device))
    commit_changes()


def log_retrieve(device):
    # Function for retrieving messages from DB
    data = dbcsr.execute('SELECT log_msg FROM Device_Info_Table WHERE Device_Name = ?', (device,))
    res = data.fetchall()
    return res


def ios_log(device, ios_ver):
    dbcsr.execute('INSERT OR IGNORE INTO Device_Info_Table (Device_Name, IOSVersion) VALUES (?, ?); ',
                  (device, ios_ver))
    dbcsr.execute('UPDATE Device_Info_Table SET IOSVersion=? WHERE Device_Name=?;',
                  (ios_ver, device))
    commit_changes()


def ios_retrieve(device):
    data = dbcsr.execute('SELECT IOSVersion FROM Device_Info_Table WHERE Device_Name = ?', (device,))
    res = data.fetchall()
    return res
