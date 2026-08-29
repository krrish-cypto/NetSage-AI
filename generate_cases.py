import csv
import random

cases = []

# Concept Tags and their templates
vlan_cases = [
    {
        "symptom": "PC gets IP but cannot ping default gateway.",
        "topology_note": "PC connected to Switch1 Fa0/1, Router on Gi0/1 (Router-on-a-stick).",
        "show_outputs": "Switch1# show vlan brief -> Fa0/1 is in VLAN 1 (default), expected VLAN 10.",
        "expected_fault": "Access port assigned to wrong VLAN.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "High"
    },
    {
        "symptom": "Devices in VLAN 20 cannot communicate with devices in VLAN 30.",
        "topology_note": "Switch1 connects to Switch2 via Gi0/1.",
        "show_outputs": "Switch1# show interfaces trunk -> Gi0/1 allowed vlans 1-19,30-4094. VLAN 20 is missing.",
        "expected_fault": "VLAN not allowed on trunk link.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "Medium"
    },
    {
        "symptom": "No connectivity for new host added to switch.",
        "topology_note": "Host on Fa0/5 in VLAN 50.",
        "show_outputs": "Switch# show vlan -> VLAN 50 does not exist in database.",
        "expected_fault": "VLAN missing from switch database.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "High"
    },
    {
        "symptom": "PC cannot reach server in another subnet; ping to local gateway works.",
        "topology_note": "Core switch acting as L3 gateway for VLANs.",
        "show_outputs": "CoreSwitch# show ip route -> no route to destination subnet. SVIs configured but ip routing is disabled.",
        "expected_fault": "IP routing not enabled on Layer 3 switch.",
        "osi_layer": "Layer 3",
        "concept_tag": "VLAN",
        "severity": "Critical"
    }
]

gateway_cases = [
    {
        "symptom": "PC can ping local subnet but not internet.",
        "topology_note": "PC IP 192.168.1.50/24.",
        "show_outputs": "C:\\> ipconfig -> Default Gateway: 192.168.2.1 (Different subnet).",
        "expected_fault": "Incorrect default gateway configured on PC.",
        "osi_layer": "Layer 3",
        "concept_tag": "Gateway",
        "severity": "High"
    },
    {
        "symptom": "Hosts in subnet 10.0.0.0/24 cannot reach other subnets.",
        "topology_note": "Router interface Gi0/0 is gateway for 10.0.0.0/24.",
        "show_outputs": "Router# show ip interface brief -> Gi0/0 is administratively down.",
        "expected_fault": "Gateway interface is shutdown.",
        "osi_layer": "Layer 1/3",
        "concept_tag": "Gateway",
        "severity": "Critical"
    },
    {
        "symptom": "Intermittent connectivity to other subnets.",
        "topology_note": "Two routers configured with HSRP for gateway redundancy.",
        "show_outputs": "Router1# show standby -> State is Init. Interface track is down.",
        "expected_fault": "HSRP state failure due to tracked interface.",
        "osi_layer": "Layer 3",
        "concept_tag": "Gateway",
        "severity": "Medium"
    },
    {
        "symptom": "PC receives IP via DHCP but has no default gateway.",
        "topology_note": "DHCP server configured on local router.",
        "show_outputs": "Router# show run | section dhcp -> default-router command is missing from pool.",
        "expected_fault": "DHCP pool missing default-router configuration.",
        "osi_layer": "Layer 3",
        "concept_tag": "Gateway",
        "severity": "High"
    }
]

dhcp_cases = [
    {
        "symptom": "PC has 169.254.x.x APIPA address.",
        "topology_note": "DHCP server on different subnet than PC.",
        "show_outputs": "Router(VLAN10)# show run interface vlan 10 -> ip helper-address is missing.",
        "expected_fault": "Missing IP helper-address for DHCP relay.",
        "osi_layer": "Layer 3/7",
        "concept_tag": "DHCP",
        "severity": "High"
    },
    {
        "symptom": "New devices cannot get IP addresses, existing devices work.",
        "topology_note": "Router provides DHCP for 192.168.1.0/24.",
        "show_outputs": "Router# show ip dhcp pool -> Free addresses: 0.",
        "expected_fault": "DHCP pool exhausted.",
        "osi_layer": "Layer 7",
        "concept_tag": "DHCP",
        "severity": "Medium"
    },
    {
        "symptom": "PC assigned IP address that conflicts with static server IP.",
        "topology_note": "Server has static IP 10.1.1.10.",
        "show_outputs": "Router# show run | include dhcp excluded -> command missing.",
        "expected_fault": "Static IPs not excluded from DHCP pool.",
        "osi_layer": "Layer 3/7",
        "concept_tag": "DHCP",
        "severity": "High"
    },
    {
        "symptom": "PC gets IP address but no DNS server.",
        "topology_note": "Router is DHCP server.",
        "show_outputs": "Router# show ip dhcp pool -> dns-server command missing.",
        "expected_fault": "DHCP pool missing DNS server configuration.",
        "osi_layer": "Layer 7",
        "concept_tag": "DHCP",
        "severity": "Low"
    }
]

