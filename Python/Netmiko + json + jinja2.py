from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko
import time
import json

HOSTS = json.load(open("DataFile.json", "r") )

ENV = Environment(loader=FileSystemLoader('.'))
deviceConfig = ENV.get_template("device_config.j2")
interfaceConfig = ENV.get_template("interface_config.j2")
    
for hosts in HOSTS:
    net_connect = Netmiko(hosts, username="admin", password="cisco", device_type="cisco_ios")

    print("Successful connection", hosts)

    net_connect.send_command("conf t\n")
    net_connect.send_command(deviceConfig.render(hosts["Hostname"]))

    for interface in HOSTS["interfaces"]:
        net_connect.send_command(interfaceConfig.render(hosts["interfaces"]))
        time.sleep(5)

    net_connect.send_command("wr\n")
    time.sleep(1)
    net_connect.send_command("\n")
    time.sleep(5)
    output = net_connect.find_prompt()
    print(output)

    net_connect.disconnect()

