# Py-air-control-telegraf

This monitor application queries Philips air purifiers using https://github.com/rgerganov/py-air-control and sends the result to InfluxDB Telegraf over UDP

## Usage
```
usage: monitor.py [-h] [-s IP:PORT] [--interval INTERVAL_SECONDS]
                  IP [IP ...]

Monitor air purifiers by IP address.

positional arguments:
  IP                    IP address(es) of the air purifiers

options:
  -h, --help            show this help message and exit
  -s IP:PORT, --server_address IP:PORT
                        IP address and port of InfluxDB Telegraf UDP
                        Socker server (default: localhost:8094)
  --interval INTERVAL_SECONDS
                        Seconds between updates (default: 60)
```

## Docker

Build the docker image
```
docker build -t my-air-monitor-image .
```

Run the docker image and configure the telegraf UDP port and IP addresses of the Philips air purifiers
```
docker run my-air-monitor-image --server_address=192.168.86.66:8094 192.168.86.23 192.168.86.246
```
