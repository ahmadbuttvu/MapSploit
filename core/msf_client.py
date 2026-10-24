from pymetasploit3.msfrpc import MsfRpcClient
import time

class MapSploitRPC:
    def __init__(self, password="mapsploit", port=55553, ssl=True):
        self.password = password
        self.port = port
        self.ssl = ssl
        self.client = None

    def connect(self):
        print(f"[*] Connecting to Metasploit RPC on port {self.port} (SSL: {self.ssl})...")
        for attempt in range(3):
            try:
                self.client = MsfRpcClient(self.password, port=self.port, ssl=self.ssl)
                print("[+] Successfully authenticated with Metasploit Database!")
                return True
            except Exception as e:
                print(f"[-] Connection attempt {attempt + 1} failed. Retrying in 2 seconds...")
                time.sleep(2)
        
        print("[-] Could not connect to MSFRPC.")
        return False
