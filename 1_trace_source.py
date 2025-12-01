import os
import re
import csv
import requests
import time

# CONFIGURATION
# Update this path to your spam folder
spam_folder = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data\Spam"
output_file = r"CSV_Results\trace_results.csv"

# Regex to find IPv4 addresses (matches 4 sets of numbers)
ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

# Private IPs to ignore (Localhost, Local LAN, etc.)
# We don't want to trace "127.0.0.1" or "192.168.x.x"
def is_private_ip(ip):
    return ip.startswith(("10.", "172.16.", "192.168.", "127.", "0."))

def get_location(ip):
    try:
        # Free API: ip-api.com (Limit: 45 requests per minute)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['country'], data['isp']
        else:
            return "Unknown", "Unknown"
    except:
        return "Error", "Error"

def extract_source_ip(content):
    # We look for "Received: from" headers. 
    # usually the LAST "Received" header is the original source.
    # We find all IPs, reverse the list, and pick the first public one.
    ips = ip_pattern.findall(content)
    for ip in reversed(ips):
        if not is_private_ip(ip):
            return ip
    return None

print("Starting Spam Tracer... (This may take a while due to API limits)")

# Prepare the CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Filename", "Source IP", "Country", "ISP"]) # Header

    count = 0
    # Limit to 60 emails 
    # If do all 500, it will take ~15 minutes due to the sleep timer.
    limit = 60 

    for filename in os.listdir(spam_folder):
        if count >= limit: 
            break
        
        if filename.endswith(".txt"):
            filepath = os.path.join(spam_folder, filename)
            
            try:
                # 'latin-1' encoding is safer for old spam files than 'utf-8'
                with open(filepath, 'r', encoding='latin-1') as f:
                    content = f.read()
                    
                ip = extract_source_ip(content)
                
                if ip:
                    country, isp = get_location(ip)
                    print(f"[{count+1}] {filename} -> {ip} ({country})")
                    writer.writerow([filename, ip, country, isp])
                    
                    # CRITICAL: Sleep to avoid banning (45 req/min limit)
                    time.sleep(1.5) 
                    count += 1
                else:
                    print(f"Skipping {filename} (No public IP found)")
                    
            except Exception as e:
                print(f"Error reading {filename}: {e}")

print(f"\nDone! Results saved to {output_file}")