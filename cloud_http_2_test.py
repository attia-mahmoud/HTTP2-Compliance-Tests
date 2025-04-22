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

masters_url = f'{base_url}/operational-masters'
workers_url = f'{base_url}/operational-workers'
task_url = f'{base_url}/task'

# Fetch operational masters
masters = fetch_data(masters_url)
# Fetch operational workers
workers = fetch_data(workers_url)
print(masters)
print(workers)

repository = "https://github.com/nopasaran-org/nopasaran-tests-trees"

tests_tree = "http_2_conformance.png"

################ VARIABLES #################

list_of_proxies = [
    # {"PROXY": "Direct", "PROXY_PORT": "8080"}
    # {"PROXY": "ApacheTest", "PROXY_PORT": "7700"}
    # {"PROXY": "Caddy", "PROXY_PORT": "7701"},
    # {"PROXY": "Envoy", "PROXY_PORT": "7702"}
    # {"PROXY": "HAproxy", "PROXY_PORT": "7704"}
    # {"PROXY": "Nginx", "PROXY_PORT": "7705", "tls_enabled": "true"}
    # {"PROXY": "Nghttpx", "PROXY_PORT": "7706"}
    # {"PROXY": "Node", "PROXY_PORT": "7707"}
    # {"PROXY": "Mitmproxy", "PROXY_PORT": "7708", "tls_enabled": "true"}
    # {"PROXY": "H2O", "PROXY_PORT": "7709", "tls_enabled": "true"}
    {"PROXY": "Cloudflare", "PROXY_PORT": "443", "tls_enabled": "true", "cloudflare_origin": "true"},
    # {"PROXY": "Fastly", "PROXY_PORT": "80"}
]

list_of_workers = [
    {"WORKER": "linodeaustralia.admin.worker.nopasaran.org", "PORT": "443", "PROXY_IP": "australiacloudflare.nopasaran.co"},
    # {"WORKER": "linodegermany.admin.worker.nopasaran.org", "PORT": "443"},
    # {"WORKER": "linodeparis.admin.worker.nopasaran.org", "PORT": "443"},
    # {"WORKER": "linodelondon.admin.worker.nopasaran.org", "PORT": "443"},
    {"WORKER": "linodejapan.admin.worker.nopasaran.org", "PORT": "443", "PROXY_IP": "japancloudflare.nopasaran.co"},
    # {"WORKER": "linodelosangeles.admin.worker.nopasaran.org", "PORT": "443", "PROXY_IP": "losangelescloudflare.nopasaran.co"},
    {"WORKER": "linodegermany.admin.worker.nopasaran.org", "PORT": "443", "PROXY_IP": "germanycloudflare.nopasaran.co"},
]

CLIENT_WORKER = "linodeparis.admin.worker.nopasaran.org"
SERVER_WORKER = "linodeaustralia.admin.worker.nopasaran.org"
SERVER_PORT = "443"
PROXY_IP = "cloudflare.nopasaran.co"

# CLIENT_WORKER = "worker2.admin.worker.nopasaran.org"
# SERVER_WORKER = "worker1.admin.worker.nopasaran.org"
# PROXY_IP = "192.168.122.6"
# SERVER_PORT = "8080"

