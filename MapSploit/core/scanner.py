import nmap

class MapSploitScanner:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        try:
            self.nm = nmap.PortScanner()
        except nmap.PortScannerError:
            print("[-] Error: Nmap not found.")
            exit(1)

    def run_scan(self, ports=None):
        print(f"[*] Starting Scan on {self.target_ip}...")
        try:
            if ports:
                self.nm.scan(self.target_ip, ports, arguments='-sV -T4 -Pn')
            else:
                self.nm.scan(self.target_ip, arguments='-sV -T4 -Pn')
        except Exception as e:
            print(f"[-] Nmap scan failed: {e}")
            return []

        extracted_services = []

        for host in self.nm.all_hosts():
            if self.nm[host].state() == 'up':
                for proto in self.nm[host].all_protocols():
                    ports_list = self.nm[host][proto].keys()
                    
                    for port in ports_list:
                        service_data = self.nm[host][proto][port]
                        
                        if service_data['state'] == 'open':
                            extracted_services.append({
                                'port': port,
                                'protocol': proto,
                                'service': service_data.get('name', 'unknown'),
                                'product': service_data.get('product', ''),
                                'version': service_data.get('version', '')
                            })

        return extracted_services
