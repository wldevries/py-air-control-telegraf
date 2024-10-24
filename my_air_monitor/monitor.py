import subprocess
import re
import argparse
import socket

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

def send_to_telegraf_udp(server_address, ipaddr, fan_speed, pm25, iaql, ddp):
    # send data in InfluxDB line protocol format
    data = f"air_purifier,device=philips_fan,ipaddr={ipaddr} speed={fan_speed},pm25={pm25},iaql={iaql},ddp=\"{ddp}\""
    
    print(f"Sending data to Telegraf at {server_address}: {data}")

    # send data to InfluxDB via UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(data.encode('utf-8'), server_address)
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Monitor air purifiers by IP address.")    

    # Add an optional argument for the InfluxDB server address
    parser.add_argument('--server_address', metavar='IP:PORT', default='localhost:8094', 
                        help='IP address and port of the InfluxDB server (default: localhost:8094)')
                        
    # Add a positional argument to accept one or more air purifier IP addresses
    parser.add_argument('ip_addresses', metavar='IP', nargs='+', 
                        help='IP address(es) of the air purifiers')

    args = parser.parse_args()

    # Parse the server address
    server_address = parse_server_address(args.server_address)

    for ipaddr in args.ip_addresses:
        print(f"\nFetching data for IP: {ipaddr}")
        data = get_air_purifier_data(ipaddr)
        
        # Focus on specific values
        fan_speed = data.get('om')  # Fan speed
        pm25 = data.get('pm25')     # PM2.5 value
        iaql = data.get('iaql')     # Allergen index
        ddp = data.get('ddp')       # Used index

        send_to_telegraf_udp(server_address, ipaddr, fan_speed, pm25, iaql, ddp)

def parse_server_address(address):
    # Split the IP and port
    ip, port = address.split(':')
    return (ip, int(port))

if __name__ == "__main__":
    main()
