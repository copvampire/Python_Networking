import paramiko ##import Paramiko Libaray
import time ##import time, used for waiting

##Host dictonary for names, and interface data
HOSTS = {
    ##Ip address to connect to device
    "209.165.200.238": {
        ##Name of device
        "Hostname": "R2",
        "interfaces": {
            "S0/0/0": {
                "ipaddress": "172.16.1.2",
                "netmask": "255.255.255.252",
                ##Not a trunk connection
                "uplink": False,
                ##No VLAN on this interface
                "VLAN": False
                },
            "S0/0/1": {
                "ipaddress": "172.16.1.2",
                "netmask": "255.255.255.252",
                "uplink": False,
                "VLAN": False
                }
        }
    },
    "172.16.1.1": {
        "Hostname": "R1",
        "interfaces": {
            "S0/0/0": {
                "ipaddress": "172.16.1.2",
                "netmask": "255.255.255.252",
                "uplink": False,
                "VLAN": False
                },
            "f0/5": {
                ##Is trunk connection
                "uplink": True,
                "VLAN": False
                }
        }
    },
    "192.168.99.2": {
        "Hostname": "Switch0",
        "interfaces": {
            "f0/5": {
                "uplink": True,
                "VLAN": False
                },
            "F0/6": {
                "ipaddress": "172.16.1.2",
                "netmask": "255.255.255.252",
                "uplink": False,
                ##VLAN 21 uses this interface
                "VLAN": "21"
                }
        }
    }
}
##Cisco login credentials
user = "admin"
password = "cisco"


for hosts in HOSTS:
    
    ##bind sshclient to varaible
    ssh_client = paramiko.SSHClient()
    ##used to auto add a creditinals for ssh connection
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #Set up SSH connection to the host
    ssh_client.connect(hostname=hosts,username=user,password=password)

    print("Successful connection", hosts)

    ##Start shell session on the ssh connection
    remote_connection = ssh_client.invoke_shell()
    
    ##Run commands through shell session
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
        ##wait 1 second before continuing
        time.sleep(1)
        remote_connection.send("\n")
        time.sleep(5)
        remote_connection.send("end\n")
        remote_connection.send("exit\n")
    
    time.sleep(1)
    ##print output of session into terminal
    output = remote_connection.recv(999999)
    print(output)

    ##Close SSH connection
    ssh_client.close()

