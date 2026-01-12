import csv
import collections
import re
from pathlib import Path

def load_tor_nodes(csv_path):
    print(f"Loading Tor nodes from {csv_path}...")
    tor_ips = set()
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'IP' in row:
                    tor_ips.add(row['IP'])
    except Exception as e:
        print(f"Warning: Could not load Tor nodes: {e}")
    return tor_ips

def investigate_users(csv_file, tor_csv_path):
    print(f"Analyzing {csv_file}...")
    
    tor_ips = load_tor_nodes(tor_csv_path)
    print(f"Loaded {len(tor_ips)} Tor exit nodes.")
    
    users = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
            
    total_users = len(users)
    print(f"Loaded {total_users} users.")
    
    # 1. Domain Analysis
    domains = collections.Counter()
    sensitive_domains = {
        'gov': [],
        'mil': [],
        'edu': [],
        'org': [] 
    }
    
    interesting_substrings = ['fbi', 'police', 'interpol', 'cia', 'nsa', 'army', 'navy', 'usmc', 'nasa']
    flagged_users = []

    # 2. IP Analysis
    reg_ips = collections.Counter()
    last_ips = collections.Counter()
    tor_usage_count = 0
    tor_users = []

    # 3. Key Targets
    targets = ['pompompurin', 'Baphomet', 'ShinyHunters', 'Omnipotent']
    found_targets = []
    
    for u in users:
        username = u['username']
        email = u['email'].lower()
        regip = u.get('regip', '')
        lastip = u.get('lastip', '')
        
        # Domain parsing
        if '@' in email:
            domain = email.split('@')[-1]
            domains[domain] += 1
            
            tld = domain.split('.')[-1]
            if tld in sensitive_domains:
                sensitive_domains[tld].append(u)
            
            if any(s in email for s in interesting_substrings):
                flagged_users.append(u)
        
        # Target check
        if username in targets:
            found_targets.append(u)
            
        # Check username for interesting keywords
        if any(s in username.lower() for s in interesting_substrings):
             if u not in flagged_users:
                 flagged_users.append(u)
                 
        # IP Collection & Tor Check
        is_tor = False
        if regip and regip != '127.0.0.9': 
            reg_ips[regip] += 1
            if regip in tor_ips:
                is_tor = True
                
        if lastip and lastip != '127.0.0.9':
            last_ips[lastip] += 1
            if lastip in tor_ips:
                is_tor = True
                
        if is_tor:
            tor_usage_count += 1
            if len(tor_users) < 20: # Keep sample
                tor_users.append(u)

    # Report Generation
    with open('investigation_report.md', 'w', encoding='utf-8') as f:
        f.write("# Preliminary Intel Report: BreachForums Users\n\n")
        f.write(f"**Total Identities Analyzed:** {total_users}\n")
        f.write(f"**Tor Correlation:** {len(tor_ips)} known exit nodes loaded.\n\n")
        
        f.write("## 1. High Value Targets\n")
        f.write("| Username | Email | Reg IP | Last IP | Notes |\n|---|---|---|---|---|\n")
        for t in found_targets:
            reg = t.get('regip','N/A')
            last = t.get('lastip','N/A')
            notes = []
            if reg in tor_ips or last in tor_ips:
                notes.append("**TOR NODE**")
            
            # Manual Intel Injection
            if t['username'] == 'ShinyHunters' and last == '185.93.3.195':
                notes.append("Datacamp Ltd / IVPN (Confirmed via Spur)")
            
            note_str = ", ".join(notes)
            f.write(f"| {t['username']} | {t['email']} | {reg} | {last} | {note_str} |\n")
            
        f.write("\n### Target Intelligence Deep Dive: ShinyHunters\n")
        f.write("> **Analysis**: The subject utilized IP `185.93.3.195`. OSINT correlation confirms this is an **IVPN** exit node hosted by **Datacamp Limited** in Spain.\n\n")
        f.write("![ShinyHunters IP Analysis](assets/shinyhunters_ip_intel.png)\n")
            
        f.write("\n## 2. IP Intelligence\n")
        f.write(f"**Tor Usage Detected:** {tor_usage_count} users verified using Tor exit nodes.\n\n")
        
        f.write("### Top Shared Registration IPs (Sockpuppets/VPNs)\n")
        f.write("| IP Address | Count | Attribution |\n|---|---|---|\n")
        for ip, count in reg_ips.most_common(10):
             attr = "**TOR NODE**" if ip in tor_ips else "Unknown/VPN"
             f.write(f"| {ip} | {count} | {attr} |\n")

        f.write("\n### Top Shared Last IPs (Shared VPNs/Proxies)\n")
        f.write("| IP Address | Count | Attribution |\n|---|---|---|\n")
        for ip, count in last_ips.most_common(10):
             attr = "**TOR NODE**" if ip in tor_ips else "Unknown/VPN"
             f.write(f"| {ip} | {count} | {attr} |\n")

        f.write("\n## 3. Domain Statistics\n")
        f.write("### Top 20 Email Domains\n")
        f.write("| Domain | Count |\n|---|---|\n")
        for d, c in domains.most_common(20):
            f.write(f"| {d} | {c} |\n")
            
        f.write("\n## 4. Sensitive TLD Analysis\n")
        for tld in ['gov', 'mil', 'edu']:
            hits = sensitive_domains[tld]
            f.write(f"### .{tld.upper()} Domains ({len(hits)} found)\n")
            if hits:
                f.write("| Username | Email |\n|---|---|\n")
                for h in hits[:10]:
                    f.write(f"| {h['username']} | {h['email']} |\n")
            else:
                f.write("None found.\n")
                
        f.write("\n## 5. Flagged Keywords\n")
        f.write(f"Found {len(flagged_users)} users with keywords like fbi, police, etc.\n")
        f.write("| Username | Email |\n|---|---|\n")
        for u in flagged_users[:20]:
             f.write(f"| {u['username']} | {u['email']} |\n")

    print("Report generated: investigation_report.md")

if __name__ == "__main__":
    # Adjust path to where the tor_nodes.csv is located relative to execution or absolute
    # Repos are at ../repos/domain_intel/data/tor_nodes.csv relative to 'breachedforum_analysis' if we are in 'breachedforum_analysis' ?
    # Let's use absolute path for safety based on workspace info
    tor_path = r"c:\Users\anon\Documents\anon\repos\domain_intel\data\tor_nodes.csv"
    investigate_users("users.csv", tor_path)
