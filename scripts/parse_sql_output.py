import re
import csv
import os

INPUT_FILE = "../outputs/aggregates/raw_metrics.txt"
OUTPUT_DIR = "../outputs/aggregates/"

SECTION_MAP = {
    "PASSWORD ALGORITHM DISTRIBUTION": "password_algos.csv",
    "REGISTRATION YEAR/MONTH HISTOGRAM": "registration_stats.csv",
    "LANGUAGE DISTRIBUTION": "language_dist.csv",
    "TIMEZONE DISTRIBUTION": "timezone_dist.csv",
    "EMAIL TOP DOMAINS": "email_domains.csv",
    "EMAIL TLD DISTRIBUTION": "email_tlds.csv",
    "USERNAME LENGTH DISTRIBUTION": "username_lengths.csv",
    "USERNAME COMPLETELY NUMERIC": "username_types.csv"
}

def parse_raw_output():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_section = None
    headers = None
    data = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for section header
        if "---" in line:
            # Save previous section if exists
            if current_section and headers and data:
                save_csv(current_section, headers, data)
            
            # Start new section
            section_name = line.replace("---", "").strip()
            current_section = SECTION_MAP.get(section_name)
            headers = None
            data = []
            print(f"[*] Found section: {section_name} -> {current_section}")
            continue

        # Skip the "output_section" line itself which is the column header for the marker
        if line == "output_section":
            continue
            
        # Parse TSV data from MySQL
        parts = line.split('\t')
        
        if not headers:
            headers = parts
        else:
            data.append(parts)

    # Save last section
    if current_section and headers and data:
        save_csv(current_section, headers, data)

def save_csv(filename, headers, data):
    if not filename:
        return
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"[+] Saved {len(data)} rows to {filename}")

if __name__ == "__main__":
    parse_raw_output()
