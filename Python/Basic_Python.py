import telnetlib ##import telnet library

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

##for each host in the dictonary HOSTS run
for hosts in HOSTS:
    ##connect to telnet IP set in hosts
    tn = telnetlib.Telnet(hosts)

    ##wait for Username: to appear then enter in username
    tn.read_until("Username: ")
    tn.write(user + "\n")
    ##If there is a password, enter the password
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")
    
    ##Enter configure terminal mode and apply default configuration
    tn.write("conf t\n")
    ##Apply hostname variable to the string hostname {}
    tn.write("hostname {} \n").format(hosts["Hostname"])
    tn.write("banner motd \#Unauthorised access is strictly prohibited\#\n")
    tn.write("no ip domain-lookup\n")
    tn.write("ip domain-name cisco.com\n")
    tn.write("crypto key generate rsa general-keys modulus 2048\n")
    tn.write("line vty 0 4\n")
    tn.write("transport input all\n")
    
    ##For each interface within the hosts run
    for interface in HOSTS["interfaces"]:
        ##Apply interface name variable to the string int {}
        tn.write("int {}\n").format(interface)
        ##if not a trunk link run
        if interface["uplink"] is False:
            ##set ipaddress and subnet, defined within interface dictonary
            tn.write("ip address {} {}\n").format(interface["ipaddress"], interface["netmask"])
            ##if there is a vlan enter in this, if not skip
            if interface["VLAN"] is not False:
                tn.write("switchport mode access vlan {}\n").format(interface["VLAN"])
                tn.write("exit\n")
            tn.write("exit\n")
        else:
            ##If uplink is not false set to trunk
            tn.write("switchport mode trunk \n")
            tn.write("exit\n")
    ##save configuration
    tn.write("wr\n")
    ##wait for this to appear
    tn.read_until("Destination filename [startup-config]?")
    tn.write("\n")
    tn.read_until("[OK]")
    tn.write("end\n")
    tn.write("exit\n")

##Print to console
print tn.read_all()