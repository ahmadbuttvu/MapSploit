import sys
from core.scanner import MapSploitScanner
from core.msf_client import MapSploitRPC
from core.engine import MapSploitEngine

def print_banner():
    print("="*60)
    print(" "*18 + "MapSploit Framework")
    print(" "*12 + "Automated Vulnerability Mapper")
    print("="*60)

def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: sudo python3 MapSploit.py <Target_IP>")
        sys.exit(1)

    target = sys.argv[1]
    
    scanner = MapSploitScanner(target)
    recon_data = scanner.run_scan()
    
    if not recon_data:
        print("[-] No open services found or scan failed.")
        sys.exit(1)

    print("\n" + "-"*60)
    rpc = MapSploitRPC()
    if not rpc.connect():
        print("[-] Exiting... Please start msfrpcd first.")
        sys.exit(1)

    print("\n" + "-"*60)
    engine = MapSploitEngine(rpc)
    final_results = engine.search_vulnerabilities(recon_data)

    print("\n" + "="*60)
    print(" "*20 + "FINAL MAPSPLOIT REPORT")
    print("="*60)

    for result in final_results:
        port = result['port']
        service = result['service'].upper()
        version = f"{result['product']} {result['version']}".strip()
        exploits = result.get('matching_exploits', [])

        print(f"\n[+] PORT {port} | {service} | {version if version else 'Unknown Version'}")
        
        if exploits:
            print(f"    [*] Found {len(exploits)} Exploit Modules:")
            for exp in exploits[:3]: 
                rank = exp.get('rank', 'normal')
                print(f"      -> {exp['module']} (Rank: {rank})")
            if len(exploits) > 3:
                print(f"      -> ... and {len(exploits) - 3} more.")
        else:
            print("    [-] No matching exploit modules found in Metasploit.")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
