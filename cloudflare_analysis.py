import json
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from summarize_outputs import analyze_results


def analyze_cloudflare_result(filename):
    """
    Modified version of analyze_results that handles the nested result structure
    specifically found in Cloudflare test results.
    
    Args:
        filename: Path to the JSON result file
        
    Returns:
        The same tuple as analyze_results
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # drop the 0th entry
    if '0' in data:
        del data['0']
    
    dropped_count = 0
    received_count = 0
    goaway_count = 0
    reset_count = 0
    error_500_count = 0
    modified_count = 0
    unmodified_count = 0
    test_results = {}
    test_messages = {}
    
    for test_id, test_data in data.items():
        if test_id == 'metadata':
            continue
            
        # Handle nested result structure in Cloudflare files
        if not test_data or not test_data.get('result'):
            test_results[test_id] = "other"
            test_messages[test_id] = "No result data"
            continue
        
        # Extract the actual result, handling nested structure if needed
        result = test_data['result']
        if isinstance(result, dict) and 'result' in result and isinstance(result['result'], dict):
            result = result['result']
        
        if isinstance(result, str):
            # skip this test
            continue
        
        # The rest of the function is identical to analyze_results
        is_goaway = False
        is_reset = False
        is_500 = False
        is_dropped = False
        is_received = False
        is_modified = False
        is_unmodified = False
        message = ""
        
        # Use safer access methods for worker data
        worker1 = result.get('Worker_1', {}) or {}
        worker2 = result.get('Worker_2', {}) or {}
        
        vars1 = worker1.get('Variables', {}) or {}
        vars2 = worker2.get('Variables', {}) or {}

        if vars2.get('result', '').startswith('Received'):
            if test_id in ['4', '87', '126', '165']:
                is_modified = True
            elif test_id in ['8', '110', '151', '7', '83']:
                is_unmodified = True
            else:
                is_unmodified = True
            message = vars2['result']
        
        elif vars1.get('client_result', '') == 'Test result: MODIFIED' or vars1.get('result', '') == 'Test result: MODIFIED':
            is_modified = True
            message = vars1.get('client_result', vars1.get('result', ''))
        elif vars1.get('client_result', '') == 'Test result: UNMODIFIED' or vars1.get('result', '') == 'Test result: UNMODIFIED':
            is_unmodified = True
            message = vars1.get('client_result', vars1.get('result', ''))

        elif vars2.get('server_result', '') == 'Test result: MODIFIED':
            is_modified = True
            message = vars2['server_result']
        elif vars2.get('server_result', '') == 'Test result: UNMODIFIED':
            is_unmodified = True
            message = vars2['server_result']
            
        elif worker1 and worker1.get('State', '') == 'GOAWAY_RECEIVED':
            is_goaway = True
            message = vars1['msg'] if vars1.get('msg', '') else vars1['client_result']
        elif worker2 and worker2.get('State', '') == 'GOAWAY_RECEIVED':
            is_goaway = True
            message = vars2['msg'] if vars2.get('msg', '') else vars2['server_result']
        elif worker1 and worker1.get('State', '') == 'REJECTED':
            is_500 = True
            message = vars1['msg'] if vars1.get('msg', '') else vars1['client_result']
        elif worker2 and worker2.get('State', '') == 'REJECTED':
            is_500 = True
            message = vars2['server_result']
        elif worker1 and worker1.get('State', '') == 'RESET_RECEIVED':
            if vars1.get('msg'):
                is_reset = True
                message = vars1['msg']
            elif vars1.get('client_result'):
                is_reset = True
                message = vars1['client_result']
        elif worker2 and worker2.get('State', '') == 'RESET_RECEIVED':
            if vars2.get('msg'):
                is_reset = True
                message = vars2['msg']
            elif vars2.get('server_result'):
                is_reset = True
                message = vars2['server_result']
        elif vars1 and vars1.get('client_result', '').startswith('Successfully received all') and vars1.get('server_result', '').startswith('Successfully received all'):
            if test_id in ['4', '87', '126', '165']:
                is_modified = True
            elif test_id in ['8', '110', '151', '7', '83']:
                is_unmodified = True
            else:
                is_unmodified = True
            message = vars1['client_result']
        elif vars2 and vars2.get('client_result', '').startswith('Successfully received all')and vars2.get('server_result', '').startswith('Successfully received all'):
            if test_id in ['4', '87', '126', '165']:
                is_modified = True
            elif test_id in ['8', '110', '151', '7', '83']:
                is_unmodified = True
            else:
                is_unmodified = True
            message = vars2['server_result']
        elif vars2.get('msg', '').startswith("Timeout occurred after 5.0s while waiting for client connection"):
            is_dropped = True
            message = vars2['msg']
        elif worker1 and worker1.get('State', '') in ['CONTROL_CHANNEL_TIMEOUT_AFTER_CLIENT_FRAMES_SENT_CLIENT', 'CONTROL_CHANNEL_TIMEOUT_AFTER_SERVER_FRAMES_SENT_CLIENT']:
            is_dropped = True
            message = vars1['msg']
        elif worker2 and worker2.get('State', '') in ['CONTROL_CHANNEL_TIMEOUT_AFTER_CLIENT_FRAMES_SENT_SERVER', 'CONTROL_CHANNEL_TIMEOUT_AFTER_SERVER_FRAMES_SENT_SERVER']:
            is_dropped = True
            message = vars2['msg']
        else:
            is_dropped = True
            message = "Unknown error"

        # Store results
        if is_modified:
            test_results[test_id] = "modified"
            modified_count += 1
        elif is_unmodified:
            test_results[test_id] = "unmodified"
            unmodified_count += 1
        elif is_dropped:
            test_results[test_id] = "dropped"
            dropped_count += 1
        elif is_reset:
            test_results[test_id] = "reset"
            reset_count += 1
        elif is_500:
            test_results[test_id] = "500"
            error_500_count += 1
        elif is_goaway:
            test_results[test_id] = "goaway"
            goaway_count += 1
        elif is_received:
            test_results[test_id] = "received"
            received_count += 1
        else:
            test_results[test_id] = "other"
        
        test_messages[test_id] = message
    
    return dropped_count, error_500_count, goaway_count, reset_count, received_count, modified_count, unmodified_count, test_results, test_messages


def load_cloudflare_results(results_dir='results'):
    """
    Load Cloudflare test results from the Cloudflare directory.
    
    Args:
        results_dir: Base directory containing the results folder.
        
    Returns:
        A dictionary mapping variant names to their test results.
    """
    cloudflare_dir = os.path.join(results_dir, 'Cloudflare')
    if not os.path.exists(cloudflare_dir):
        print(f"Cloudflare results directory not found at {cloudflare_dir}")
        return {}
    
    # Get all JSON files in the directory
    json_files = [f for f in os.listdir(cloudflare_dir) if f.endswith('.json')]
    if not json_files:
        print("No Cloudflare test result files found")
        return {}
    
    all_test_results = {}
    
    for file_name in json_files:
        file_path = os.path.join(cloudflare_dir, file_name)
        try:
            # Extract variant info from the file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Generate variant name based on metadata
            if 'metadata' in data:
                metadata = data['metadata']
                client = metadata.get('client_worker', 'unknown_client')
                server = metadata.get('server_worker', 'unknown_server')
                date = metadata.get('date', 'unknown_date')
                
                # Create a variant name based on client-server pair
                client_location = extract_location(client)
                server_location = extract_location(server)
                variant_name = f"CF-{client_location}-to-{server_location}-{date.split(' ')[0]}"
            else:
                # For older files without metadata, use the filename
                variant_name = f"CF-{os.path.splitext(file_name)[0]}"
            
            # Use the special analyze function that handles nested result structure
            _, _, _, _, _, _, _, test_results, _ = analyze_cloudflare_result(file_path)
            
            all_test_results[variant_name] = test_results
            print(f"Loaded {len(test_results)} test results for {variant_name}")
                
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    
    return all_test_results


def extract_location(worker_string):
    """Extract location from worker string."""
    if not worker_string or worker_string == 'unknown_client' or worker_string == 'unknown_server':
        return 'unknown'
    
    # Try to extract location from worker name
    # Example: linodeaustralia.admin.worker.nopasaran.org
    parts = worker_string.split('.')
    if parts and len(parts) > 0:
        location = parts[0]
        # Remove 'linode' prefix if present
        if location.startswith('linode'):
            location = location[6:]
        return location
    
    return 'unknown'


def compare_cloudflare_variants(all_test_results, summaries_dir):
    """
    Compare test results between Cloudflare variants and identify differences.
    
    Args:
        all_test_results: Dictionary mapping variant names to their test results
        summaries_dir: Directory to save the output report
    """
    # Check if we have enough variants to compare
    if len(all_test_results) < 2:
        print("Not enough Cloudflare variants to compare")
        return
    
    # Get the list of all variants
    all_variants = list(all_test_results.keys())
    print(f"Found {len(all_variants)} Cloudflare variants to compare: {', '.join(all_variants)}")
    
    # Get the common test IDs across all variants
    common_test_ids = set()
    for variant in all_variants:
        if common_test_ids:
            common_test_ids &= set(all_test_results[variant].keys())
        else:
            common_test_ids = set(all_test_results[variant].keys())
    
    print(f"Found {len(common_test_ids)} common test IDs across all variants")
    
    # Find tests with different outcomes
    different_outcomes = {}
    for test_id in common_test_ids:
        # Collect results for this test across variants
        test_results = {variant: all_test_results[variant][test_id] for variant in all_variants}
        
        # Check if there are differences
        if len(set(test_results.values())) > 1:
            different_outcomes[test_id] = test_results
    
    print(f"Found {len(different_outcomes)} tests with different outcomes")
    
    # Load test descriptions
    try:
        with open('test_cases.json', 'r') as f:
            test_cases = json.load(f)
        test_descriptions = {str(case['id']): case['description'] for case in test_cases}
    except Exception as e:
        print(f"Warning: Could not load test descriptions from test_cases.json: {e}")
        test_descriptions = {}
    
    # Create the output file
    output_file = os.path.join(summaries_dir, "cloudflare_variant_differences.txt")
    
    with open(output_file, 'w') as f:
        f.write("# Differences Between Cloudflare Variants\n\n")
        f.write(f"Comparing {', '.join(all_variants)}\n\n")
        f.write(f"Total tests with different outcomes: {len(different_outcomes)}\n\n")
        
        # Sort test IDs numerically
        sorted_test_ids = sorted(different_outcomes.keys(), key=lambda x: int(x) if x.isdigit() else float('inf'))
        
        for test_id in sorted_test_ids:
            description = test_descriptions.get(test_id, "No description available")
            results = different_outcomes[test_id]
            
            f.write(f"## Test {test_id}: {description}\n\n")
            
            # Create a table for this test
            f.write("| Variant | Outcome |\n")
            f.write("|---------|--------|\n")
            
            for variant in all_variants:
                f.write(f"| {variant} | {results[variant]} |\n")
            
            f.write("\n")

    return different_outcomes


def create_cloudflare_correlation_matrix(all_test_results, output_directory):
    """
    Create a Pearson correlation matrix visualization specifically for Cloudflare variants.
    
    Args:
        all_test_results: Dictionary mapping variant names to their test results
        output_directory: Directory to save the visualization
    """
    os.makedirs(output_directory, exist_ok=True)
    
    # Get the list of all variants
    all_variants = list(all_test_results.keys())
    
    if len(all_variants) < 2:
        print("Not enough Cloudflare variants to create correlation matrix")
        return
    
    # Get test IDs from all variants
    test_ids = sorted(list(set().union(*[results.keys() for results in all_test_results.values()])),
                     key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    # Create matrix data with the same encoding as the original function
    matrix_data = np.zeros((len(all_variants), len(test_ids)))
    for i, variant in enumerate(all_variants):
        for j, test_id in enumerate(test_ids):
            # Convert result to numeric value with better separation
            result = all_test_results[variant].get(test_id, "other")
            if result == "received":
                matrix_data[i][j] = 4  # Success
            elif result == "reset":
                matrix_data[i][j] = 3  # Reset
            elif result == "goaway":
                matrix_data[i][j] = 2  # Goaway
            elif result == "500":
                matrix_data[i][j] = 1  # 500 error
            elif result == "dropped":
                matrix_data[i][j] = 0  # Failure
            else:  # other
                matrix_data[i][j] = np.nan  # Use NaN to exclude "other" from correlation
    
    # Calculate correlation matrix with better NaN handling
    correlation_matrix = np.zeros((len(all_variants), len(all_variants)))
    std_devs = np.zeros(len(all_variants))
    
    # First check which variants have non-zero standard deviation
    for i in range(len(all_variants)):
        # Calculate std dev, ignoring NaNs
        valid_data = matrix_data[i, ~np.isnan(matrix_data[i, :])]
        if len(valid_data) > 0:
            std_devs[i] = np.std(valid_data)
    
    # Create text matrix to display actual values
    text_matrix = np.empty((len(all_variants), len(all_variants)), dtype=object)
    
    # Calculate correlations
    for i in range(len(all_variants)):
        for j in range(len(all_variants)):
            # Fill diagonal with 1.0
            if i == j:
                correlation_matrix[i, j] = 1.0
                text_matrix[i, j] = "1.00"
                continue
                
            # Check if there's enough data to compare
            valid_indices = ~(np.isnan(matrix_data[i]) | np.isnan(matrix_data[j]))
            valid_count = np.sum(valid_indices)
            
            # Skip if not enough valid data points
            if valid_count < 2:
                correlation_matrix[i, j] = np.nan
                text_matrix[i, j] = "---"
                continue
            
            # Check for zero standard deviation
            if std_devs[i] == 0 or std_devs[j] == 0:
                # Check if data is identical
                identical = np.array_equal(
                    matrix_data[i, valid_indices],
                    matrix_data[j, valid_indices]
                )
                
                if identical:
                    correlation_matrix[i, j] = 1.0
                    text_matrix[i, j] = "SAME"
                else:
                    correlation_matrix[i, j] = np.nan
                    text_matrix[i, j] = "---"
            else:
                # Normal correlation calculation
                try:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        corr = np.corrcoef(
                            matrix_data[i, valid_indices], 
                            matrix_data[j, valid_indices]
                        )[0, 1]
                    
                    correlation_matrix[i, j] = corr
                    text_matrix[i, j] = f"{corr:.2f}"
                except Exception:
                    correlation_matrix[i, j] = np.nan
                    text_matrix[i, j] = "ERR"
    
    # Create figure with adequate size for the labels
    plt.figure(figsize=(max(12, len(all_variants)*1.5), max(10, len(all_variants))))
    
    # Create heatmap with masked NaN values
    masked_matrix = np.ma.masked_invalid(correlation_matrix)
    im = plt.imshow(masked_matrix, cmap='coolwarm', aspect='equal', vmin=-1, vmax=1)
    
    # Add colorbar
    plt.colorbar(im)
    
    # Configure ticks and labels
    plt.xticks(np.arange(len(all_variants)), all_variants, rotation=45, ha='right', fontsize=9)
    plt.yticks(np.arange(len(all_variants)), all_variants, fontsize=9)
    
    # Add correlation values as text
    for i in range(len(all_variants)):
        for j in range(len(all_variants)):
            plt.text(j, i, text_matrix[i, j],
                   ha='center', va='center', 
                   color='black' if text_matrix[i, j] in ["SAME", "---", "ERR"] else None)
            
            # Make text white for dark background
            if text_matrix[i, j] not in ["SAME", "---", "ERR"] and correlation_matrix[i, j] > 0.5:
                plt.gca().texts[-1].set_color('white')
    
    plt.title('Cloudflare Variants Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save the plot
    filename = 'cloudflare_correlation_matrix.png'
    plt.savefig(os.path.join(output_directory, filename), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Return some stats for debugging
    return {
        "total_variants": len(all_variants),
        "valid_correlations": np.sum(~np.isnan(correlation_matrix)),
        "nan_correlations": np.sum(np.isnan(correlation_matrix)),
        "identical_variants": np.sum(text_matrix == "SAME") 
    }


def create_cloudflare_test_variance_chart(all_test_results, output_directory):
    """
    Create a visualization showing which tests vary between different Cloudflare variants.
    
    Args:
        all_test_results: Dictionary mapping variant names to their test results
        output_directory: Directory to save the visualization
    """
    os.makedirs(output_directory, exist_ok=True)
    
    # Get the list of all variants
    all_variants = list(all_test_results.keys())
    
    if len(all_variants) < 2:
        print("Not enough Cloudflare variants to create test variance chart")
        return
    
    # Get all test IDs across all variants
    all_test_ids = set()
    for results in all_test_results.values():
        all_test_ids.update(results.keys())
    
    # Sort test IDs numerically
    sorted_test_ids = sorted(all_test_ids, key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    # Create a matrix of test results
    # 0 = not applicable/missing, 1 = dropped, 2 = 500, 3 = goaway, 4 = reset, 5 = unmodified, 6 = modified
    result_map = {
        "dropped": 1, 
        "500": 2, 
        "goaway": 3, 
        "reset": 4, 
        "unmodified": 5, 
        "modified": 6,
        "received": 7
    }
    
    # Create a matrix of test results
    result_matrix = np.zeros((len(all_variants), len(sorted_test_ids)))
    
    for i, variant in enumerate(all_variants):
        for j, test_id in enumerate(sorted_test_ids):
            if test_id in all_test_results[variant]:
                result = all_test_results[variant][test_id]
                result_matrix[i, j] = result_map.get(result, 0)
    
    # Calculate variance for each test
    test_variance = np.zeros(len(sorted_test_ids))
    for j in range(len(sorted_test_ids)):
        # Get non-zero values for this test
        test_values = result_matrix[:, j]
        non_zero = test_values[test_values > 0]
        if len(non_zero) > 1:
            # Check if there's more than one unique value
            unique_values = np.unique(non_zero)
            if len(unique_values) > 1:
                test_variance[j] = 1  # Mark as having variance
    
    # Filter to only include tests with variance
    variant_indices = np.where(test_variance > 0)[0]
    if len(variant_indices) == 0:
        print("No tests with variance found")
        return
    
    variant_test_ids = [sorted_test_ids[i] for i in variant_indices]
    variant_matrix = result_matrix[:, variant_indices]
    
    # Create a colormap for different result types
    colors = ['#f0f0f0', '#ff6b6b', '#ffd93d', '#ff9f43', '#6c5ce7', '#4ecdc4', '#2ecc71', '#6bceff']
    cmap = plt.matplotlib.colors.ListedColormap(colors)
    bounds = np.arange(0, 9) - 0.5
    norm = plt.matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    
    # Create the figure
    fig_width = max(12, len(variant_test_ids) * 0.4)
    fig_height = max(8, len(all_variants) + 2)
    plt.figure(figsize=(fig_width, fig_height))
    
    # Create the heatmap
    im = plt.imshow(variant_matrix, cmap=cmap, norm=norm, aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im, ticks=range(8))
    cbar.set_ticklabels(['N/A', 'dropped', '500', 'goaway', 'reset', 'unmodified', 'modified', 'received'])
    
    # Configure ticks and labels
    plt.xticks(np.arange(len(variant_test_ids)), variant_test_ids, rotation=90, fontsize=8)
    plt.yticks(np.arange(len(all_variants)), all_variants, fontsize=9)
    
    plt.title('Cloudflare Test Result Variance', fontsize=14, fontweight='bold')
    plt.xlabel('Test ID', fontsize=12)
    plt.ylabel('Cloudflare Variant', fontsize=12)
    
    plt.tight_layout()
    
    # Save the plot
    filename = 'cloudflare_test_variance.png'
    plt.savefig(os.path.join(output_directory, filename), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create a summary file listing the tests with variance
    try:
        with open('test_cases.json', 'r') as f:
            test_cases = json.load(f)
        test_descriptions = {str(case['id']): case['description'] for case in test_cases}
    except Exception as e:
        print(f"Warning: Could not load test descriptions from test_cases.json: {e}")
        test_descriptions = {}
    
    # Create the output file
    output_file = os.path.join(output_directory, "cloudflare_variant_test_differences.txt")
    
    with open(output_file, 'w') as f:
        f.write("# Tests with Result Variance Between Cloudflare Variants\n\n")
        f.write(f"Total tests with variance: {len(variant_test_ids)}\n\n")
        
        for test_id in variant_test_ids:
            description = test_descriptions.get(test_id, "No description available")
            f.write(f"## Test {test_id}: {description}\n\n")
            
            # Create a table for this test
            f.write("| Variant | Outcome |\n")
            f.write("|---------|--------|\n")
            
            for variant in all_variants:
                result = all_test_results[variant].get(test_id, "N/A")
                f.write(f"| {variant} | {result} |\n")
            
            f.write("\n")
    
    return {
        "total_tests": len(sorted_test_ids),
        "tests_with_variance": len(variant_test_ids),
        "variance_percentage": (len(variant_test_ids) / len(sorted_test_ids)) * 100
    }


def create_grouped_correlation_matrix(all_test_results, output_directory):
    """
    Create a custom correlation matrix visualization that groups Cloudflare variants by location pairs,
    showing multiple dates for each location pair in a grid of subplots.
    
    Args:
        all_test_results: Dictionary mapping variant names to their test results
        output_directory: Directory to save the visualization
    """
    os.makedirs(output_directory, exist_ok=True)
    
    # Get the list of all variants
    all_variants = list(all_test_results.keys())
    
    if len(all_variants) < 2:
        print("Not enough Cloudflare variants to create grouped correlation matrix")
        return
    
    # Parse the variant names to extract location pairs and dates
    location_pairs = {}
    for variant in all_variants:
        # Expected format: CF-location1-to-location2-YYYY-MM-DD
        parts = variant.split('-')
        if len(parts) >= 5 and parts[1] and parts[3]:
            # Extract the location pair and date
            location_pair = f"{parts[1]}-to-{parts[3]}"
            date = "-".join(parts[4:])  # Handle dates that might contain additional hyphens
            
            if location_pair not in location_pairs:
                location_pairs[location_pair] = []
            location_pairs[location_pair].append((variant, date))
    
    # Sort the location pairs for consistent ordering
    sorted_location_pairs = sorted(location_pairs.keys())
    
    # Get test IDs from all variants
    test_ids = sorted(list(set().union(*[results.keys() for results in all_test_results.values()])),
                    key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    # Create matrix data with the same encoding as the original function
    matrix_data = {}
    for variant in all_variants:
        matrix_data[variant] = np.zeros(len(test_ids))
        for j, test_id in enumerate(test_ids):
            # Convert result to numeric value with better separation
            result = all_test_results[variant].get(test_id, "other")
            if result == "received":
                matrix_data[variant][j] = 4  # Success
            elif result == "reset":
                matrix_data[variant][j] = 3  # Reset
            elif result == "goaway":
                matrix_data[variant][j] = 2  # Goaway
            elif result == "500":
                matrix_data[variant][j] = 1  # 500 error
            elif result == "dropped":
                matrix_data[variant][j] = 0  # Failure
            else:  # other
                matrix_data[variant][j] = np.nan  # Use NaN to exclude "other" from correlation
    
    # Calculate correlation matrix
    correlation_values = {}
    for variant1 in all_variants:
        correlation_values[variant1] = {}
        for variant2 in all_variants:
            # Skip self-correlations
            if variant1 == variant2:
                correlation_values[variant1][variant2] = 1.0
                continue
                
            # Get valid indices (non-NaN in both variants)
            valid_indices = ~(np.isnan(matrix_data[variant1]) | np.isnan(matrix_data[variant2]))
            valid_count = np.sum(valid_indices)
            
            # Skip if not enough valid data points
            if valid_count < 2:
                correlation_values[variant1][variant2] = np.nan
                continue
            
            # Calculate standard deviations, ignoring NaNs
            std_dev1 = np.std(matrix_data[variant1][valid_indices])
            std_dev2 = np.std(matrix_data[variant2][valid_indices])
            
            # Check for zero standard deviation
            if std_dev1 == 0 or std_dev2 == 0:
                # Check if data is identical
                identical = np.array_equal(
                    matrix_data[variant1][valid_indices],
                    matrix_data[variant2][valid_indices]
                )
                
                if identical:
                    correlation_values[variant1][variant2] = 1.0
                else:
                    correlation_values[variant1][variant2] = np.nan
            else:
                # Normal correlation calculation
                try:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        corr = np.corrcoef(
                            matrix_data[variant1][valid_indices], 
                            matrix_data[variant2][valid_indices]
                        )[0, 1]
                    
                    correlation_values[variant1][variant2] = corr
                except Exception:
                    correlation_values[variant1][variant2] = np.nan
    
    # Determine grid dimensions based on number of location pairs
    grid_size = int(np.ceil(np.sqrt(len(sorted_location_pairs))))
    
    # Create figure
    fig = plt.figure(figsize=(grid_size * 6, grid_size * 5))
    fig.suptitle('Cloudflare Variants Correlation Matrix by Location', fontsize=16, fontweight='bold')
    
    # Create a subplot for each location pair
    for idx, location_pair in enumerate(sorted_location_pairs):
        variants_in_pair = [v[0] for v in location_pairs[location_pair]]
        
        # Create subplot
        ax = fig.add_subplot(grid_size, grid_size, idx + 1)
        
        # Create matrix for this location pair
        n_variants = len(variants_in_pair)
        pair_matrix = np.zeros((n_variants, n_variants))
        
        # Fill matrix with correlation values
        for i, variant1 in enumerate(variants_in_pair):
            for j, variant2 in enumerate(variants_in_pair):
                pair_matrix[i, j] = correlation_values[variant1][variant2]
        
        # Create heatmap
        masked_matrix = np.ma.masked_invalid(pair_matrix)
        im = ax.imshow(masked_matrix, cmap='coolwarm', aspect='equal', vmin=-1, vmax=1)
        
        # Label the axes with dates only (more compact)
        date_labels = [v[1] for v in location_pairs[location_pair]]
        ax.set_xticks(np.arange(n_variants))
        ax.set_yticks(np.arange(n_variants))
        ax.set_xticklabels(date_labels, rotation=45, ha='right', fontsize=7)
        ax.set_yticklabels(date_labels, fontsize=7)
        
        # Set title for this subplot
        ax.set_title(location_pair, fontsize=10)
        
        # Add correlation values as text
        for i in range(n_variants):
            for j in range(n_variants):
                value = pair_matrix[i, j]
                if np.isnan(value):
                    text = "---"
                elif i == j:
                    text = "1.00"
                else:
                    text = f"{value:.2f}"
                
                ax.text(j, i, text, ha='center', va='center', fontsize=8,
                        color='white' if not np.isnan(value) and 0.3 < value < 0.7 else 'black')
    
    # Add colorbar to the figure
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Correlation Coefficient')
    
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    # Save the plot
    filename = 'cloudflare_grouped_correlation_matrix.png'
    plt.savefig(os.path.join(output_directory, filename), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        "total_location_pairs": len(sorted_location_pairs),
        "total_variants": len(all_variants)
    }


def create_cross_location_correlation_matrix(all_test_results, output_directory):
    """
    Create a comprehensive correlation matrix that shows both within-location and
    cross-location correlations between different Cloudflare test variants.
    
    Args:
        all_test_results: Dictionary mapping variant names to their test results
        output_directory: Directory to save the visualization
    """
    os.makedirs(output_directory, exist_ok=True)
    
    # Get the list of all variants
    all_variants = list(all_test_results.keys())
    
    if len(all_variants) < 2:
        print("Not enough Cloudflare variants to create cross-location correlation matrix")
        return
    
    # Parse the variant names to extract location pairs and dates
    location_pairs = {}
    for variant in all_variants:
        # Expected format: CF-location1-to-location2-YYYY-MM-DD
        parts = variant.split('-')
        if len(parts) >= 5 and parts[1] and parts[3]:
            # Extract the location pair and date
            location_pair = f"{parts[1]}-to-{parts[3]}"
            date = "-".join(parts[4:])  # Handle dates that might contain additional hyphens
            
            if location_pair not in location_pairs:
                location_pairs[location_pair] = []
            location_pairs[location_pair].append((variant, date))
    
    # Sort the location pairs for consistent ordering
    sorted_location_pairs = sorted(location_pairs.keys())
    
    # Get test IDs from all variants
    test_ids = sorted(list(set().union(*[results.keys() for results in all_test_results.values()])),
                    key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    # Create matrix data with the same encoding as the original function
    matrix_data = {}
    for variant in all_variants:
        matrix_data[variant] = np.zeros(len(test_ids))
        for j, test_id in enumerate(test_ids):
            # Convert result to numeric value with better separation
            result = all_test_results[variant].get(test_id, "other")
            if result == "modified":
                matrix_data[variant][j] = 6  # Modified
            elif result == "unmodified":
                matrix_data[variant][j] = 5  # Unmodified
            elif result == "received":
                matrix_data[variant][j] = 4  # Success
            elif result == "reset":
                matrix_data[variant][j] = 3  # Reset
            elif result == "goaway":
                matrix_data[variant][j] = 2  # Goaway
            elif result == "500":
                matrix_data[variant][j] = 1  # 500 error
            elif result == "dropped":
                matrix_data[variant][j] = 0  # Failure
            else:  # other
                matrix_data[variant][j] = np.nan  # Use NaN to exclude "other" from correlation
    
    # Calculate correlation matrix
    correlation_values = {}
    for variant1 in all_variants:
        correlation_values[variant1] = {}
        for variant2 in all_variants:
            # Skip self-correlations
            if variant1 == variant2:
                correlation_values[variant1][variant2] = 1.0
                continue
                
            # Get valid indices (non-NaN in both variants)
            valid_indices = ~(np.isnan(matrix_data[variant1]) | np.isnan(matrix_data[variant2]))
            valid_count = np.sum(valid_indices)
            
            # Skip if not enough valid data points
            if valid_count < 2:
                correlation_values[variant1][variant2] = np.nan
                continue
            
            # Calculate standard deviations, ignoring NaNs
            std_dev1 = np.std(matrix_data[variant1][valid_indices])
            std_dev2 = np.std(matrix_data[variant2][valid_indices])
            
            # Check for zero standard deviation
            if std_dev1 == 0 or std_dev2 == 0:
                # Check if data is identical
                identical = np.array_equal(
                    matrix_data[variant1][valid_indices],
                    matrix_data[variant2][valid_indices]
                )
                
                if identical:
                    correlation_values[variant1][variant2] = 1.0
                else:
                    correlation_values[variant1][variant2] = np.nan
            else:
                # Normal correlation calculation
                try:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        corr = np.corrcoef(
                            matrix_data[variant1][valid_indices], 
                            matrix_data[variant2][valid_indices]
                        )[0, 1]
                    
                    correlation_values[variant1][variant2] = corr
                except Exception:
                    correlation_values[variant1][variant2] = np.nan
    
    # Create the figure
    n_locations = len(sorted_location_pairs)
    fig_size = max(12, n_locations * 2)
    fig, axes = plt.subplots(n_locations, n_locations, figsize=(fig_size, fig_size))
    
    # Flat array access for single location case
    if n_locations == 1:
        axes = np.array([[axes]])
    
    # Set title
    fig.suptitle('Cloudflare Variants Correlation Matrix - Cross-Location Analysis', fontsize=16, fontweight='bold')
    
    # Create a mapping of variants by location for easier access
    variants_by_location = {}
    for loc_pair in sorted_location_pairs:
        variants_by_location[loc_pair] = [v[0] for v in location_pairs[loc_pair]]
    
    # Fill in each subplot with the appropriate correlation matrix
    for i, loc1 in enumerate(sorted_location_pairs):
        for j, loc2 in enumerate(sorted_location_pairs):
            ax = axes[i, j]
            
            # Get variants for each location
            variants1 = variants_by_location[loc1]
            variants2 = variants_by_location[loc2]
            
            # Create correlation matrix for this location pair
            corr_matrix = np.zeros((len(variants1), len(variants2)))
            
            # Fill matrix with correlation values
            for i_var, var1 in enumerate(variants1):
                for j_var, var2 in enumerate(variants2):
                    corr_matrix[i_var, j_var] = correlation_values[var1][var2]
            
            # Create the heatmap
            masked_matrix = np.ma.masked_invalid(corr_matrix)
            im = ax.imshow(masked_matrix, cmap='coolwarm', aspect='equal', vmin=-1, vmax=1)
            
            # Set axis labels
            if i == n_locations - 1:  # Bottom row gets x labels
                date_labels = [v[1] for v in location_pairs[loc2]]
                ax.set_xticks(np.arange(len(variants2)))
                ax.set_xticklabels(date_labels, rotation=45, ha='right', fontsize=7)
            else:
                ax.set_xticks([])
            
            if j == 0:  # Left column gets y labels
                date_labels = [v[1] for v in location_pairs[loc1]]
                ax.set_yticks(np.arange(len(variants1)))
                ax.set_yticklabels(date_labels, fontsize=7)
            else:
                ax.set_yticks([])
            
            # Set title for diagonal elements only
            if i == j:
                ax.set_title(loc1, fontsize=9)
            
            # Add correlation values as text
            for i_text in range(len(variants1)):
                for j_text in range(len(variants2)):
                    value = corr_matrix[i_text, j_text]
                    if np.isnan(value):
                        text = "---"
                    elif i == j and i_text == j_text:  # Diagonal within a location
                        text = "1.00"
                    else:
                        text = f"{value:.2f}"
                    
                    # Adjust text color based on background
                    text_color = 'white' if not np.isnan(value) and value > 0.5 else 'black'
                    
                    ax.text(j_text, i_text, text, ha='center', va='center', fontsize=7, color=text_color)
    
    # Add overall column and row labels
    for i, loc in enumerate(sorted_location_pairs):
        # Create row labels on the left side
        row_label_ax = fig.add_subplot(n_locations, 1, i + 1, frameon=False)
        row_label_ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        row_label_ax.grid(False)
        row_label_ax.set_ylabel(loc, fontsize=10, rotation=90, labelpad=20)
        
        # Create column labels on the top
        col_label_ax = fig.add_subplot(1, n_locations, i + 1, frameon=False)
        col_label_ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        col_label_ax.grid(False)
        col_label_ax.set_title(loc, fontsize=10, pad=20)
    
    # Add colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Correlation Coefficient')
    
    plt.tight_layout(rect=[0.02, 0.02, 0.9, 0.95])
    
    # Save the plot
    filename = 'cloudflare_cross_location_correlation_matrix.png'
    plt.savefig(os.path.join(output_directory, filename), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Calculate average correlations between location pairs
    location_avg_correlations = {}
    for loc1 in sorted_location_pairs:
        location_avg_correlations[loc1] = {}
        vars1 = variants_by_location[loc1]
        
        for loc2 in sorted_location_pairs:
            if loc1 == loc2:
                location_avg_correlations[loc1][loc2] = 1.0
                continue
                
            vars2 = variants_by_location[loc2]
            
            # Calculate average correlation between locations
            valid_corrs = []
            for var1 in vars1:
                for var2 in vars2:
                    corr = correlation_values[var1][var2]
                    if not np.isnan(corr):
                        valid_corrs.append(corr)
            
            if valid_corrs:
                location_avg_correlations[loc1][loc2] = np.mean(valid_corrs)
            else:
                location_avg_correlations[loc1][loc2] = np.nan
    
    # Create a summary heatmap of average correlations between locations
    fig, ax = plt.subplots(figsize=(10, 8))
    avg_corr_matrix = np.zeros((n_locations, n_locations))
    
    for i, loc1 in enumerate(sorted_location_pairs):
        for j, loc2 in enumerate(sorted_location_pairs):
            avg_corr_matrix[i, j] = location_avg_correlations[loc1][loc2]
    
    masked_avg_matrix = np.ma.masked_invalid(avg_corr_matrix)
    im = ax.imshow(masked_avg_matrix, cmap='coolwarm', aspect='equal', vmin=-1, vmax=1)
    
    # Add labels
    ax.set_xticks(np.arange(n_locations))
    ax.set_yticks(np.arange(n_locations))
    ax.set_xticklabels(sorted_location_pairs, rotation=45, ha='right')
    ax.set_yticklabels(sorted_location_pairs)
    
    # Add title
    ax.set_title('Average Correlation Between Location Pairs', fontsize=14)
    
    # Add text annotations
    for i in range(n_locations):
        for j in range(n_locations):
            value = avg_corr_matrix[i, j]
            if np.isnan(value):
                text = "---"
            else:
                text = f"{value:.2f}"
            
            # Adjust text color based on background
            text_color = 'white' if not np.isnan(value) and value > 0.5 else 'black'
            
            ax.text(j, i, text, ha='center', va='center', color=text_color)
    
    plt.colorbar(im)
    plt.tight_layout()
    
    # Save the summary plot
    filename = 'cloudflare_location_avg_correlation.png'
    plt.savefig(os.path.join(output_directory, filename), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        "total_location_pairs": n_locations,
        "total_variants": len(all_variants)
    }


# Add a main function to run the analysis if this script is executed directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze Cloudflare variant test results')
    parser.add_argument('--results-dir', default='results', help='Directory containing test results')
    parser.add_argument('--output-dir', default='visualizations', help='Directory to save visualizations')
    parser.add_argument('--summaries-dir', default='summaries', help='Directory to save text summaries')
    args = parser.parse_args()
    
    # Create output directories if they don't exist
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.summaries_dir, exist_ok=True)
    
    # Load all Cloudflare variant results using the new method
    all_test_results = load_cloudflare_results(args.results_dir)
    
    if all_test_results:
        # Run the Cloudflare analysis
        compare_cloudflare_variants(all_test_results, args.summaries_dir)
        corr_stats = create_cloudflare_correlation_matrix(all_test_results, args.output_dir)
        test_stats = create_cloudflare_test_variance_chart(all_test_results, args.output_dir)
        
        # Add the new grouped correlation matrices
        grouping_stats = create_grouped_correlation_matrix(all_test_results, args.output_dir)
        cross_loc_stats = create_cross_location_correlation_matrix(all_test_results, args.output_dir)
        
        print("Cloudflare variant analysis complete.")
        print(f"Correlation stats: {corr_stats}")
        if test_stats:
            print(f"Test variance stats: {test_stats}")
        print(f"Grouping stats: {grouping_stats}")
        print(f"Cross-location stats: {cross_loc_stats}")
    else:
        print("No Cloudflare results found. Analysis skipped.") 