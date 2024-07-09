import sys
import csv
import json
import requests

def read_csv(file_name):
    data_list = []
    try:
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Process tags
                if 'tags' in row:
                    row['tags'] = row['tags'].split(',')
                else:
                    row['tags'] = []
                data_list.append(row)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)
    return data_list

def main():
    if len(sys.argv) != 4:
        print("Error: Team name, API key, and CSV file name are required.")
        print("Usage: script.py <team_name> <api_key> <csv_file>")
        sys.exit(1)

    team_name = sys.argv[1]
    api_key = sys.argv[2]
    csv_file = sys.argv[3]
    url = f"https://nodeboard.io/a/{team_name}/n/api/managedsites/"

    data_list = read_csv(csv_file)

    for data in data_list:
        data_json = {
            "name": data.get("hostname", ""),
            "url": data.get("url", "http://example.com"),
            "ip_address": data.get("ip_address", ""),
            "notes": data.get("notes", "Some important notes that you want to add"),
            "description": data.get("description", "Laptop"),
            "tags": data.get("tags", [])
        }

        response = requests.post(url, headers={
            "Authorization": f"Api-Key {api_key}",
            "Content-Type": "application/json"
        }, data=json.dumps(data_json))

        if response.status_code not in (200, 201):
            print(f"Error: Failed to send data to Nodeboard (HTTP code {response.status_code}).")
            sys.exit(1)

    print("Data successfully sent to Nodeboard.")

if __name__ == "__main__":
    main()