dns_cases = [
    {
        "symptom": "Users can ping 8.8.8.8 but cannot open www.google.com.",
        "topology_note": "PC using internal DNS server.",
        "show_outputs": "C:\\> nslookup www.google.com -> DNS request timed out.",
        "expected_fault": "Internal DNS server unreachable or misconfigured.",
        "osi_layer": "Layer 7",
        "concept_tag": "DNS",
        "severity": "Medium"
    },
    {
        "symptom": "Router cannot resolve hostnames for ping or telnet.",
        "topology_note": "Router needs to resolve external names.",
        "show_outputs": "Router# show run | include ip domain-lookup -> no ip domain-lookup is configured.",
        "expected_fault": "Domain lookup disabled on router.",
        "osi_layer": "Layer 7",
        "concept_tag": "DNS",
        "severity": "Low"
    },
    {
        "symptom": "Internal web server unreachable by hostname, IP works.",
        "topology_note": "Internal DNS used.",
        "show_outputs": "DNS Server -> A record points to old IP address 192.168.1.5 instead of 192.168.1.10.",
        "expected_fault": "Stale or incorrect DNS A record.",
        "osi_layer": "Layer 7",
        "concept_tag": "DNS",
        "severity": "Medium"
    },
    {
        "symptom": "PC gets wrong DNS server via DHCP.",
        "topology_note": "Router provides DHCP.",
        "show_outputs": "Router# show run | section dhcp -> dns-server is typed as 8.8.8.9 instead of 8.8.8.8.",
        "expected_fault": "Typo in DHCP dns-server configuration.",
        "osi_layer": "Layer 7",
        "concept_tag": "DNS",
        "severity": "Medium"
    }
]

routing_cases = [
    {
        "symptom": "Branch A cannot reach Branch B.",
        "topology_note": "OSPF configured on both branch routers.",
        "show_outputs": "RouterA# show ip ospf neighbor -> list is empty. show run -> network statement has wrong wildcard mask.",
        "expected_fault": "OSPF network statement misconfiguration prevents adjacency.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "Critical"
    },
    {
        "symptom": "Traffic taking suboptimal path to destination.",
        "topology_note": "Dual links between routers, EIGRP running.",
        "show_outputs": "Router# show ip route -> route points to slower serial link. show interface -> bandwidth statement is wrong on fast link.",
        "expected_fault": "Incorrect bandwidth configuration affecting metric.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "Medium"
    },
    {
        "symptom": "No default route propagated to internal network.",
        "topology_note": "Edge router running OSPF with internal routers.",
        "show_outputs": "EdgeRouter# show run | section ospf -> default-information originate is missing.",
        "expected_fault": "Missing default-information originate command in OSPF.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "High"
    },
    {
        "symptom": "Static route not appearing in routing table.",
        "topology_note": "Next hop IP is 10.1.1.2.",
        "show_outputs": "Router# show ip route -> 10.1.1.2 is not reachable. Interface connected to next hop is down.",
        "expected_fault": "Static route invalid because next-hop is unreachable.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "High"
    }
]

acl_cases = [
    {
        "symptom": "SSH access to router denied from admin PC.",
        "topology_note": "VTY lines have access-class applied.",
        "show_outputs": "Router# show access-lists 10 -> permit 192.168.1.0 0.0.0.255. Admin PC is 10.0.0.5.",
        "expected_fault": "ACL denies admin PC IP address.",
        "osi_layer": "Layer 3/4",
        "concept_tag": "ACL",
        "severity": "High"
    },
    {
        "symptom": "Web traffic blocked, ping works to server.",
        "topology_note": "Extended ACL applied inbound on router interface.",
        "show_outputs": "Router# show access-lists 101 -> permit icmp any any, deny tcp any any eq 80, permit ip any any.",
        "expected_fault": "Extended ACL explicitly blocking port 80.",
        "osi_layer": "Layer 4",
        "concept_tag": "ACL",
        "severity": "Medium"
    },
    {
        "symptom": "All traffic from Branch dropped at Core.",
        "topology_note": "Standard ACL applied.",
        "show_outputs": "Core# show run interface Gi0/0 -> ip access-group 10 in. ACL 10 has no permit statements (implicit deny all).",
        "expected_fault": "Implicit deny all dropping traffic due to missing permit statements.",
        "osi_layer": "Layer 3",
        "concept_tag": "ACL",
        "severity": "Critical"
    },
    {
        "symptom": "DHCP requests failing for clients.",
        "topology_note": "ACL applied inbound on client VLAN interface.",
        "show_outputs": "Router# show access-lists -> denies UDP ports 67/68.",
        "expected_fault": "ACL blocking DHCP broadcast traffic.",
        "osi_layer": "Layer 4",
        "concept_tag": "ACL",
        "severity": "High"
    }
]

