import requests
import time
import json
import os
from datetime import datetime

def poll_status(status_url, interval=5, timeout=60):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(status_url)
            response.raise_for_status()

            data = response.json()
            status = data.get('status')

            if status == "completed":
                return data.get('result')
            elif status == "failed":
                print(f"Task failed. Error: {data.get('error')}")
                return None
            else:
                print(f"Task status: {status}. Checking again in {interval} seconds...")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

        time.sleep(interval)

    print("Polling timed out.")
    return None

def run_test_case(test_case):
    MASTER = "mahmoudmaster.admin.master.nopasaran.org"

    WORKER_1 = "linodeaustralia.admin.worker.nopasaran.org"
    WORKER_1_PORT = "7700"

    WORKER_2 = "linodegermany.admin.worker.nopasaran.org"
    WORKER_2_IP = "172.104.229.16"
    WORKER_2_PORT = "7700"

    variables = {
        "master": MASTER,
        "first-worker": WORKER_1,
        "second-worker": WORKER_2,
        "repository": "https://github.com/nopasaran-org/nopasaran-tests-trees",
        "tests-tree": "http_2_conformance.png",
        "task_url": "https://www.nopasaran.org/api/v1/tests-trees/task",
        "variables": {
            "Root": {
                "Worker_1": {
                    "role": "client",
                    "client": "client",
                    "server": "server",
                    "host": WORKER_2_IP,
                    "port": WORKER_1_PORT,
                    "controller_conf_filename": "controller_configuration.json",
                    "tls_enabled": test_case.get("tls_enabled", False),
                    "tls_protocol": test_case.get("tls_protocol", "h2"),
                    "connection_settings_client": test_case.get("connection_settings_client", {}),
                    "connection_settings_server": test_case.get("connection_settings_server", {}),
                    "client_frames": test_case.get("client_frames", []),
                    "server_frames": test_case.get("server_frames", [])
                },
                "Worker_2": {
                    "role": "server",
                    "client": "client",
                    "server": "server",
                    "host": WORKER_2_IP,
                    "port": WORKER_2_PORT,
                    "controller_conf_filename": "controller_configuration.json",
                    "tls_enabled": test_case.get("tls_enabled", False),
                    "tls_protocol": test_case.get("tls_protocol", "h2"),
                    "connection_settings_client": test_case.get("connection_settings_client", {}),
                    "connection_settings_server": test_case.get("connection_settings_server", {}),
                    "client_frames": test_case.get("client_frames", []),
                    "server_frames": test_case.get("server_frames", [])
                }
            }
        }
    }

    payload = {
        "master": MASTER,
        "first-worker": WORKER_1,
        "second-worker": WORKER_2,
        "repository": "https://github.com/nopasaran-org/nopasaran-tests-trees",
        "tests-tree": "http_2_conformance.png",
        "variables": variables
    }

    try:
        response = requests.post(
            "https://www.nopasaran.org/api/v1/tests-trees/task",
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        
        task_id = response.json().get('task_id')
        if task_id:
            status_url = f'https://www.nopasaran.org/api/v1/tests-trees/task/{task_id}'
            return poll_status(status_url)
        
    except requests.exceptions.RequestException as e:
        print(f"Test case {test_case['id']} failed: {e}")
        return None

def main():
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')

    # Load test cases
    with open('test_cases.json', 'r') as f:
        test_cases = json.load(f)

    # Create log file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'results/test_results_{timestamp}.json'
    
    results = {}
    
    # Run each test case
    for test_case in test_cases:
        print(f"Running test case {test_case['id']}: {test_case['description']}")
        result = run_test_case(test_case)
        results[test_case['id']] = {
            'description': test_case['description'],
            'result': result
        }
        
        # Write results to file after each test
        with open(log_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Wait between tests to avoid overwhelming the server
        time.sleep(2)

    print(f"All test results have been saved to {log_file}")

if __name__ == "__main__":
    main()