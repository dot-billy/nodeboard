# Notes

### Obtain your Nodeboard API Key:

1. Login to https://nodeboard.io

2. Click Profile

3. Scroll down, select New API Key 

4. Copy down the API key as it'll only appear once.

   

### Obtain your UniFi API Key:

1. Sign in to the UniFi Site Manager at unifi.ui.com.
2. From the left navigation bar, click on API.
3. Click Create API Key.
4. Copy the key and store it securely, as it will only be displayed once.
5. Click Done to ensure the key is hashed and securely stored.

# Notes

### Obtain your Nodeboard API Key:

1. Login to https://nodeboard.io

2. Click Profile

3. Scroll down, select New API Key 

4. Copy down the API key as it'll only appear once.

localhost api:

xU03CmpM.UsXIZjH57dky13zb2byniaLrBZFyqO8V

### Obtain your UniFi API Key:

1. Sign in to the UniFi Site Manager at unifi.ui.com.
2. From the left navigation bar, click on API.
3. Click Create API Key.
4. Copy the key and store it securely, as it will only be displayed once.
5. Click Done to ensure the key is hashed and securely stored.


# Nodeboard Bulk Import Script
`add_nodes_generic.py`

This Python script allows you to import data from a CSV file into [Nodeboard](https://nodeboard.io), a digital asset tracking tool. It reads the CSV data, formats it into JSON, and posts it to Nodeboard via API for the specified team. Run this script from the command line for batch processing of multiple records.

## Prerequisites

- **Python 3.x**
- **Python Libraries**:
  - `csv`
  - `json`
  - `requests` (Install using `pip install requests` if not available)

## Usage

### 1. Prepare Your CSV File

Ensure your CSV file is formatted as follows, with headers:

- `hostname`: Name of the managed site
- `url`: URL associated with the site
- `ip_address`: IP address of the site
- `notes`: Additional notes for the site
- `description`: Description of the managed site
- `tags`: Comma-separated tags for categorization

#### Example CSV Content:

```csv
hostname,url,ip_address,notes,description,tags
"Example Site 1","http://example.com","192.168.1.1","Main server","Server","production,web"
"Example Site 2","http://example.org","192.168.1.2","Backup server","Server","backup,archive"
