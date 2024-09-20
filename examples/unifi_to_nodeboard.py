import requests
import json

def get_hosts(api_key):
    headers = {'X-API-KEY': api_key}
    response = requests.get('https://api.ui.com/ea/hosts', headers=headers)
    try:
        return response.json()['data']
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        print("Response content:", response.text[:500])
        return []

def get_devices(api_key, host_ids):
    headers = {'X-API-KEY': api_key}
    devices_data = []
    for host_id in host_ids:
        params = {'hostIds[]': host_id}
        response = requests.get('https://api.ui.com/ea/devices', headers=headers, params=params)
        try:
            device_response = response.json()['data']
            for item in device_response:
                devices_data.extend(item['devices'])  # Assuming 'devices' is directly under each item
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON for host {host_id}:", e)
            print("Response content:", response.text[:500])
    return devices_data

def post_to_nodeboard(device, team_slug, api_key):
    # Define the base URL and API key
    base_url = "https://nodeboard.io"
    url = f"{base_url}/a/{team_slug}/n/api/managedsites/"
    
    # Prepare the data payload
    data_json = {
        "name": device.get('name', 'Unnamed Device'),
        "url": f"https://{device.get('ip', 'no-ip')}",
        "ip_address": device.get('ip', 'No IP assigned'),
        "notes": f"Unifi Networking: {device.get('name', 'no name')}",
        "description": "Managed device from Unifi",
        "tags": [
            device.get('model', ''),
            device.get('shortname', ''),
            device.get('status', ''),
            f"updateAvailable: {device.get('updateAvailable', 'false')}",
            device.get('version', '')
        ]
    }

    # Perform the POST request
    response = requests.post(url, headers={
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json",
    }, data=json.dumps(data_json))

    # Check if the request was successful
    if response.status_code in (200, 201):
        print(f"Managed site created successfully for device {device.get('name', 'Unnamed')}.")
    else:
        print(f"Failed to create managed site for device {device.get('name', 'Unnamed')}. HTTP Status code: {response.status_code}")
        print(response.text)

def main():
    api_key = 'unifi_api_key'
    team_slug = 'nodeboard_team_slug'
    nodeboard_api_key = 'nodeboard_api_key'
    hosts = get_hosts(api_key)
    host_ids = [host['id'] for host in hosts]

    devices = get_devices(api_key, host_ids)
    for device in devices:
        post_to_nodeboard(device, team_slug, nodeboard_api_key)

if __name__ == "__main__":
    main()
