import re
import time
import SQL_Module
thread_flag = 0


def routes(session):
    #
    # Logs the Cisco IOS Routes from the routing table
    #
    result = session.send_command("sh ip route")
    res = re.findall(r'[0-9]+?\.[0-9]+?\.[0-9]+?\.[0-9]', result)
    ip_table = "\n".join(res)
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    SQL_Module.log_route(device, ip_table)


def vlans(session):
    #
    # Logs the Cisco VLAN Database
    #
    result = session.send_command("sh vlans")
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    SQL_Module.log_vlan(device, result)


def ios(session):
    #
    # Logs the Cisco IOS Version
    #
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    result = session.send_command("sh version")
    res = result.partition('\n')[0]
    SQL_Module.ios_log(device, res)


def sys(session):
    #
    # Logs Cisco IOS Logs
    #
    result = session.send_command("sh log")
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    SQL_Module.sys_logger(device, result)


def get_route(session):
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    res = SQL_Module.retrieve_route(device)
    return res[0]


def get_vlan(session):
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    res = SQL_Module.get_vlans(device)
    return res[0]


def get_version(session):
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    res = SQL_Module.ios_retrieve(device)
    return res[0]


def get_syslog(session):
    device = session.find_prompt()
    device = re.sub('[>#]', '', device)
    res = SQL_Module.log_retrieve(device)
    return res[0]


def tasks(session, delay):
    while True:
        global thread_flag
        if thread_flag == 1:
            return None
        else:
            routes(session)
            vlans(session)
            ios(session)
            sys(session)
            time.sleep(delay)
