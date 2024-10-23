import subprocess
import re
import argparse

def get_air_purifier_data(ipaddr):
    result = subprocess.run(['airctrl', '--ipaddr', ipaddr], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return parse_output(output)

def parse_output(output):
    data = {}
    
    # Regular expression to capture the key and value from each line
    pattern = re.compile(r'\[(.*?)\]\s+(.*):\s+(.*)')
    
    # Go through each line and match it
    for line in output.splitlines():
        match = pattern.match(line)
        if match:
            code, _, value = match.groups()
            data[code.strip()] = value.strip()
    
    return data

def main(ip_addresses):
    for ipaddr in ip_addresses:
        print(f"\nFetching data for IP: {ipaddr}")
        data = get_air_purifier_data(ipaddr)
        
        # Focus on specific values
        fan_speed = data.get('om')  # Fan speed
        pm25 = data.get('pm25')     # PM2.5 value
        iaql = data.get('iaql')     # Allergen index
        ddp = data.get('ddp')       # Used index
        
        # Print the relevant data
        print(f"Fan speed (om): {fan_speed}")
        print(f"PM2.5 (pm25): {pm25}")
        print(f"Allergen index (iaql): {iaql}")
        print(f"Used index (ddp): {ddp}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor air purifiers by IP address.")
    
    # Add an argument to accept one or more IP addresses
    parser.add_argument('ip_addresses', metavar='IP', nargs='+', help='IP address(es) of the air purifiers')
    
    args = parser.parse_args()
    
    # Pass the list of IP addresses to the main function
    main(args.ip_addresses)
