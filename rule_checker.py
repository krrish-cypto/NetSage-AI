import re
import ipaddress

class RuleChecker:
    def __init__(self):
        self.issues = []

    def check_duplicate_ips(self, devices):
        """Check for duplicate IP addresses across all devices."""
        ip_map = {}
        for device in devices:
            for interface in device.get('interfaces', []):
                ip = interface.get('ip')
                if ip:
                    if ip in ip_map:
                        self.issues.append(f"Duplicate IP {ip} found on {device['name']} and {ip_map[ip]}")
                    else:
                        ip_map[ip] = device['name']

    def check_gateway_mismatch(self, hosts, routers):
        """Check if host default gateway is in the same subnet as its IP."""
        for host in hosts:
            ip = host.get('ip')
            mask = host.get('mask')
            gw = host.get('gateway')
            if not (ip and mask and gw):
                continue
            
            try:
                host_net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
                gw_ip = ipaddress.IPv4Address(gw)
                if gw_ip not in host_net:
                    self.issues.append(f"Gateway Mismatch: Host {host['name']} gateway {gw} is not in subnet {host_net}")
            except Exception as e:
                self.issues.append(f"Invalid IP configuration on {host['name']}: {str(e)}")

    def check_interface_down(self, devices):
        """Check for administratively down interfaces."""
        for device in devices:
            for interface in device.get('interfaces', []):
                if interface.get('status') == 'down':
                    self.issues.append(f"Interface Down: {device['name']} interface {interface['name']} is down.")

    def check_missing_vlan(self, switches, required_vlans):
        """Check if required VLANs exist on switches."""
        for switch in switches:
            configured_vlans = switch.get('vlans', [])
            for req_vlan in required_vlans:
                if req_vlan not in configured_vlans:
                    self.issues.append(f"Missing VLAN: Switch {switch['name']} is missing VLAN {req_vlan}")

    def run_checks(self, network_state):
        self.issues = []
        devices = network_state.get('routers', []) + network_state.get('switches', []) + network_state.get('hosts', [])
        
        self.check_duplicate_ips(devices)
        self.check_gateway_mismatch(network_state.get('hosts', []), network_state.get('routers', []))
        self.check_interface_down(devices)
        
        required_vlans = network_state.get('required_vlans', [])
        self.check_missing_vlan(network_state.get('switches', []), required_vlans)
        
        return self.issues

if __name__ == "__main__":
    # Sample Output demonstrating the rule checker
    sample_network = {
        "routers": [
            {
                "name": "Router1",
                "interfaces": [
                    {"name": "Gi0/0", "ip": "192.168.1.1", "mask": "255.255.255.0", "status": "up"},
                    {"name": "Gi0/1", "ip": "10.0.0.1", "mask": "255.255.255.0", "status": "down"}
                ]
            }
        ],
        "switches": [
            {
                "name": "Switch1",
                "interfaces": [
                    {"name": "Vlan1", "ip": "192.168.1.2", "mask": "255.255.255.0", "status": "up"}
                ],
                "vlans": [1, 10, 20]
            }
        ],
        "hosts": [
            {
                "name": "PC1",
                "ip": "192.168.1.10",
                "mask": "255.255.255.0",
                "gateway": "192.168.2.1", # Gateway mismatch
                "interfaces": [{"name": "Eth0", "ip": "192.168.1.10", "status": "up"}]
            },
            {
                "name": "PC2",
                "ip": "192.168.1.1", # Duplicate IP with Router1
                "mask": "255.255.255.0",
                "gateway": "192.168.1.1",
                "interfaces": [{"name": "Eth0", "ip": "192.168.1.1", "status": "up"}]
            }
        ],
        "required_vlans": [1, 10, 20, 30] # Missing VLAN 30 on Switch1
    }

    checker = RuleChecker()
    issues = checker.run_checks(sample_network)
    
    print("--- Rule Checker Results ---")
    for issue in issues:
        print(f"- {issue}")
