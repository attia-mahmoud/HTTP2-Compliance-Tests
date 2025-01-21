import requests
import time
import json

def poll_status(status_url, interval=5, timeout=60):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(status_url)
            response.raise_for_status()  # Raise an error for HTTP errors

            data = response.json()
            status = data.get('status')

            if status == "completed":
                print("Task completed. Result:")
                print(data.get('result'))
                return data.get('result')
            elif status == "failed":
                print("Task failed. Error:")
                print(data.get('error'))
                return None
            else:
                print(f"Task status: {status}. Checking again in {interval} seconds...")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

        time.sleep(interval)

    print("Polling timed out.")
    return None

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Define the endpoint URLs
base_url = 'https://www.nopasaran.org/api/v1/tests-trees'

tests_trees_url = f'{base_url}/repository'
masters_url = f'{base_url}/operational-masters'
workers_url = f'{base_url}/operational-workers'
task_url = f'{base_url}/task'

# Fetch scenarios and repository
tests_trees_data = fetch_data(tests_trees_url)

repository = "https://github.com/nopasaran-org/nopasaran-tests-trees"

# PROXY_WITH_VERSION = "node"

CLIENT_WORKER = "linodeaustralia.admin.worker.nopasaran.org"
CLIENT_PORT = "7700"

SERVER_WORKER = "linodegermany.admin.worker.nopasaran.org"
# SERVER_IP = "cloudflare.nopasaran.co"
SERVER_IP = "172.104.229.16"
SERVER_PORT = "7700"

MASTER = "mahmoudmaster.admin.master.nopasaran.org"

# Use command-line arguments for workers and port
worker_1 = CLIENT_WORKER
worker_1_port = CLIENT_PORT
worker_2 = SERVER_WORKER
worker_2_ip = SERVER_IP
worker_2_port = SERVER_PORT
master = MASTER

tests_tree = "http_2_conformance.png"

# Construct the variables dictionary
variables = {
    "Root": {
        "Worker_1": {
            "role": "client",
            "client": "client",
            "server": "server",
            "host": worker_2_ip,
            "port": worker_1_port,
            "tls_enabled": "false",
            "protocol": "h2",
            "connection_settings_client": {},
            "controller_conf_filename": "controller_configuration.json",
            "client_frames": [
                {
                    "type": "HEADERS",
                    "tests": [
                        [
                            {
                                "function": "verifytype",
                                "params": [
                                    "RequestReceived"
                                ]
                            }
                        ]
                    ]
                }
            ],
            "server_frames": []
        },
        "Worker_2": {
            "role": "server",
            "client": "client",
            "server": "server",
            "host": worker_2_ip,
            "port": worker_2_port,
            "tls_enabled": "false",
            "protocol": "h2",
            "connection_settings_server": {},
            "controller_conf_filename": "controller_configuration.json",
            "client_frames": [],
            "server_frames": []
        }
    }
}

# Construct the payload for the task
payload = {
    "master": master,
    "first-worker": worker_1,
    "second-worker": worker_2,
    "repository": repository,
    "tests-tree": tests_tree,
    "variables": variables
}

# Convert payload to JSON string
payload_json = json.dumps(payload)

try:
    response = requests.post(
        task_url,
        data=payload_json,
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("Request succeeded. Response:")
    print(response.text)

    # Extract task ID from the response
    task_id = response.json().get('task_id')
    if task_id:
        status_url = f'{task_url}/{task_id}'
        print(f"Task URL: {status_url}")
        result = poll_status(status_url)

        if result:
            print("Final result retrieved:", result)
        else:
            print("Failed to retrieve the final result.")
    else:
        print("No task ID returned.")

except requests.exceptions.RequestException as e:
    print(response.content)
    print(f"Request failed: {e}")