MASTER = "mahmoudmaster.admin.master.nopasaran.org"

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
def run_test_case(test_case, proxy, server_config, max_retries=3):
    print(f"\nRunning test case {test_case['id']}: {test_case['description']}")
    
    # Verify server has PROXY_IP configured
    if "PROXY_IP" not in server_config:
        print(f"Cannot run test: Server {server_config['WORKER']} missing PROXY_IP configuration")
        return None
    
    retry_count = 0
    while retry_count < max_retries:
        # Update variables with test case data
        variables = {
            "Root": {
                "Worker_1": {
                    "role": "client",
                    "client": "client",
                    "server": "server",
                    "host": server_config["PROXY_IP"],  # Use the server's PROXY_IP
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
                    "port": server_config["PORT"],
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

def is_worker_operational(worker_host, operational_workers):
    return worker_host in operational_workers

def is_master_operational(master_host, operational_masters):
    return master_host in operational_masters

def get_worker_pairs(workers_list):
    pairs = []
    for i in range(len(workers_list)):
        for j in range(len(workers_list)):
            if i != j:  # Don't pair a worker with itself
                pairs.append((workers_list[i], workers_list[j]))
    return pairs

def get_result_filename(proxy_dir, client_worker, server_worker, timestamp):
    # Create a filename using the worker pair information
    pair_name = f"{client_worker.split('.')[0]}_to_{server_worker.split('.')[0]}"
    return f"{proxy_dir}/test_results_{pair_name}_{timestamp}.json"

# Main execution logic
if not masters or not workers:
    print("Failed to fetch operational masters/workers list. Exiting.")
    exit(1)

operational_workers = workers
operational_masters = masters

if not is_master_operational(MASTER, operational_masters):
    print(f"Master {MASTER} is not operational. Exiting.")
    exit(1)

# Determine which workers to use
active_workers = []
if list_of_workers:
    # Validate each worker in the list
    for worker_config in list_of_workers:
        worker_host = worker_config["WORKER"]
        if is_worker_operational(worker_host, operational_workers):
            active_workers.append(worker_config)
        else:
            print(f"Worker {worker_host} is not operational, skipping.")
else:
    # Use default workers if they're operational
    if is_worker_operational(CLIENT_WORKER, operational_workers) and is_worker_operational(SERVER_WORKER, operational_workers):
        active_workers = [
            {"WORKER": CLIENT_WORKER, "PORT": SERVER_PORT},
            {"WORKER": SERVER_WORKER, "PORT": SERVER_PORT}
        ]
    else:
        print("Default workers are not operational. Exiting.")
        exit(1)

if len(active_workers) < 2:
    print("Not enough operational workers to run tests. Exiting.")
    exit(1)

# Get all possible worker pairs
worker_pairs = get_worker_pairs(active_workers)

for proxy in list_of_proxies:
    # Create proxy-specific directory
    proxy_dir = os.path.join('results', proxy["PROXY"])
    if not os.path.exists(proxy_dir):
        os.makedirs(proxy_dir)

    timestamp = datetime.datetime.now().strftime("%d_%b_%H_%M")
    
    # For each pair of workers
    for client_worker, server_worker in worker_pairs:
        # Generate filename for this worker pair
        filename = get_result_filename(proxy_dir, client_worker["WORKER"], server_worker["WORKER"], timestamp)
        
        # Initialize or load existing results for this pair
        if os.path.exists(filename) and tests:
            with open(filename, 'r') as f:
                all_results = json.load(f)
            test_counter = len([k for k in all_results.keys() if k != "metadata"])
        else:
            all_results = {
                "metadata": {
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "proxy": proxy["PROXY"],
                    "master": MASTER,
                    "client_worker": client_worker["WORKER"],
                    "server_worker": server_worker["WORKER"]
                }
            }
            test_counter = 0

        # Determine which test cases to run
        test_cases_to_run = []
        if tests:
            test_cases_to_run = [tc for tc in test_cases if tc['id'] in tests]
        else:
            test_cases_to_run = test_cases

        for test_case in test_cases_to_run:
            # Update the worker configuration for this test
            CLIENT_WORKER = client_worker["WORKER"]
            SERVER_WORKER = server_worker["WORKER"]
            
            # Skip if server worker doesn't have PROXY_IP configured
            if "PROXY_IP" not in server_worker:
                print(f"Skipping tests for {SERVER_WORKER} as PROXY_IP is not configured")
                continue
                
            # Run the test and get the result, with automatic retries for timeouts
            test_result = run_test_case(test_case, proxy, server_worker)
            
            # Create a new test entry with a numeric key
            test_counter += 1
            all_results[str(test_counter)] = {
                "test_id": test_case['id'],
                "description": test_case['description'],
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "result": test_result
            }

            # Update results file after each test
            with open(filename, 'w') as f:
                json.dump(all_results, f, indent=2)
            print(f"Results updated in {filename}")

        print(f"\nCompleted tests for worker pair: {client_worker['WORKER']} -> {server_worker['WORKER']}")

    print(f"\nAll tests completed for proxy {proxy['PROXY']}")