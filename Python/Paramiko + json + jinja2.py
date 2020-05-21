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
    ##bind sshclient to varaible
    ssh_client = paramiko.SSHClient()
    ##used to auto add a creditinals for ssh connection
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #Set up SSH connection to the host
    ssh_client.connect(hostname=hosts,username=username,password=password)

    print("Successful connection", hosts)

    ##Start shell session on the ssh connection
    remote_connection = ssh_client.invoke_shell()

    remote_connection.send("conf t\n")
    ##Send Jinj2 template that was renderd with the data from hostname
    remote_connection.send(deviceConfig.render(hosts["Hostname"]))

    for interface in HOSTS["interfaces"]:
        ##Send Jinj2 template that was renderd with the data from the host interfaces
        remote_connection.send(interfaceConfig.render(hosts["interfaces"]))
        time.sleep(5)

    remote_connection.send("wr\n")
    ##wait 1 second before continuing
    time.sleep(1)
    remote_connection.send("\n")
    time.sleep(5)
    ##print output of session into terminal
    output = remote_connection.recv(65535)
    print(output)

    ##Close SSH connection
    ssh_client.close()

