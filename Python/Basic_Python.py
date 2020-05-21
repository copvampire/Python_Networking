import telnetlib

HOSTS = {
    "209.165.200.238": {
        "Hostname": "R2",
        "interfaces": {
            "S0/0/0": {
                "ipaddress": "172.16.1.2",
                "netmask": "255.255.255.252",
                "uplink": False,
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
                "VLAN": "21"
                }
        }
    }
}
user = "admin"
password = "cisco"

for hosts in HOSTS:
    tn = telnetlib.Telnet(hosts)

    tn.read_until("Username: ")
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")
    
    tn.write("conf t\n")
    tn.write("hostname {} \n").format(hosts["Hostname"])
    tn.write("banner motd \#Unauthorised access is strictly prohibited\#\n")
    tn.write("no ip domain-lookup\n")
    tn.write("ip domain-name cisco.com\n")
    tn.write("crypto key generate rsa general-keys modulus 2048\n")
    tn.write("line vty 0 4\n")
    tn.write("transport input all\n")
    
    for interface in HOSTS["interfaces"]:
        tn.write("int {}\n").format(interface)
        if interface["uplink"] is False:
            tn.write("ip address {} {}\n").format(interface["ipaddress"], interface["netmask"])
            if interface["VLAN"] is not False:
                tn.write("switchport mode access vlan {}\n").format(interface["VLAN"])
                tn.write("exit\n")
            tn.write("exit\n")
        else:
            tn.write("switchport mode trunk \n")
            tn.write("exit\n")

    tn.write("wr\n")
    tn.read_until("Destination filename [startup-config]?")
    tn.write("\n")
    tn.read_until("[OK]")
    tn.write("end\n")
    tn.write("exit\n")

print tn.read_all()