nat_cases = [
    {
        "symptom": "Internal hosts cannot reach internet.",
        "topology_note": "PAT configured on edge router.",
        "show_outputs": "Router# show ip nat translations -> empty. show run -> ip nat inside/outside missing on interfaces.",
        "expected_fault": "Missing ip nat inside/outside on interfaces.",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "Critical"
    },
    {
        "symptom": "External users cannot access internal web server.",
        "topology_note": "Static NAT configured.",
        "show_outputs": "Router# show run | include nat -> ip nat inside source static 192.168.1.10 203.0.113.5. Actually, server IP is 192.168.1.20.",
        "expected_fault": "Static NAT maps to wrong internal IP.",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "High"
    },
    {
        "symptom": "Only some internal hosts can access internet.",
        "topology_note": "Dynamic NAT with pool.",
        "show_outputs": "Router# show ip nat statistics -> Pool exhausted. 'overload' keyword is missing.",
        "expected_fault": "NAT pool exhausted due to missing 'overload' keyword for PAT.",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "Medium"
    },
    {
        "symptom": "NAT translations failing.",
        "topology_note": "Access-list used to define interesting traffic for NAT.",
        "show_outputs": "Router# show access-lists 1 -> permit 10.0.0.0 0.0.0.255. Internal network is 192.168.1.0/24.",
        "expected_fault": "NAT ACL matches wrong internal subnet.",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "High"
    }
]

wireless_cases = [
    {
        "symptom": "Clients cannot associate with AP.",
        "topology_note": "WLC and lightweight AP deployed.",
        "show_outputs": "WLC UI -> AP not joined. Switch# show power inline -> AP drawing 0W, PoE disabled on port.",
        "expected_fault": "PoE not enabled on switch port connecting to AP.",
        "osi_layer": "Layer 1",
        "concept_tag": "Wireless",
        "severity": "High"
    },
    {
        "symptom": "Guest Wi-Fi clients get internal IPs.",
        "topology_note": "WLAN mapped to VLAN.",
        "show_outputs": "WLC UI -> Guest WLAN mapped to Management Interface instead of Guest Interface.",
        "expected_fault": "WLAN mapped to incorrect interface/VLAN on WLC.",
        "osi_layer": "Layer 2",
        "concept_tag": "Wireless",
        "severity": "Medium"
    },
    {
        "symptom": "Poor wireless performance in specific area.",
        "topology_note": "Multiple APs in area.",
        "show_outputs": "WLC UI -> All APs on Channel 6, causing high co-channel interference.",
        "expected_fault": "Channel overlap/co-channel interference.",
        "osi_layer": "Layer 1",
        "concept_tag": "Wireless",
        "severity": "Low"
    },
    {
        "symptom": "Clients disconnect frequently.",
        "topology_note": "WPA2 Enterprise configured.",
        "show_outputs": "WLC UI -> RADIUS server unreachable. Radius server IP changed recently.",
        "expected_fault": "RADIUS server configuration on WLC points to wrong IP.",
        "osi_layer": "Layer 7",
        "concept_tag": "Wireless",
        "severity": "High"
    }
]

# Combine all cases
all_case_lists = [vlan_cases, gateway_cases, dhcp_cases, dns_cases, routing_cases, acl_cases, nat_cases, wireless_cases]
for lst in all_case_lists:
    cases.extend(lst)

# Generate a few more variations to ensure >30 cases (currently 32)
extra_cases = [
    {
        "symptom": "Server cannot reach backup server in same rack.",
        "topology_note": "Both servers connected to same switch.",
        "show_outputs": "Switch# show interfaces trunk -> Port is in access mode, but servers need trunking for virtualization.",
        "expected_fault": "Switchport mode is access instead of trunk for hypervisor.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "Medium"
    },
    {
        "symptom": "No internet access for newly provisioned subnet.",
        "topology_note": "NAT edge router.",
        "show_outputs": "Router# show ip nat translations -> No entries for new subnet. ACL 1 (NAT) does not include new subnet.",
        "expected_fault": "NAT ACL needs updating to include new subnet.",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "High"
    }
]
cases.extend(extra_cases)

# Write to CSV
csv_file = "C:\\Users\\krish\\Cisco AI Internship\\NetSage-AI\\cases.csv"
keys = cases[0].keys()

with open(csv_file, 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(cases)

print(f"Generated {len(cases)} cases and saved to {csv_file}")
