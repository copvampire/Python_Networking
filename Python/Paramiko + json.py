import paramiko
import time
import json

HOSTS = json.load(open("DataFile.json", "r") )

username = "admin"
password = "cisco"


for hosts in HOSTS:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hosts,username=username,password=password)

    print("Successful connection", hosts)

    remote_connection = ssh_client.invoke_shell()

    remote_connection.send("conf t\n")
    remote_connection.send("hostname {} \n").format(hosts["Hostname"])
    remote_connection.send("banner motd \#Unauthorised access is strictly prohibited\#\n")
    remote_connection.send("no ip domain-lookup\n")
    remote_connection.send("ip domain-name cisco.com\n")
    remote_connection.send("crypto key generate rsa general-keys modulus 2048\n")
    remote_connection.send("line vty 0 4\n")
    remote_connection.send("transport input all\n")

    for interface in HOSTS["interfaces"]:
        remote_connection.send("int {}\n").format(interface)
        if interface["uplink"] is False:
            remote_connection.send("ip address {} {}\n").format(interface["ipaddress"], interface["netmask"])
            if interface["VLAN"] is not False:
                remote_connection.send("switchport mode access vlan {}\n").format(interface["VLAN"])
                remote_connection.send("exit\n")
            remote_connection.send("exit\n")
        else:
            remote_connection.send("switchport mode trunk \n")
            remote_connection.send("exit\n")

        remote_connection.send("wr\n")
        time.sleep(1)
        remote_connection.send("\n")
        time.sleep(5)
        remote_connection.send("end\n")
        remote_connection.send("exit\n")
    
    time.sleep(1)
    output = remote_connection.recv(65535)
    print(output)

    ssh_client.close

