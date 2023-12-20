#!/bin/bash

# Check if both team name and API key are provided
if [ "$#" -ne 2 ]; then
    echo "Error: Team name and API key are required."
    echo "Usage: $0 <team_name> <api_key>"
    exit 1
fi

teamname=$1
API_KEY=$2
URL="https://nodeboard.io/a/$teamname/n/api/managedsites/"

# Gather system information with error checking
HOSTNAME=$(hostname)
IP_ADDRESS=$(hostname -I | awk '{print $1}')  # Primary IP address
OS_TYPE=$(uname -s)  # Operating system name
KERNEL_VERSION=$(uname -r)  # Kernel version

if ! OS_VERSION=$(lsb_release -d | awk -F"\t" '{print $2}'); then
    echo "Error: Unable to determine OS version."
    exit 1
fi

if ! SERIAL_NUMBER=$(sudo dmidecode -t system | grep 'Serial Number' | awk -F: '{print $2}' | xargs); then
    echo "Error: Unable to determine Serial Number."
    exit 1
fi

RAM=$(grep MemTotal /proc/meminfo | awk '{print int($2/1024/1024)}')  # Total RAM in GB
if [ -z "$RAM" ]; then
    echo "Error: Unable to determine RAM."
    exit 1
fi

if ! CPU_TYPE=$(grep "model name" /proc/cpuinfo | uniq | awk -F: '{print $2}' | xargs); then
    echo "Error: Unable to determine CPU type."
    exit 1
fi

CPU_CORES=$(grep -c ^processor /proc/cpuinfo)  # Number of CPU cores
if [ -z "$CPU_CORES" ]; then
    echo "Error: Unable to determine CPU cores."
    exit 1
fi

UPTIME=$(uptime -p)  # System uptime
if [ -z "$UPTIME" ]; then
    echo "Error: Unable to determine uptime."
    exit 1
fi

# JSON data to be sent in the POST request
# url and ip_address cannot be blank, we recommend filling url with https://example.com or some other url if it does not have an actual routable URL
DATA_JSON=$(cat <<EOF
{
  "name": "$HOSTNAME",
  "url": "http://example.com", 
  "ip_address": "$IP_ADDRESS", 
  "notes": "Some important notes that you want to add",
  "description": "Laptop",
  "tags": ["$OS_TYPE", "$KERNEL_VERSION", "OS Version: $OS_VERSION", "Serial: $SERIAL_NUMBER", "RAM: $RAM GB", "CPU: $CPU_TYPE", "Cores: $CPU_CORES", "Uptime: $UPTIME"]
}
EOF
)

# POST request with curl and error handling
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$URL" \
     -H "Authorization: Api-Key $API_KEY" \
     -H "Content-Type: application/json" \
     -d "$DATA_JSON")

if [ "$RESPONSE" -ne 200 ] && [ "$RESPONSE" -ne 201 ]; then
    echo "Error: Failed to send data to Nodeboard (HTTP code $RESPONSE)."
    exit 1
fi

echo "Data successfully sent to Nodeboard."
