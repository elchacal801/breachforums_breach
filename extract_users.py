import re
import csv
import sys
import socket
import struct

def hex_to_ip(hex_str):
    try:
        # Handle '0x' prefix
        if hex_str.startswith('0x') or hex_str.startswith('0X'):
            # Convert hex to int
            val = int(hex_str, 16)
            # Pack as big-endian unsigned int
            packed = struct.pack('>I', val)
            # Convert to IP string
            return socket.inet_ntoa(packed)
    except Exception:
        pass
    return hex_str # Return original if conversion fails

def parse_sql_dump(input_file, output_file):
    print(f"Processing {input_file}...")
    
    insert_pattern = re.compile(r"INSERT INTO `[^`]+` \((.*?)\) VALUES", re.IGNORECASE)
    
    columns = []
    col_indices = {}
    target_cols = ['username', 'email', 'regip', 'lastip']
    ip_cols = ['regip', 'lastip']
    
    count = 0
    
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f_in, \
         open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        
        writer = csv.writer(f_out)
        writer.writerow(target_cols)
        
        for line in f_in:
            if not line.startswith("INSERT INTO"):
                continue
                
            if not columns:
                match = insert_pattern.search(line)
                if match:
                    cols_str = match.group(1)
                    columns = [c.strip('` ') for c in cols_str.split(',')]
                    print(f"Found columns: {columns}")
                    
                    try:
                        for t in target_cols:
                            col_indices[t] = columns.index(t)
                    except ValueError as e:
                        print(f"Error: Could not find required columns. Available: {columns}")
                        return
                    
            if not col_indices:
                continue

            val_start = line.find('VALUES')
            if val_start == -1: continue
            
            content = line[val_start + 6:].strip()
            if content.endswith(';'):
                content = content[:-1]
                
            idx = 0
            n = len(content)
            in_string = False
            escape = False
            in_paren = False
            
            row_items = []
            current_item = []
            
            while idx < n:
                char = content[idx]
                
                if char == '(':
                    if not in_string:
                        in_paren = True
                        row_items = []
                        current_item = []
                        idx += 1
                        continue
                
                if char == ')':
                    if not in_string and in_paren:
                         is_end_of_row = False
                         if idx + 1 >= n:
                             is_end_of_row = True
                         elif content[idx+1] in [',', ';']:
                             is_end_of_row = True
                             
                         if is_end_of_row:
                             row_items.append("".join(current_item).strip())
                             
                             # Process row
                             max_idx = max(col_indices.values())
                             if len(row_items) > max_idx:
                                 row_data = []
                                 for col in target_cols:
                                     val = row_items[col_indices[col]]
                                     if val.startswith("'") and val.endswith("'"):
                                         val = val[1:-1]
                                     
                                     if col in ip_cols:
                                         val = hex_to_ip(val)
                                         
                                     row_data.append(val)
                                 
                                 writer.writerow(row_data)
                                 count += 1
                                 if count % 1000 == 0:
                                     print(f"Extracted {count} users...", end='\r')
                             
                             in_paren = False
                             idx += 1
                             if idx < n and content[idx] == ',':
                                 idx += 1 
                             continue
                             
                if char == "'":
                    if not escape:
                        in_string = not in_string
                    else:
                        escape = False 
                        
                if char == '\\':
                    if in_string:
                        escape = not escape
                    else:
                         escape = False
                         
                if char == ',':
                    if not in_string and in_paren:
                        row_items.append("".join(current_item).strip())
                        current_item = []
                        idx += 1
                        continue
                        
                if in_paren:
                    current_item.append(char)
                
                if escape and char != '\\':
                    escape = False
                    
                idx += 1

    print(f"\nDone. Extracted {count} users to {output_file}")

if __name__ == "__main__":
    parse_sql_dump("data/databoose.sql", "users.csv")
