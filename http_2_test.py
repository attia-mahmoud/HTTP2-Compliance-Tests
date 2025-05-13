import requests
import time
import json
import datetime
import os

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

tests_tree = "http_2_conformance.png"

################ VARIABLES #################

list_of_proxies = [
    # {"PROXY": "Direct", "PROXY_PORT": "8080"}
    # {"PROXY": "Apache-2.4.62", "PROXY_PORT": "7700"},
    # {"PROXY": "Caddy-2.9.1", "PROXY_PORT": "7701"},
    # {"PROXY": "Envoy-1.21.2", "PROXY_PORT": "8080"}
    {"PROXY": "HAproxy-3.2.0", "PROXY_PORT": "7700"},
    # {"PROXY": "Nginx-1.22.0", "PROXY_PORT": "7770", "tls_enabled": "true"}
    # {"PROXY": "Nghttpx-1.62.1", "PROXY_PORT": "7706"}
    # {"PROXY": "Node-20.16.0", "PROXY_PORT": "7707"}
    # {"PROXY": "Mitmproxy", "PROXY_PORT": "7708", "tls_enabled": "true"}
    # {"PROXY": "H2O-cf59e67c3", "PROXY_PORT": "7703", "tls_enabled": "false"}
    # {"PROXY": "Cloudflare", "PROXY_PORT": "443", "tls_enabled": "true", "cloudflare_origin": "true"},
    # {"PROXY": "Fastly", "PROXY_PORT": "443", "tls_enabled": "true"}
    # {"PROXY": "Traefik_old", "PROXY_PORT": "7715"},
    # {"PROXY": "Caddy_old", "PROXY_PORT": "7716"},
    # {"PROXY": "BunnyCDN", "PROXY_PORT": "443", "tls_enabled": "true"},
    # {"PROXY": "lighttpd-1.4.64", "PROXY_PORT": "7771"},
]

# CLIENT_WORKER = "linodejapan.admin.worker.nopasaran.org"
# SERVER_WORKER = "linodeaustralia.admin.worker.nopasaran.org"
# SERVER_PORT = "8080"
# PROXY_IP = "fastly.nopasaran.co"

CLIENT_WORKER = "labworker3.admin.worker.nopasaran.org"
SERVER_WORKER = "worker1.admin.worker.nopasaran.org"
PROXY_IP = "192.168.122.6"
SERVER_PORT = "8080"

MASTER = "master.admin.master.nopasaran.org"

file = "test_cases.json"

tests = []

################ VARIABLES #################


# Load test cases from test_cases.json
with open(file, 'r') as f:
    test_cases = json.load(f)

# Create results directory if it doesn't exist
if not os.path.exists('results'):
    os.makedirs('results')

# Function to run a single test case and return the result
def run_test_case(test_case, proxy, max_retries=3):
    print(f"\nRunning test case {test_case['id']}: {test_case['description']}")
    
    retry_count = 0
    while retry_count < max_retries:
        # Update variables with test case data
        variables = {
            "Root": {
                "Worker_1": {
                    "role": "client",
                    "client": "client",
                    "server": "server",
                    "host": PROXY_IP,
                    "port": proxy["PROXY_PORT"],
                    "tls_enabled": proxy.get("tls_enabled", "false"),
                    "protocol": "h2",
                    "connection_settings_client": test_case.get("connection_settings_client", {}),
                    "controller_conf_filename": "controller_configuration.json",
                    "cloudflare_origin": proxy.get("cloudflare_origin", "false"),
                    "client_frames": test_case.get("client_frames", [{"type": "HEADERS", "flags": {"END_STREAM": "true"}}]),
                    "server_frames": test_case.get("server_frames", [{"type": "HEADERS", "flags": {"END_STREAM": "true"}}]),
                },
                "Worker_2": {
                    "role": "server",
                    "client": "client",
                    "server": "server",
                    "host": "0.0.0.0",
                    "port": SERVER_PORT,
                    "tls_enabled": proxy.get("tls_enabled", "false"),
                    "protocol": "h2",
                    "connection_settings_server": test_case.get("connection_settings_server", {}),
                    "controller_conf_filename": "controller_configuration.json",
                    "cloudflare_origin": proxy.get("cloudflare_origin", "false"),
                    "client_frames": test_case.get("client_frames", [{"type": "HEADERS", "flags": {"END_STREAM": "true"}}]),
                    "server_frames": test_case.get("server_frames", [{"type": "HEADERS", "flags": {"END_STREAM": "true"}}]),
                }
            }
        }

        # Construct the payload for the task
        payload = {
            "master": MASTER,
            "first-worker": CLIENT_WORKER,
            "second-worker": SERVER_WORKER,
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
            response.raise_for_status()
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
                    
                    # Check if the test timed out
                    if has_timeout(result) and retry_count < max_retries - 1:
                        retry_count += 1
                        continue
                    
                    # If no timeout or max retries reached, return the result
                    return {
                        "description": test_case['description'],
                        "result": result
                    }
                else:
                    print("Failed to retrieve the final result.")
                    if retry_count < max_retries - 1:
                        retry_count += 1
                        continue
                    else:
                        return {
                            "description": test_case['description'],
                            "result": None
                        }
            else:
                print("No task ID returned.")
                if retry_count < max_retries - 1:
                    retry_count += 1
                    continue
                else:
                    return {
                        "description": test_case['description'],
                        "result": None
                    }

        except requests.exceptions.RequestException as e:
            print(response.content)
            print(f"Request failed: {e}")
            if retry_count < max_retries - 1:
                retry_count += 1
                continue
            else:
                return {
                    "description": test_case['description'],
                    "result": f"Error: {str(e)}"
                }

# Function to check if a test result has a timeout
def has_timeout(result):
    if not isinstance(result, dict):
        return False
    
    for worker, worker_data in result.items():
        if worker_data is None:
            return True
        if worker_data and worker_data.get('Variables', {}).get('controller_conf_filename', False):
            return True
        if worker_data and worker_data.get('State', '') == 'ERROR':
            return True
    return False

# Main execution logic
for proxy in list_of_proxies:
    # Create proxy-specific directory
    proxy_dir = os.path.join('results', proxy["PROXY"])
    if not os.path.exists(proxy_dir):
        os.makedirs(proxy_dir)

    timestamp = datetime.datetime.now().strftime("%d_%b_%H_%M")
    filename = f"{proxy_dir}/test_results_{timestamp}.json"
    
    # If specific tests are provided, load the most recent results file
    existing_results = {}
    if tests:
        # Find the most recent results file
        result_files = [f for f in os.listdir(proxy_dir) if f.startswith('test_results_')]
        if result_files:
            latest_file = max(result_files, key=lambda x: os.path.getmtime(os.path.join(proxy_dir, x)))
            with open(os.path.join(proxy_dir, latest_file), 'r') as f:
                existing_results = json.load(f)
            filename = os.path.join(proxy_dir, latest_file)
    
    all_results = existing_results.copy()
    
    # Determine which test cases to run
    test_cases_to_run = []
    if tests:
        test_cases_to_run = [tc for tc in test_cases if tc['id'] in tests]
    else:
        test_cases_to_run = test_cases

    for test_case in test_cases_to_run:
        # Run the test and get the result, with automatic retries for timeouts
        test_result = run_test_case(test_case, proxy)
        all_results[str(test_case['id'])] = test_result

        # Update results file after each test
        with open(filename, 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"Results updated in {filename}")

    print(f"\nAll tests completed. Results saved in {filename}")