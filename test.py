import json

with open('docs/clientside_vs_serverside.json', 'r') as f:
    test_filters = json.load(f)
    tests = test_filters['client_side_non_conformant_frames']

with open('results/Varnish/test_results_23_Apr_12_30.json', 'r') as f:
    all_results = json.load(f)

filtered_results = {}
for test_id, test_data in all_results.items():
    # Convert test_id (string key) to int for comparison with the list of integer IDs
    try:
        if int(test_id) in tests:
            filtered_results[test_id] = test_data
    except ValueError:
        # Handle cases where test_id might not be a valid integer string
        print(f"Warning: Could not convert test ID '{test_id}' to integer. Skipping.")

# print to new json file
with open('results/Varnish/test_results_23_Apr_12_30_filtered.json', 'w') as f:
    json.dump(filtered_results, f, indent=2)



