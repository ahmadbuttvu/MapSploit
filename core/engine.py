class MapSploitEngine:
    def __init__(self, rpc_client):
        self.rpc = rpc_client

    def score_module(self, module_name, rank, product_name):
        score = 0
        module_lower = module_name.lower()
        product_lower = product_name.lower() if product_name else ""
        
        if rank == 'excellent': score += 10
        elif rank == 'great': score += 7
        elif rank == 'good': score += 5
        elif rank == 'normal': score += 2

        if product_lower and any(word in module_lower for word in product_lower.split() if len(word) > 3):
            score += 20

        if "windows" in module_lower and "windows" not in product_lower:
            score -= 50
        if "solaris" in module_lower or "freebsd" in module_lower or "aix" in module_lower:
            score -= 50

        return score

    def search_vulnerabilities(self, recon_data):
        print("\n[*] Running Smart Context-Aware Mapping...")
        mapped_results = []

        for service in recon_data:
            product = service.get('product', '')
            srv_name = service.get('service', '')
            port = service['port']

            queries_to_try = []
            if product:
                queries_to_try.append(product)
                queries_to_try.append(product.split()[0])
            if srv_name:
                queries_to_try.append(srv_name)

            exploits_found = []
            
            for query in queries_to_try:
                print(f"[*] Trying MSF Search for: '{query}' (Port: {port})")
                try:
                    search_results = self.rpc.client.call('module.search', [query])
                    
                    if isinstance(search_results, list) and len(search_results) > 0:
                        for module in search_results:
                            if module.get('type') == 'exploit':
                                mod_name = module.get('fullname')
                                rank = module.get('rank')
                                
                                relevance_score = self.score_module(mod_name, rank, product)
                                
                                if relevance_score > 0:
                                    exploits_found.append({
                                        'module': mod_name,
                                        'rank': rank,
                                        'score': relevance_score
                                    })
                        
                        if exploits_found:
                            exploits_found = sorted(exploits_found, key=lambda x: x['score'], reverse=True)
                            print(f"    [+] Success! Found {len(exploits_found)} highly relevant modules.")
                            break
                            
                except Exception as e:
                    print(f"[-] Search failed for {query}: {e}")

            service['matching_exploits'] = exploits_found
            mapped_results.append(service)

        return mapped_results
