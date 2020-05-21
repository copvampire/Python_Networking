from jinja2 import Environment, FileSystemLoader ##Import Enviroment and FileSystemLoader from the Jinja2 Library 
import paramiko
import time
import json

HOSTS = json.load(open("./Datafiles/DataFile.json", "r") )

username = "admin"
password = "cisco"

##set up enviroment for loading files, load current directory
ENV = Environment(loader=FileSystemLoader('.'))
##Bind default and interface templates to variables
deviceConfig = ENV.get_template("Jinja2Templates/device_config.j2")
interfaceConfig = ENV.get_template("Jinja2Templates/interface_config.j2")
    
for hosts in HOSTS:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hosts,username=username,password=password)

    print("Successful connection", hosts)

    remote_connection = ssh_client.invoke_shell()

    remote_connection.send("conf t\n")
    ##Send Jinj2 template that was renderd with the data from hostname
    remote_connection.send(deviceConfig.render(hosts["Hostname"]))

    for interface in HOSTS["interfaces"]:
        ##Send Jinj2 template that was renderd with the data from the host interfaces
        remote_connection.send(interfaceConfig.render(hosts["interfaces"]))
        time.sleep(5)

    remote_connection.send("wr\n")
    time.sleep(1)
    remote_connection.send("\n")
    time.sleep(5)
    output = remote_connection.recv(65535)
    print(output)

    ssh_client.close()

