import re

INPUT_FILE = "insert_sample.txt"
OUTPUT_FILE = "create_schema.sql"

def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract content between `...` (`uid`, ...) VALUES
        match = re.search(r'INSERT INTO `[^`]+` \((.*?)\) VALUES', content)
        if not match:
            print("[!] Could not find column list in sample.")
            return

        cols_str = match.group(1)
        # Split by comma, handling potential backticks
        cols = [c.strip().strip('`') for c in cols_str.split(',')]
        
        print(f"[*] Found {len(cols)} columns.")
        
        sql = "CREATE TABLE hcclmafd2jnkwmfufmybb_users (\n"
        for col in cols:
            # Use TEXT for everything to be safe
            sql += f"    `{col}` TEXT,\n"
        
        # Remove last comma
        sql = sql.rstrip(",\n") + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(sql)
            
        print(f"[+] Schema saved to {OUTPUT_FILE}")
            
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
