import requests
import yaml
import re
# Define the base URL and API key
base_url = "https://nodeboard.io"
team_slug = "TeamNameHere"
api_key = "APIKEYHERE"


# Define the endpoint URL
url = f"{base_url}/a/{team_slug}/n/api/managedsites/"

def is_valid_group_name(tag):
    # Exclude tags that look like IP addresses
    ip_regex = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
    if ip_regex.match(tag):
        return False
    # Exclude tags that start with 'Port:' or 'HD'
    if tag.startswith('Port:') or tag.startswith('HD'):
        return False
    # Exclude tags that contain spaces or special characters
    if not re.match(r'^[A-Za-z0-9_-]+$', tag):
        return False
    # Optionally, exclude tags that are too long or too short
    if len(tag) < 2 or len(tag) > 50:
        return False
    # Otherwise, the tag is valid
    return True

def main():
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes

    data = response.json()

    # Initialize the inventory dictionary
    inventory = {'all': {'hosts': {}, 'children': {}}}

    # Iterate over each host in the results
    for host in data.get('results', []):
        name = host.get('name')
        ip_address = host.get('ip_address')
        tags = host.get('tags', [])

        # Add the host to the 'all' group
        inventory['all']['hosts'][name] = {'ansible_host': ip_address}

        # Add the host to groups based on valid tags
        for tag in tags:
            if is_valid_group_name(tag):
                if tag not in inventory['all']['children']:
                    inventory['all']['children'][tag] = {'hosts': {}}
                inventory['all']['children'][tag]['hosts'][name] = {'ansible_host': ip_address}
            else:
                print(f"Skipping invalid tag '{tag}' for host '{name}'")

    # Write the inventory to a YAML file
    with open('inventory.yml', 'w') as f:
        yaml.dump(inventory, f, default_flow_style=False)

    print("Inventory has been written to inventory.yml")

if __name__ == "__main__":
    main()
