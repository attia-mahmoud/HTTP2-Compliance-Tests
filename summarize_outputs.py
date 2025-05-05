import json
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from collections import defaultdict, Counter
from scipy.stats import pearsonr
import seaborn as sns
import pandas as pd
import random
import glob
from datetime import datetime
import matplotlib.ticker as mticker

# Constants

def get_latest_file(directory):
    """Get the most recent file in the directory."""
    files = glob.glob(os.path.join(directory, "*.json"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def analyze_results(filename, scope):
    """Analyze a single result file and categorize results as dropped, error, or other."""
    with open(filename, 'r') as f:
        data = json.load(f)
    # drop the 0th entry
    if '0' in data:
        del data['0']
    if 'metadata' in data:
        del data['metadata']
    
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
        if not test_data or not test_data.get('result'):
            # Handle missing/empty result data as 'dropped' and count it
            test_results[test_id] = "dropped"
            test_messages[test_id] = "No result data, categorized as dropped"
            dropped_count += 1 # Increment dropped count
            continue # Continue to next test_id
        
        result = test_data['result']
        is_goaway = False
        is_reset = False
        is_500 = False
        is_dropped = False
        is_received = False
        is_modified = False
        is_unmodified = False
        message = ""
        
        if isinstance(result, str):
            # Treat string results as 'dropped'
            test_results[test_id] = "dropped"
            test_messages[test_id] = f"Result is string, categorized as dropped: {result}"
            dropped_count += 1  # Increment dropped count
            continue  # Continue to next test_id
        
        # Use safer access methods for worker data
        worker1 = result.get('Worker_1', {}) or {}
        worker2 = result.get('Worker_2', {}) or {}
        
        vars1 = worker1.get('Variables', {}) or {}
        vars2 = worker2.get('Variables', {}) or {}

        if vars2.get('result', '').startswith('Received'):
            if test_id in ['4', '87', '126', '165']:
                if scope == 'full':
                    is_modified = True
                else:
                    is_received = True
            elif test_id in ['8', '110', '151', '7', '83']:
                if scope == 'full':
                    is_unmodified = True
                else:
                    is_received = True
            else:
                if scope == 'full':
                    is_unmodified = True
                else:
                    is_received = True
            message = vars2['result']
        
        elif vars1.get('client_result', '') == 'Test result: MODIFIED' or vars1.get('result', '') == 'Test result: MODIFIED':
            if scope == 'full':
                is_modified = True
            else:
                is_received = True
            message = vars1.get('client_result', vars1.get('result', ''))
        elif vars1.get('client_result', '') == 'Test result: UNMODIFIED' or vars1.get('result', '') == 'Test result: UNMODIFIED':
            if scope == 'full':
                is_unmodified = True
            else:
                is_received = True
            message = vars1.get('client_result', vars1.get('result', ''))

        elif vars2.get('server_result', '') == 'Test result: MODIFIED':
            if scope == 'full':
                is_modified = True
            else:
                is_received = True
            message = vars2['server_result']
        elif vars2.get('server_result', '') == 'Test result: UNMODIFIED':
            if scope == 'full':
                is_unmodified = True
            else:
                is_received = True
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
                is_reset = True # TODO: check if this is correct
                message = vars1['client_result']
        elif worker2 and worker2.get('State', '') == 'RESET_RECEIVED':
            if vars2.get('msg'):
                is_reset = True
                message = vars2['msg']
            elif vars2.get('server_result'):
                is_reset = True # TODO: check if this is correct
                message = vars2['server_result']
        elif vars1 and vars1.get('client_result', '').startswith('Successfully received all') and vars1.get('server_result', '').startswith('Successfully received all'):
            if test_id in ['4', '87', '126', '165']:
                if scope == 'full':
                    is_modified = True
                else:
                    is_received = True
            elif test_id in ['8', '110', '151', '7', '83']:
                if scope == 'full':
                    is_unmodified = True
                else:
                    is_received = True
            else:
                if scope == 'full':
                    is_unmodified = True
                else:
                    is_received = True
            message = vars1['client_result']
        elif vars2 and vars2.get('client_result', '').startswith('Successfully received all')and vars2.get('server_result', '').startswith('Successfully received all'):
            if test_id in ['4', '87', '126', '165']:
                if scope == 'full':
                    is_modified = True
                else:
                    is_received = True
            elif test_id in ['8', '110', '151', '7', '83']:
                if scope == 'full':
                    is_unmodified = True
                else:
                    is_received = True
            else:
                if scope == 'full':
                    is_unmodified = True
                else:
                    is_received = True
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
            test_results[test_id] = "dropped" # Default to dropped
            dropped_count += 1
            message = f"Unknown dictionary state/result, categorized as dropped: {result}" # Provide context
            # Optional: print a warning for debugging unhandled cases
            # print(f"Warning: Unhandled dictionary structure for test {test_id}, categorized as dropped.")

        # Assign message if not already set by specific conditions
        if test_id not in test_messages:
            test_messages[test_id] = message if message else "Category assigned"
    
    return dropped_count, error_500_count, goaway_count, reset_count, received_count, modified_count, unmodified_count, test_results, test_messages

def create_markdown_table(headers, data):
    """Create a markdown table with equal column widths."""
    # Convert all data to strings and find max width for each column
    str_data = [[str(cell) for cell in row] for row in data]
    
    # Include headers in width calculation
    all_rows = [headers] + str_data
    col_widths = []
    for col_idx in range(len(headers)):
        width = max(len(row[col_idx]) for row in all_rows)
        col_widths.append(width)
    
    # Create header row with padding
    header_cells = [str(h).ljust(width) for h, width in zip(headers, col_widths)]
    table = [f"| {' | '.join(header_cells)} |"]
    
    # Create separator row with padding
    separator_cells = ['-' * width for width in col_widths]
    table.append(f"| {' | '.join(separator_cells)} |")
    
    # Create data rows with padding
    for row in str_data:
        padded_cells = [cell.ljust(width) for cell, width in zip(row, col_widths)]
        table.append(f"| {' | '.join(padded_cells)} |")
    
    return '\n'.join(table)

def create_proxy_correlation_matrix(test_results, proxy_configs, output_directory):
    """Create a Pearson correlation matrix visualization of proxy test results."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Split proxies by scope
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'full' and proxy in test_results]
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'client-only' and proxy in test_results]
    
    # Create separate correlation matrices for each scope
    for scope, proxies in [('full', full_scope_proxies), ('client-only', client_only_proxies)]:
        if not proxies:  # Skip if no proxies in this category
            continue
            
        test_ids = sorted(list(set().union(*[results.keys() for proxy, results in test_results.items() 
                                           if proxy in proxies])),
                         key=lambda x: int(x) if x.isdigit() else float('inf'))
        
        # Create matrix data with better encoding
        matrix_data = np.zeros((len(proxies), len(test_ids)))
        for i, proxy in enumerate(proxies):
            for j, test_id in enumerate(test_ids):
                # Convert result to numeric value with better separation
                result = test_results[proxy].get(test_id, "other")
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
        
        # Calculate correlation matrix with NaN handling
        correlation_matrix = np.zeros((len(proxies), len(proxies)))
        for i in range(len(proxies)):
            for j in range(len(proxies)):
                # Calculate correlation for each pair, ignoring NaNs
                valid_indices = ~(np.isnan(matrix_data[i]) | np.isnan(matrix_data[j]))
                if np.sum(valid_indices) > 1:  # Need at least 2 valid points
                    correlation_matrix[i, j] = np.corrcoef(
                        matrix_data[i, valid_indices], 
                        matrix_data[j, valid_indices]
                    )[0, 1]
                else:
                    correlation_matrix[i, j] = 0
        
        # Create figure
        plt.figure(figsize=(12, 10))
        
        # Create heatmap
        im = plt.imshow(correlation_matrix, cmap='coolwarm', aspect='equal', vmin=-1, vmax=1)
        
        # Add colorbar
        plt.colorbar(im)
        
        # Configure ticks and labels
        plt.xticks(np.arange(len(proxies)), proxies, rotation=45, ha='right')
        plt.yticks(np.arange(len(proxies)), proxies)
        
        # Add correlation values as text
        for i in range(len(proxies)):
            for j in range(len(proxies)):
                text = plt.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                              ha='center', va='center', color='black')
                
                # Make text white for dark background
                if abs(correlation_matrix[i, j]) > 0.5:
                    text.set_color('white')
        
        scope_title = 'Full Test Suite' if scope == 'full' else 'Client-side Tests Only'
        plt.title(f'Proxy Correlation Matrix ({scope_title})', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Save the plot
        filename = 'correlation_matrix_full.png' if scope == 'full' else 'correlation_matrix_client_only.png'
        plt.savefig(os.path.join(output_directory, filename), 
                    dpi=300, bbox_inches='tight')
        plt.close()

def create_proxy_result_pies(test_results, proxy_configs, output_directory):
    """Create individual pie charts showing result proportions for each proxy.
    Saves each chart to analysis/behavior/proxies/<proxy_name>_result_pie.png.
    """
    proxies_output_dir = os.path.join(output_directory, 'proxies')
    os.makedirs(proxies_output_dir, exist_ok=True)
    
    colors = ['#ff6b6b', '#ffd93d', '#ff9f43', '#6c5ce7', '#6bceff', '#4ecdc4', '#2ecc71', '#95a5a6']
    
    for proxy, config in proxy_configs.items():
        if proxy not in test_results:
            print(f"Skipping pie chart for {proxy}: No results found.")
            continue
            
        fig, ax = plt.subplots(figsize=(8, 8)) # Create a new figure for each proxy
        
        proxy_title = f"{proxy} Result Distribution"
        create_single_pie(ax, test_results[proxy], colors, proxy_title)
        
        # Save the individual pie chart
        filename = f"{proxy}_result_pie.png"
        output_path = os.path.join(proxies_output_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig) # Close the figure to free memory

def create_proxy_line_graphs(test_results, proxy_configs, output_directory):
    """Create line graphs showing test result categories with different proxies as lines in CDF style."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Split proxies by scope
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'full' and proxy in test_results]
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'client-only' and proxy in test_results]
    
    # Define the categories in the order we want them on the x-axis
    categories = ['dropped', '500', 'goaway', 'reset', 'unmodified', 'modified']
    category_display_names = ['D', 'E', 'G', 'R', 'U', 'M']
    
    # Load test_cases.json to determine optimum behavior
    with open('test_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Create a mapping from test ID to whether it should use stream reset or goaway
    test_error_types = {}
    for test in test_cases:
        test_id = str(test['id'])
        if test.get('error_type') == 'stream':
            test_error_types[test_id] = 'reset'
        elif test.get('expected_result') == 'error':
            test_error_types[test_id] = 'goaway'
        elif test.get('expected_result') == 'ignore':
            test_error_types[test_id] = 'ignore'
    
    # Create separate graphs for full scope and client-only proxies
    for scope, proxies in [('full', full_scope_proxies), ('client-only', client_only_proxies)]:
        if not proxies:  # Skip if no proxies in this category
            continue
        
        plt.figure(figsize=(12, 8))
        
        # Define a colormap for the lines
        colors = plt.cm.viridis(np.linspace(0, 1, len(proxies)))
        
        # Calculate percentages for each proxy and category
        for i, proxy in enumerate(proxies):
            proxy_results = test_results[proxy]
            total_tests = len(proxy_results)
            
            if total_tests == 0:
                continue
                
            # Count occurrences of each category
            category_counts = {cat: 0 for cat in categories}
            
            for result in proxy_results.values():
                if result in category_counts:
                    category_counts[result] += 1
                    
            # Calculate raw percentages
            percentages = [category_counts[cat] / total_tests * 100 for cat in categories]
            
            # Calculate cumulative percentages for CDF
            cum_percentages = []
            cum_sum = 0
            for pct in percentages:
                cum_sum += pct
                cum_percentages.append(cum_sum)
            
            # Plot the line for this proxy
            plt.plot(range(len(categories)), cum_percentages, marker='o', linewidth=2, 
                     color=colors[i], label=f"{proxy}")
        
        # Add the optimum/baseline behavior
        # For full scope, use all test cases; for client-only, use only client-side tests
        if scope == 'full':
            relevant_test_cases = test_error_types
        else:
            # For client-only proxies, we'll skip the baseline since they don't handle server-side tests
            relevant_test_cases = {}
        
        if relevant_test_cases:
            # Initialize category counts for baseline
            baseline_counts = {cat: 0 for cat in categories}
            total_baseline_tests = len(relevant_test_cases)
            
            # Count ideal responses based on error_type
            for test_id, error_type in relevant_test_cases.items():
                if error_type == 'reset':
                    baseline_counts['reset'] += 1
                elif error_type == 'goaway':
                    baseline_counts['goaway'] += 1
                elif error_type == 'ignore':
                    baseline_counts['dropped'] += 1
            
            # Calculate percentages
            baseline_percentages = [baseline_counts[cat] / total_baseline_tests * 100 for cat in categories]
            
            # Calculate cumulative percentages
            baseline_cum_percentages = []
            cum_sum = 0
            for pct in baseline_percentages:
                cum_sum += pct
                baseline_cum_percentages.append(cum_sum)
            
            # Plot the baseline with a distinct style
            plt.plot(range(len(categories)), baseline_cum_percentages, 'k--', linewidth=2.5, 
                     marker='*', markersize=10, label="RFC Ideal")
        
        # Configure the plot
        plt.xticks(range(len(categories)), category_display_names, rotation=45)
        plt.xlim(-0.5, len(categories) - 0.5)
        plt.ylim(0, 110)  # Increased from 100 to 110 to provide more padding at the top
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Add test count annotation next to the 100% mark on the y-axis
        test_count = 166 if scope == 'full' else 83  # Hardcoded values as specified
        
        scope_title = 'HTTP/2 End-to-End' if scope == 'full' else 'HTTP/2 to HTTP/1.1'
        plt.title(f'HTTP/2 Test Result Distribution - {scope_title} ({test_count} tests)', fontsize=14, fontweight='bold')
        plt.ylabel('Cumulative Percentage (%)', fontsize=12)
        
        # Add legend with smaller font size
        plt.legend(loc='lower right', fontsize=10)
        
        plt.tight_layout()
        
        # Save the figure
        filename = 'result_cdf_full.png' if scope == 'full' else 'result_cdf_client_only.png'
        plt.savefig(os.path.join(output_directory, filename), dpi=300, bbox_inches='tight')
        plt.close()

def create_single_pie(ax, test_results, colors, title):
    """Create a single pie chart on the given axis."""
    if not test_results:
        ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=14)
        ax.axis('off')
        ax.set_title(title, pad=20)
        return
    
    # Count categories
    total_tests = len(test_results)
    dropped = sum(1 for result in test_results.values() if result == "dropped")
    error_500 = sum(1 for result in test_results.values() if result == "500")
    goaway = sum(1 for result in test_results.values() if result == "goaway")
    reset = sum(1 for result in test_results.values() if result == "reset")
    received = sum(1 for result in test_results.values() if result == "received")
    modified = sum(1 for result in test_results.values() if result == "modified")
    unmodified = sum(1 for result in test_results.values() if result == "unmodified")
    other = total_tests - dropped - error_500 - goaway - reset - received - modified - unmodified
    
    # Calculate percentages
    dropped_pct = (dropped / total_tests) * 100 if total_tests > 0 else 0
    error_500_pct = (error_500 / total_tests) * 100 if total_tests > 0 else 0
    goaway_pct = (goaway / total_tests) * 100 if total_tests > 0 else 0
    reset_pct = (reset / total_tests) * 100 if total_tests > 0 else 0
    received_pct = (received / total_tests) * 100 if total_tests > 0 else 0
    modified_pct = (modified / total_tests) * 100 if total_tests > 0 else 0
    unmodified_pct = (unmodified / total_tests) * 100 if total_tests > 0 else 0
    other_pct = (other / total_tests) * 100 if total_tests > 0 else 0
    
    # Only include non-zero values
    sizes = []
    labels = []
    colors_filtered = []
    
    if dropped > 0:
        sizes.append(dropped_pct)
        labels.append(f'Dropped\n{dropped} ({dropped_pct:.1f}%)')
        colors_filtered.append(colors[0])
    
    if error_500 > 0:
        sizes.append(error_500_pct)
        labels.append(f'500 Error\n{error_500} ({error_500_pct:.1f}%)')
        colors_filtered.append(colors[1])
    
    if goaway > 0:
        sizes.append(goaway_pct)
        labels.append(f'GOAWAY\n{goaway} ({goaway_pct:.1f}%)')
        colors_filtered.append(colors[2])
    
    if reset > 0:
        sizes.append(reset_pct)
        labels.append(f'RESET\n{reset} ({reset_pct:.1f}%)')
        colors_filtered.append(colors[3])
    
    if received > 0:
        sizes.append(received_pct)
        labels.append(f'Received\n{received} ({received_pct:.1f}%)')
        colors_filtered.append(colors[4])
        
    if modified > 0:
        sizes.append(modified_pct)
        labels.append(f'Modified\n{modified} ({modified_pct:.1f}%)')
        colors_filtered.append(colors[5])
        
    if unmodified > 0:
        sizes.append(unmodified_pct)
        labels.append(f'Unmodified\n{unmodified} ({unmodified_pct:.1f}%)')
        colors_filtered.append(colors[6])
    
    if other > 0:
        sizes.append(other_pct)
        labels.append(f'Other\n{other} ({other_pct:.1f}%)')
        colors_filtered.append(colors[7])
    
    if sizes:  # Only create pie if we have non-zero values
        ax.pie(sizes, labels=labels, colors=colors_filtered, autopct='', 
               startangle=90)
    else:
        ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=14)
        ax.axis('off')
    
    ax.set_title(title, pad=20)

def create_result_counts_table(dropped_counts, error_500_counts, goaway_counts, reset_counts, received_counts, all_test_results, proxy_configs, output_directory):
    """Create a markdown table summarizing the counts of dropped, error, reset, goaway, and received results."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Create table header
    table = "| Proxy | Test Scope | Dropped Count | 500 Error Count | GOAWAY Count | RESET Count | Received Count | Modified Count | Unmodified Count | Received Tests | Modified Tests | Unmodified Tests |\n"
    table += "| ----- | ---------- | ------------- | --------------- | ------------ | ----------- | -------------- | -------------- | ---------------- | -------------- | -------------- | ---------------- |\n"
    
    # Add rows for each proxy
    for proxy in sorted(dropped_counts.keys()):
        # Get the list of test IDs for each result type
        received_tests = []
        modified_tests = []
        unmodified_tests = []
        modified_count = 0
        unmodified_count = 0
        
        if proxy in all_test_results:
            for test_id, result in all_test_results[proxy].items():
                if result == "received":
                    received_tests.append(test_id)
                elif result == "modified":
                    modified_tests.append(test_id)
                    modified_count += 1
                elif result == "unmodified":
                    unmodified_tests.append(test_id)
                    unmodified_count += 1
        
        # Format the test ID lists
        received_tests_str = ", ".join(sorted(received_tests, key=lambda x: int(x) if x.isdigit() else float('inf')))
        modified_tests_str = ", ".join(sorted(modified_tests, key=lambda x: int(x) if x.isdigit() else float('inf')))
        unmodified_tests_str = ", ".join(sorted(unmodified_tests, key=lambda x: int(x) if x.isdigit() else float('inf')))
        
        # Get test scope
        scope = proxy_configs[proxy]['scope']
        scope_display = "Full" if scope == "full" else "Client-side Only"
        
        # Add the row with all information
        table += f"| {proxy} | {scope_display} | {dropped_counts.get(proxy, 0)} | {error_500_counts.get(proxy, 0)} | {goaway_counts.get(proxy, 0)} | {reset_counts.get(proxy, 0)} | {received_counts.get(proxy, 0)} | {modified_count} | {unmodified_count} | {received_tests_str} | {modified_tests_str} | {unmodified_tests_str} |\n"
    
    # Write to file
    with open(os.path.join(output_directory, "result_counts.md"), "w") as f:
        f.write(table)

def create_test_results_matrix(all_test_results, proxy_configs, output_directory):
    """Create a matrix showing test results for each proxy and test ID."""
    all_test_ids = sorted(set().union(*[test_results.keys() for test_results in all_test_results.values()]),
                         key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    proxies = list(proxy_configs.keys())  # Convert dict_keys to list
    matrix_headers = ['Test ID'] + proxies
    matrix_data = []
    outlier_counts = {proxy: 0 for proxy in proxies}  # Track outliers for each proxy
    
    for test_id in all_test_ids:
        row = [test_id]
        # First collect all results for this test
        test_row = []
        for proxy in proxies:  # Use the list of proxies
            if proxy in all_test_results:
                result = all_test_results[proxy].get(test_id, "")
                if result == "received":
                    test_row.append("✓R")
                elif result == "dropped":
                    test_row.append("✓D")
                elif result == "500":
                    test_row.append("✓5")
                elif result == "goaway":
                    test_row.append("✓G")
                elif result == "reset":
                    test_row.append("✓X")
                elif result == "modified":
                    test_row.append("✓M")
                elif result == "unmodified":
                    test_row.append("✓U")
                elif result == "other":
                    test_row.append("✓O")
                else:
                    test_row.append("")
            else:
                test_row.append("")
        
        # Check if there's an outlier
        results = [r for r in test_row if r]
        if len(set(results)) > 1 and len(results) > 0:
            # Count occurrences of each result
            result_counts = {}
            for i, res in enumerate(test_row):
                if res:
                    result_counts[res] = result_counts.get(res, 0) + 1
            
            # Find the least common result
            min_count = min(result_counts.values()) if result_counts else 0
            if min_count == 1:  # If there's a unique outlier
                outlier_results = [r for r, count in result_counts.items() if count == min_count]
                for outlier in outlier_results:
                    idx = test_row.index(outlier)
                    test_row[idx] = f'**{outlier}**'
                    outlier_counts[proxies[idx]] += 1  # Use the list index
        
        row.extend(test_row)
        matrix_data.append(row)
    
    # Add empty row for spacing
    matrix_data.append([''] * (len(proxies) + 1))
    
    # Add outlier count row
    outlier_row = ['Outlier Count']
    outlier_row.extend(str(outlier_counts[proxy]) for proxy in proxies)
    matrix_data.append(outlier_row)
    
    matrix_table = create_markdown_table(matrix_headers, matrix_data)
    
    with open(os.path.join(output_directory, 'test_results_matrix.md'), 'w') as f:
        f.write(matrix_table)

def extract_and_save_outliers(all_test_results, proxy_configs, output_directory):
    """
    Extract outliers from test results and save them to dedicated files based on test scope.
    
    Outliers are defined as tests where exactly one proxy behaves differently from all others
    that have the same scope (full or client-only).
    
    Args:
        all_test_results: Dictionary mapping proxy names to their test results
        proxy_configs: Dictionary mapping proxy names to their configurations
        output_directory: Directory to save the output report
    """
    # Load test descriptions
    try:
        with open('test_cases.json', 'r') as f:
            test_cases = json.load(f)
        test_descriptions = {str(case['id']): case['description'] for case in test_cases}
    except Exception as e:
        print(f"Warning: Could not load test descriptions from test_cases.json: {e}")
        test_descriptions = {}
    
    # Get list of proxies by scope
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() 
                         if config['scope'] == 'full' and proxy in all_test_results]
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() 
                         if config['scope'] == 'client-only' and proxy in all_test_results]
    
    # Get all test IDs
    all_test_ids = sorted(set().union(*[results.keys() for results in all_test_results.values()]),
                         key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    # Dictionary to collect outliers by scope
    # {test_id: {outlier_proxy, outlier_behavior, common_behavior}}
    full_scope_outliers = {}
    client_only_outliers = {}
    
    # Function to process tests for a given scope
    def process_scope(test_id, scope_proxies, outliers_dict):
        # Skip if we don't have at least 3 proxies to compare
        if len(scope_proxies) < 3:
            return
        
        # Collect results for this test from proxies in this scope
        test_results = {}
        for proxy in scope_proxies:
            if test_id in all_test_results[proxy]:
                test_results[proxy] = all_test_results[proxy][test_id]
        
        # Skip if not enough proxies have results for this test
        if len(test_results) < 3:
            return
        
        # Following the vector graph logic:
        # Count occurrences of each result value
        result_counts = {}
        for result in test_results.values():
            result_counts[result] = result_counts.get(result, 0) + 1
        
        # Check if there's exactly one outlier (one result value with count=1)
        if 1 in result_counts.values() and len(result_counts) > 1:
            # Find the outlier result(s)
            outlier_results = [r for r, count in result_counts.items() if count == 1]
            
            for outlier_result in outlier_results:
                # Find which proxy had the outlier result
                outlier_proxy = None
                for proxy, result in test_results.items():
                    if result == outlier_result:
                        outlier_proxy = proxy
                        break
                
                # Find the most common result (this is the "normal" behavior)
                common_result = max(result_counts.items(), key=lambda x: x[1])[0]
                
                # Store the outlier information
                outliers_dict[test_id] = {
                    'outlier_proxy': outlier_proxy,
                    'outlier_behavior': outlier_result,
                    'common_behavior': common_result
                }
    
    # Process each test for both scopes
    for test_id in all_test_ids:
        process_scope(test_id, full_scope_proxies, full_scope_outliers)
        process_scope(test_id, client_only_proxies, client_only_outliers)
    
    # Helper function to write outliers to a file
    def write_outliers_file(outliers, filename, scope_name):
        output_file = os.path.join(output_directory, filename)
        
        with open(output_file, 'w') as f:
            f.write(f"# Outlier Behaviors in HTTP/2 Conformance Tests - {scope_name} Scope\n\n")
            f.write("This document lists tests where exactly one proxy behaved differently than all others.\n\n")
            f.write(f"Total outliers found: {len(outliers)}\n\n")
            
            # Sort outliers by proxy to group them
            proxy_outliers = {}
            for test_id, data in outliers.items():
                proxy = data['outlier_proxy']
                if proxy not in proxy_outliers:
                    proxy_outliers[proxy] = []
                proxy_outliers[proxy].append((test_id, data))
            
            # Write grouped by proxy
            for proxy in sorted(proxy_outliers.keys()):
                f.write(f"## Outliers for {proxy}\n\n")
                
                # Create table header
                f.write("| Test ID | Description | Outlier Behavior | Common Behavior |\n")
                f.write("|---------|-------------|------------------|----------------|\n")
                
                # Add each outlier for this proxy
                for test_id, data in sorted(proxy_outliers[proxy], key=lambda x: int(x[0]) if x[0].isdigit() else float('inf')):
                    description = test_descriptions.get(test_id, "No description available")
                    outlier_behavior = data['outlier_behavior']
                    common_behavior = data['common_behavior']
                    
                    f.write(f"| {test_id} | {description} | {outlier_behavior} | {common_behavior} |\n")
                
                f.write("\n")
            
    # Write both files
    write_outliers_file(full_scope_outliers, "outliers_full.md", "Full")
    write_outliers_file(client_only_outliers, "outliers_client_only.md", "Client-Only")
    
    return full_scope_outliers, client_only_outliers

def load_client_server_classification(json_path):
    """Load the classification of tests as client-side or server-side."""
    with open(json_path, 'r') as f:
        classification = json.load(f)
    
    # Convert frame numbers to strings to match test IDs
    client_side_tests = set(str(frame) for frame in classification['client_side_non_conformant_frames'])
    server_side_tests = set(str(frame) for frame in classification['server_side_non_conformant_frames'])
    
    return client_side_tests, server_side_tests

def create_client_server_conformance_visualization(test_results, client_side_tests, server_side_tests, proxy_configs, output_directory, scope_filter='all'):
    """
    Create visualizations showing how well each proxy conforms to client-side and server-side tests separately.
    Optionally filters proxies based on scope.
    
    Args:
        test_results: Dictionary mapping proxy names to their test results.
        client_side_tests: Set of test IDs classified as client-side.
        server_side_tests: Set of test IDs classified as server-side.
        proxy_configs: Dictionary mapping proxy names to their configurations.
        output_directory: Directory to save the output plots.
        scope_filter: 'all', 'full', or 'client-only'. Filters proxies based on scope.
    """
    os.makedirs(output_directory, exist_ok=True)
    
    # Filter proxies based on scope_filter
    filtered_proxies = {}
    if scope_filter == 'all':
        filtered_proxies = list(test_results.keys())
    elif scope_filter == 'full':
        filtered_proxies = [p for p, cfg in proxy_configs.items() if cfg['scope'] == 'full' and p in test_results]
    elif scope_filter == 'client-only':
        filtered_proxies = [p for p, cfg in proxy_configs.items() if cfg['scope'] == 'client-only' and p in test_results]
    else:
        print(f"Invalid scope_filter: {scope_filter}. Defaulting to 'all'.")
        filtered_proxies = list(test_results.keys())
        
    if not filtered_proxies:
        print(f"No proxies found for scope filter '{scope_filter}'. Skipping visualization.")
        return

    # First, load the test cases to get expected results
    with open('test_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Create a mapping of test ID to expected result
    expected_results = {str(case['id']): case['expected_result'] for case in test_cases}
    
    # Initialize data structures for tracking conformance
    client_conformance_data = {proxy: {'conformant': 0, 'non_conformant': 0, 'total': 0} 
                             for proxy in test_results.keys()}
    server_conformance_data = {proxy: {'conformant': 0, 'non_conformant': 0, 'total': 0} 
                             for proxy in test_results.keys()}
    
    # Analyze each proxy's results
    for proxy, results in test_results.items():
        if proxy not in filtered_proxies: # Skip proxies not in the filtered list
            continue
        for test_id, result in results.items():
            if test_id not in expected_results:
                continue
                
            expected = expected_results[test_id]
            
            # Determine if test is client-side or server-side
            if test_id in client_side_tests:
                client_conformance_data[proxy]['total'] += 1
                if expected == "error":
                    if result in ["goaway", "reset", "500"]:
                        client_conformance_data[proxy]['conformant'] += 1
                    else:  # dropped, received, modified, unmodified, or other
                        client_conformance_data[proxy]['non_conformant'] += 1
                elif expected == "ignore":
                    if result == "dropped":
                        client_conformance_data[proxy]['conformant'] += 1
                    else:  # goaway, reset, 500, received, modified, unmodified, or other
                        client_conformance_data[proxy]['non_conformant'] += 1
            elif test_id in server_side_tests:
                server_conformance_data[proxy]['total'] += 1
                if expected == "error":
                    if result in ["goaway", "reset", "500"]:
                        server_conformance_data[proxy]['conformant'] += 1
                    else:  # dropped, received, modified, unmodified, or other
                        server_conformance_data[proxy]['non_conformant'] += 1
                elif expected == "ignore":
                    if result == "dropped":
                        server_conformance_data[proxy]['conformant'] += 1
                    else:  # goaway, reset, 500, received, modified, unmodified, or other
                        server_conformance_data[proxy]['non_conformant'] += 1
    
    # Create the visualization
    plt.figure(figsize=(15, 8))
    
    # Prepare data
    proxies = filtered_proxies # Use filtered list
    x = np.arange(len(proxies))
    width = 0.35  # Width of the bars
    
    # Calculate non-conformance percentages (1 - conformance)
    client_non_conformant = []
    server_non_conformant = []
    
    for proxy in proxies:
        # Client data
        client_total = client_conformance_data[proxy]['total']
        if client_total > 0:
            client_non_conformant.append(
                (client_total - client_conformance_data[proxy]['conformant']) / client_total * 100)
        else:
            client_non_conformant.append(0)
        
        # Server data
        server_total = server_conformance_data[proxy]['total']
        if server_total > 0:
            server_non_conformant.append(
                (server_total - server_conformance_data[proxy]['conformant']) / server_total * 100)
        else:
            server_non_conformant.append(0)
    
    # Create bars
    plt.bar(x - width/2, client_non_conformant, width, label='Client Non-Compliant', color='#2ecc71', hatch='///')
    plt.bar(x + width/2, server_non_conformant, width, label='Server Non-Compliant', color='#3498db')
    
    # Customize the plot
    plt.xlabel('Proxy', fontsize=18)
    plt.ylabel('Percentage of Non-Compliant Tests', fontsize=18)
    
    # Adjust title based on scope filter
    if scope_filter == 'full':
        title_suffix = ' (Full Scope Proxies)'
        filename_suffix = '_full'
    elif scope_filter == 'client-only':
        title_suffix = ' (Client-Only Scope Proxies)'
        filename_suffix = '_client_only'
    else:
        title_suffix = ' (All Proxies)'
        filename_suffix = '_all'
        
    plt.xticks(x, proxies, rotation=45, ha='right', fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(fontsize=18)
    
    # Add percentage labels on the bars
    def add_labels(x_pos, heights):
        for i, height in enumerate(heights):
            if height > 0:  # Only add label if there's a non-zero value
                plt.text(x_pos[i], height + 1,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontsize=10) # Added fontsize for bar labels
    
    # Add labels for client and server bars
    add_labels(x - width/2, client_non_conformant)
    add_labels(x + width/2, server_non_conformant)
    
    plt.ylim(0, 100)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    
    # Save the plot with scope-specific filename
    plt.savefig(os.path.join(output_directory, f'client_server_non_conformance{filename_suffix}.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def load_test_pairs(pairs_file='docs/pairs.json'):
    """Load the test pairs from the JSON file."""
    with open(pairs_file, 'r') as f:
        data = json.load(f)
    return data['pairs']

def create_test_outcome_by_id_table(all_test_results, output_directory):
    """Create a text file listing proxies that had modified, unmodified, or received results for each test ID."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Load test case descriptions
    with open('test_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Create a mapping of test ID to description
    test_descriptions = {str(case['id']): case['description'] for case in test_cases}
    
    # Create a dict to organize test outcomes by test ID
    test_outcomes = {}
    
    # Process each proxy's results
    for proxy, results in all_test_results.items():
        if proxy in ["Mitmproxy"]:
            continue
        for test_id, result in results.items():
            if test_id not in test_outcomes:
                test_outcomes[test_id] = {
                    "received": [],
                    "modified": [],
                    "unmodified": []
                }
            
            if result == "received":
                test_outcomes[test_id]["received"].append(proxy)
            elif result == "modified":
                test_outcomes[test_id]["modified"].append(proxy)
            elif result == "unmodified":
                test_outcomes[test_id]["unmodified"].append(proxy)
    
    # Create the output file
    output_file = os.path.join(output_directory, "test_outcomes_by_id.md")
    
    with open(output_file, 'w') as f:
        f.write("Test Outcomes by Test ID\n\n")
        
        # Sort test IDs numerically
        sorted_test_ids = sorted(test_outcomes.keys(), key=lambda x: int(x) if x.isdigit() else float('inf'))
        
        for test_id in sorted_test_ids:
            description = test_descriptions.get(test_id, "No description available")
            outcomes = test_outcomes[test_id]
            
            # Only include tests that have at least one positive outcome (received, modified, or unmodified)
            if any(outcomes.values()):
                f.write(f"{test_id} {description}\n")
                
                # List proxies for each outcome type
                if outcomes["received"]:
                    f.write(f"Received: {', '.join(sorted(outcomes['received']))}\n")
                
                if outcomes["modified"]:
                    f.write(f"Received modified: {', '.join(sorted(outcomes['modified']))}\n")
                
                if outcomes["unmodified"]:
                    f.write(f"Received unmodified: {', '.join(sorted(outcomes['unmodified']))}\n")
                
                # Add a separator between tests
                f.write("\n")

def create_modified_unmodified_summary(all_test_results, output_directory):
    """Create a text file listing proxies that had modified or unmodified results for each test ID."""
    os.makedirs(output_directory, exist_ok=True)

    # Load test case descriptions
    try:
        with open('test_cases.json', 'r') as f:
            test_cases = json.load(f)
        test_descriptions = {str(case['id']): case['description'] for case in test_cases}
    except Exception as e:
        print(f"Warning: Could not load test descriptions from test_cases.json: {e}")
        test_descriptions = {}

    # Create a dict to organize test outcomes by test ID
    test_outcomes = defaultdict(lambda: {"modified": [], "unmodified": []})

    # Process each proxy's results
    for proxy, results in all_test_results.items():
        for test_id, result in results.items():
            if result == "modified":
                test_outcomes[test_id]["modified"].append(proxy)
            elif result == "unmodified":
                test_outcomes[test_id]["unmodified"].append(proxy)

    # Create the output file
    output_file = os.path.join(output_directory, "modified_unmodified_summary.md")

    with open(output_file, 'w') as f:
        f.write("# Modified and Unmodified Test Results Summary\n\n")
        f.write("This file lists test cases where at least one proxy returned a 'modified' or 'unmodified' result.\n\n")

        # Sort test IDs numerically
        sorted_test_ids = sorted(test_outcomes.keys(), key=lambda x: int(x) if x.isdigit() else float('inf'))

        for test_id in sorted_test_ids:
            description = test_descriptions.get(test_id, "No description available")
            outcomes = test_outcomes[test_id]

            # Only include tests that have at least one modified or unmodified result
            if outcomes["modified"] or outcomes["unmodified"]:
                f.write(f"## Test {test_id}: {description}\n\n")

                if outcomes["modified"]:
                    f.write(f"**Modified by:** {', '.join(sorted(outcomes['modified']))}\n")

                if outcomes["unmodified"]:
                    f.write(f"**Unmodified by:** {', '.join(sorted(outcomes['unmodified']))}\n")

                # Add a separator between tests
                f.write("\n---\n\n")

def create_client_server_proxy_line_graphs(test_results, proxy_configs, client_side_tests, server_side_tests, output_directory):
    """Create line graphs showing test result categories with different proxies as lines in CDF style,
    separated by client-side and server-side tests."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Filter for full-scope proxies only
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() 
                         if config['scope'] == 'full' and proxy in test_results]
    
    if not full_scope_proxies:
        print("No full-scope proxies found for client-server line graphs")
        return
    
    # Define the categories in the order we want them on the x-axis
    categories = ['dropped', '500', 'goaway', 'reset', 'unmodified', 'modified']
    category_display_names = ['D', 'E', 'G', 'R', 'U', 'M']
    
    # Load test_cases.json to determine optimum behavior
    with open('test_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Create a mapping from test ID to whether it should use stream reset or goaway
    test_error_types = {}
    for test in test_cases:
        test_id = str(test['id'])
        if test.get('error_type') == 'stream':
            test_error_types[test_id] = 'reset'
        elif test.get('expected_result') == 'error':
            test_error_types[test_id] = 'goaway'
        elif test.get('expected_result') == 'ignore':
            test_error_types[test_id] = 'ignore'
    
    # Process separately for client-side and server-side tests
    for test_type, test_set in [('client_side', client_side_tests), ('server_side', server_side_tests)]:
        plt.figure(figsize=(12, 8))
        
        # Define a colormap for the lines
        colors = plt.cm.viridis(np.linspace(0, 1, len(full_scope_proxies)))
        
        # Calculate percentages for each proxy and category
        for i, proxy in enumerate(full_scope_proxies):
            proxy_results = {test_id: result for test_id, result in test_results[proxy].items() 
                            if test_id in test_set}
            
            total_tests = len(proxy_results)
            
            if total_tests == 0:
                continue
                
            # Count occurrences of each category
            category_counts = {cat: 0 for cat in categories}
            
            for result in proxy_results.values():
                if result in category_counts:
                    category_counts[result] += 1
                    
            # Calculate raw percentages
            percentages = [category_counts[cat] / total_tests * 100 for cat in categories]
            
            # Calculate cumulative percentages for CDF
            cum_percentages = []
            cum_sum = 0
            for pct in percentages:
                cum_sum += pct
                cum_percentages.append(cum_sum)
            
            # Plot the line for this proxy
            plt.plot(range(len(categories)), cum_percentages, marker='o', linewidth=2, 
                     color=colors[i], label=f"{proxy}")
        
        # Add the optimum/baseline behavior
        # For full scope, use all test cases; for client-only, use only client-side tests
        if test_type == 'full':
            relevant_test_cases = test_error_types
        else:
            # For client-only proxies, we'll skip the baseline since they don't handle server-side tests
            relevant_test_cases = {}
        
        if relevant_test_cases:
            # Initialize category counts for baseline
            baseline_counts = {cat: 0 for cat in categories}
            total_baseline_tests = len(relevant_test_cases)
            
            # Count ideal responses based on error_type
            for test_id, error_type in relevant_test_cases.items():
                if error_type == 'reset':
                    baseline_counts['reset'] += 1
                elif error_type == 'goaway':
                    baseline_counts['goaway'] += 1
                elif error_type == 'ignore':
                    baseline_counts['dropped'] += 1
            
            # Calculate percentages
            baseline_percentages = [baseline_counts[cat] / total_baseline_tests * 100 for cat in categories]
            
            # Calculate cumulative percentages
            baseline_cum_percentages = []
            cum_sum = 0
            for pct in baseline_percentages:
                cum_sum += pct
                baseline_cum_percentages.append(cum_sum)
            
            # Plot the baseline with a distinct style
            plt.plot(range(len(categories)), baseline_cum_percentages, 'k--', linewidth=2.5, 
                     marker='*', markersize=10, label="RFC Ideal")
        
        # Configure the plot
        plt.xticks(range(len(categories)), category_display_names, rotation=45)
        plt.xlim(-0.5, len(categories) - 0.5)
        plt.ylim(0, 110)  # Increased from 100 to 110 to provide more padding at the top
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Get test count for this test type
        test_count = len(test_set)
        test_type_display = "Client-side" if test_type == "client_side" else "Server-side"
        
        plt.title(f'HTTP/2 Test Result Distribution - {test_type_display} Only ({test_count} tests)', 
                  fontsize=14, fontweight='bold')
        plt.ylabel('Cumulative Percentage (%)', fontsize=12)
        
        # Add legend with smaller font size
        plt.legend(loc='lower right', fontsize=10)
        
        plt.tight_layout()
        
        # Save the figure
        filename = f'client_server_cdf_{test_type}.png'
        plt.savefig(os.path.join(output_directory, filename), dpi=300, bbox_inches='tight')
        plt.close()

def create_client_server_discrepancy_visualization(test_results, test_pairs, output_directory):
    """Create visualizations showing discrepancies between client and server test pairs."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Create a DataFrame to store discrepancies
    discrepancy_data = []
    
    # Define all possible result types for consistent ordering
    result_types = ["dropped", "500", "goaway", "reset", "received", "other"]
    
    # Create transition matrices for each proxy
    transition_matrices = {}
    
    for proxy_name in test_results.keys():
        # Initialize transition matrix with zeros
        transition_matrix = pd.DataFrame(0, 
                                        index=result_types, 
                                        columns=result_types)
        transition_matrices[proxy_name] = transition_matrix
    
    for client_test, server_test in test_pairs:
        client_test_str = str(client_test)
        server_test_str = str(server_test)
        
        for proxy_name, results in test_results.items():
            # Get results for this pair (if available)
            client_result = results.get(client_test_str, "unknown")
            server_result = results.get(server_test_str, "unknown")
            
            # Skip if either result is unknown
            if client_result == "unknown" or server_result == "unknown":
                continue
            
            # If client_result is not in our predefined types, map it to "other"
            if client_result not in result_types:
                client_result = "other"
                
            # If server_result is not in our predefined types, map it to "other"
            if server_result not in result_types:
                server_result = "other"
                
            # Increment the count in the transition matrix
            transition_matrices[proxy_name].loc[client_result, server_result] += 1
                
            # Check if there's a discrepancy
            has_discrepancy = client_result != server_result
            
            discrepancy_data.append({
                'Proxy': proxy_name,
                'Test Pair': f"C{client_test}/S{server_test}",
                'Client Result': client_result,
                'Server Result': server_result,
                'Has Discrepancy': has_discrepancy,
                'Discrepancy Type': f"{client_result}→{server_result}" if has_discrepancy else "None"
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(discrepancy_data)
    
    if df.empty:
        print("No valid test pair data found for discrepancy visualization")
        return
    
    # Calculate summary statistics
    summary = df.groupby('Proxy')['Has Discrepancy'].mean().reset_index()
    summary.columns = ['Proxy', 'Discrepancy Rate']
    summary = summary.sort_values('Discrepancy Rate', ascending=False)

    # Create the bar chart visualization
    fig, ax = plt.subplots(figsize=(10, 6))

    # Summary bar chart
    # Store the bars for potential future use
    bars = ax.barh(summary['Proxy'], summary['Discrepancy Rate'], color='skyblue')

    # Add percentage labels to the bars (using the raw rate value)
    for i, v in enumerate(summary['Discrepancy Rate']):
        # Place label slightly after the bar end
        ax.text(v + 0.01, i, f"{v:.1%}", va='center')

    # plt.title('Client/Server Test Pair Discrepancy Rates by Proxy', fontsize=14, fontweight='bold')
    ax.set_xlabel('Percentage of Test Pairs with Varying Behavior', fontsize=12)
    ax.set_ylabel('Proxy', fontsize=12)

    # Set x-axis limits (slightly wider to accommodate labels)
    max_rate = summary['Discrepancy Rate'].max()
    ax.set_xlim(0, max_rate * 1.15 if max_rate > 0 else 0.1) # Adjusted limit calculation

    # Format x-axis ticks as percentages
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))

    plt.tight_layout()

    # Save the figure
    plt.savefig(os.path.join(output_directory, 'client_server_discrepancies.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_test_timeline_graphs(test_results, proxy_configs, client_side_tests, server_side_tests, output_directory):
    """Create line graphs showing test results per test ID for each proxy,
       optionally filtering tests for client-only scope."""
    os.makedirs(output_directory, exist_ok=True)

    # Define categories and their numerical mapping for the Y-axis (excluding 'other')
    categories = ['dropped', '500', 'goaway', 'reset', 'unmodified', 'modified']
    category_map = {cat: i for i, cat in enumerate(categories)}
    
    # Get all unique test IDs sorted numerically (used for full scope)
    all_test_ids_full = sorted(
        list(set().union(*(results.keys() for results in test_results.values()))),
        key=lambda x: int(x) if x.isdigit() else float('inf')
    )

    # Filter test IDs for client-side only tests
    all_test_ids_client_only = sorted(
        [tid for tid in all_test_ids_full if tid in client_side_tests],
        key=lambda x: int(x) if x.isdigit() else float('inf')
    )

    # Split proxies by scope
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'full' and proxy in test_results]
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'client-only' and proxy in test_results]

    # Create graphs for each scope
    for scope, proxies in [('full', full_scope_proxies), ('client-only', client_only_proxies)]:
        if not proxies:
            continue

        # Select the appropriate test IDs for the current scope
        current_test_ids = all_test_ids_full if scope == 'full' else all_test_ids_client_only
        if not current_test_ids: # Skip if no relevant tests for this scope
            print(f"Skipping timeline graph for {scope} scope: No relevant test IDs found.")
            continue
            
        x_values = range(len(current_test_ids)) # Numerical x-axis positions
            
        plt.figure(figsize=(18, 10)) # Wider figure for better test ID visibility
        
        # Define a colormap
        colors = plt.cm.tab20(np.linspace(0, 1, len(proxies))) # Using tab20 for more distinct colors

        # Prepare plot data for this scope
        for i, proxy in enumerate(proxies):
            proxy_results = test_results[proxy]
            y_values = []
            for test_id in current_test_ids:
                result = proxy_results.get(test_id, 'other') # Get result, default to 'other'
                # Map result to numerical value, skip if it's 'other' or not in map
                y_value = category_map.get(result)
                y_values.append(y_value if y_value is not None else np.nan) # Use NaN for excluded/missing categories
            
            # Plot the line for this proxy, connecting non-NaN points
            plt.plot(x_values, y_values, marker='.', linestyle='-', markersize=4, 
                     linewidth=1.5, color=colors[i], label=proxy)

        # Configure the plot
        plt.xticks(x_values, current_test_ids, rotation=90, fontsize=8) # Rotate test IDs for readability
        plt.yticks(list(category_map.values()), list(category_map.keys())) # Use category names for Y-axis labels

        plt.xlim(-0.5, len(current_test_ids) - 0.5)
        plt.ylim(-0.5, len(categories) - 0.5) # Adjust ylim based on new categories
        plt.grid(True, axis='both', linestyle='--', alpha=0.5) # Grid on both axes

        scope_title = 'Full Test Suite Proxies' if scope == 'full' else 'Client-side Only Proxies (Client Tests Only)'
        plt.title(f'Test Result Timeline - {scope_title}', fontsize=16, fontweight='bold')
        plt.xlabel('Test ID', fontsize=12)
        plt.ylabel('Result Category', fontsize=12)
        
        # Add legend
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10) # Place legend outside plot area
        
        plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend

        # Save the figure
        filename = f'test_timeline_{scope}.png'
        plt.savefig(os.path.join(output_directory, filename), dpi=300, bbox_inches='tight')
        plt.close()

def create_proxy_matrix_graph(outcomes_dict, proxy_configs, scope_filter, output_directory, client_side_tests_set=None, global_test_ids=None):
    """Creates a matrix visualization of test outcomes filtered by proxy scope."""
    charts_directory = os.path.join(output_directory, 'matrix_graphs')
    os.makedirs(charts_directory, exist_ok=True)

    # Define distinct colors and map for each relevant category
    # 1: Modified (Yellow) - Full scope only
    # 2: Unmodified (Red) - Full scope only
    # 3: Reset (Light Blue)
    # 4: Goaway (Orange)
    # 5: 500 Error (Purple)
    # 6: Not Applicable (Black) - Client-only scope only
    # 7: Received (Red) - Includes Modified/Unmodified for client-only
    # 0: Dropped/Other (Gray)
    colors = {
        1: '#ffd93d',  # Modified (M)
        2: '#ff6b6b',  # Unmodified (U)
        3: '#6bccee',  # Reset (R) - Light Blue
        4: '#ff9f43',  # Goaway (G) - Orange
        5: '#a26bcd',  # 500 Error (E) - Purple
        6: '#000000',  # Not Applicable (N) - Black
        7: '#ff6b6b',  # Received (Rec) - Red
        0: '#cccccc'   # Dropped/Other (D) - Gray
    }
    # Base mapping
    outcome_map = {
        "not_applicable": 6, # Used for client-only filtering
        "dropped": 0,
        "500": 5,
        "goaway": 4,
        "reset": 3,
        "received": 7
    }
    # Add scope-specific mappings
    if scope_filter == 'full':
        outcome_map["modified"] = 1
        outcome_map["unmodified"] = 2
    else: # client-only
        # Map modified/unmodified to Received for client-only
        outcome_map["modified"] = 7
        outcome_map["unmodified"] = 7


    # --- Filtering and Data Preparation ---
    filtered_proxies = sorted([
        proxy for proxy, config in proxy_configs.items()
        if proxy in outcomes_dict and config['scope'] == scope_filter
    ])

    if not filtered_proxies:
        print(f"No proxies found for scope '{scope_filter}'. Skipping matrix graph.")
        return

    # Determine the list of test IDs to use for this graph
    if scope_filter == 'client-only' and global_test_ids is not None:
        # For client-only graph, use the globally provided list
        test_ids_for_graph = global_test_ids
        # Filter out tests >= 106
        test_ids_for_graph = [tid for tid in test_ids_for_graph if int(tid) < 106]
    else:
        # For full scope, derive IDs only from the filtered proxies' results
        test_ids_for_graph = sorted(
            list(set().union(*(outcomes_dict[proxy].keys() for proxy in filtered_proxies))),
            key=lambda x: int(x) if x.isdigit() else float('inf')
        )
        # Ensure full scope also respects global_test_ids if provided, although less typical
        if global_test_ids is not None:
             global_test_ids_set = set(global_test_ids)
             test_ids_for_graph = [tid for tid in test_ids_for_graph if tid in global_test_ids_set]


    if not test_ids_for_graph:
        print(f"No test IDs found for scope '{scope_filter}'. Skipping matrix graph.")
        return

    num_tests = len(test_ids_for_graph)

    matrix_data_numeric = []
    proxy_labels = []

    # Process data (rows = proxies, columns = tests)
    for proxy in filtered_proxies:
        outcomes = outcomes_dict[proxy]
        numerical_outcomes = []
        # Iterate using the determined test ID list for this graph
        for test_id in test_ids_for_graph:
            # Removed redundant check: if scope_filter == 'client-only' and int(test_id) >= 106: continue

            # Check if this test should be marked as "Not Applicable" for client-only scope
            if scope_filter == 'client-only' and client_side_tests_set is not None and test_id not in client_side_tests_set:
                numerical_outcomes.append(outcome_map["not_applicable"]) # Assign 6 (Black)
            else:
                # Otherwise, use the normal result mapping
                result_str = outcomes.get(test_id, "other") # Default to "other" if test missing for this proxy
                # Map the result string using the finalized outcome_map
                numerical_outcomes.append(outcome_map.get(result_str, 0)) # Default to 0 (Dropped/Other)

        matrix_data_numeric.append(numerical_outcomes)
        proxy_labels.append(proxy) # Use original proxy name

    matrix_data = np.array(matrix_data_numeric) # No transpose
    num_proxies_display = len(proxy_labels)
    num_tests_display = num_tests # Use num_tests determined earlier

    # --- Figure and Axes Creation ---
    fig_height = num_proxies_display * 0.4 + 1.5 # Adjust multiplier and base as needed
    fig_width = num_tests_display * 0.15 + 1 # Adjust multiplier and base as needed
    fig = plt.figure(figsize=(fig_width, fig_height))

    ax_matrix = plt.subplot2grid((num_proxies_display + 2, num_tests_display + 1),
                               (0, 0),
                               rowspan=num_proxies_display,
                               colspan=num_tests_display)

    # --- Plot Matrix Rectangles ---
    rect_height = 1.0 # Represents height for one proxy
    rect_width = 1.0  # Represents width for one test
    for i in range(num_proxies_display):  # Iterate over proxies (rows)
        for j in range(num_tests_display):  # Iterate over tests (columns)
            # Check if matrix_data[i][j] exists before accessing
            if i < matrix_data.shape[0] and j < matrix_data.shape[1]:
                outcome = matrix_data[i][j]
                color = colors.get(outcome, colors[0]) # Default to color for 0 if outcome not found
                y_pos = (num_proxies_display - 1 - i) * rect_height
                x_pos = j * rect_width
                rect = plt.Rectangle((x_pos, y_pos), rect_width, rect_height, facecolor=color, edgecolor='white', linewidth=0.5)
                ax_matrix.add_patch(rect)

    # --- Axis and Grid Configuration ---
    ax_matrix.set_xlim(0, num_tests_display * rect_width)
    ax_matrix.set_ylim(0, num_proxies_display * rect_height)

    ax_matrix.set_xticks(np.arange(num_tests_display + 1) * rect_width)
    ax_matrix.set_yticks(np.arange(num_proxies_display + 1) * rect_height)

    # Set minor ticks and labels for X axis (Tests - every 10th)
    x_tick_positions = []
    x_tick_labels = []
    for i, test_id in enumerate(test_ids_for_graph):
        try:
            test_num = int(test_id)
            if test_num % 10 == 0:
                x_tick_positions.append(i * rect_width + rect_width / 2)
                x_tick_labels.append(test_id)
        except ValueError:
            pass
    ax_matrix.set_xticks(x_tick_positions, minor=True)
    ax_matrix.set_xticklabels(x_tick_labels, minor=True, rotation=0, ha='center', fontsize=10)

    # Set minor ticks and labels for Y axis (Proxies)
    ax_matrix.set_yticks(np.arange(num_proxies_display) * rect_height + rect_height / 2, minor=True)
    ax_matrix.set_yticklabels(proxy_labels[::-1], minor=True, fontsize=10)

    # Configure label appearance and grid
    ax_matrix.tick_params(axis='x', which='minor', labelsize=16, bottom=True, top=False, labelbottom=True)
    ax_matrix.tick_params(axis='y', which='minor', labelsize=16, left=True, right=False, labelleft=True)
    ax_matrix.set_xticklabels([], minor=False)
    ax_matrix.set_yticklabels([], minor=False)
    ax_matrix.tick_params(which='major', length=0)
    ax_matrix.grid(True, which='major', color='white', linewidth=1)
    ax_matrix.tick_params(which='minor', length=0)

    # Adjust layout and save
    plt.tight_layout(pad=1.0, rect=[0, 0.05, 1, 0.95])

    filename = f'proxy_outcome_matrix_{scope_filter}.png'

    # --- Add Legend ---
    # Map numerical value back to a display name
    outcome_display_names = {
        1: "Modified",
        2: "Unmodified",
        3: "Reset",
        4: "Goaway",
        5: "Error 500",
        6: "Not Applicable",
        7: "Accepted",
        0: "Dropped", # Changed label for 0
    }

    legend_patches = []
    keys_for_this_legend = []

    if scope_filter == 'client-only':
        # Order: Reset(3), Goaway(4), 500(5), Received(7), Dropped(0), Not Applicable(6)
        keys_for_this_legend = [0, 5, 4, 3, 7, 6]
        # Note: Modified(1)/Unmodified(2) are mapped to Received(7) in outcome_map for this scope
    else: # scope_filter == 'full'
        # Order: Modified(1), Unmodified(2), Reset(3), Goaway(4), 500(5), Received(7), Dropped(0)
        keys_for_this_legend = [0, 5, 4, 3, 2, 1]
        # Not Applicable(6) is omitted

    for key in keys_for_this_legend:
        if key in colors:
            display_name = outcome_display_names.get(key, f"Unknown ({key})")
            legend_patches.append(mpatches.Patch(color=colors[key], label=display_name))

    fig.legend(handles=legend_patches, loc='lower center', ncol=len(legend_patches),
               bbox_to_anchor=(0.5, 0), frameon=False, fontsize=16)

    plt.savefig(os.path.join(charts_directory, filename),
                dpi=300, bbox_inches='tight')
    plt.close(fig) # Close the figure explicitly

# // === Start Refactor for Combined Plots ===

# Define the new helper function that plots on a given Axes object
def _plot_radar_on_ax(ax, proxies_to_plot, scope, test_results, proxy_configs, 
                      global_tick_values_log, global_tick_labels, global_max_log_display, 
                      title_prefix="Radar Chart"):
    """Plots a single radar chart onto a given Matplotlib Axes object (ax)."""
    
    # --- This function assumes ax is already a polar subplot ---
    # It does NOT create a figure or save it.

    # Define categories and outcome map based on scope
    if scope == 'full':
        categories = ['Dropped', '500 Error', 'GOAWAY', 'RESET', 'Unmodified', 'Modified']
        category_keys = ['dropped', '500', 'goaway', 'reset', 'unmodified', 'modified']
    else: # client-only
        categories = ['Dropped', '500 Error', 'GOAWAY', 'RESET', 'Accepted']
        category_keys = ['dropped', '500', 'goaway', 'reset', 'accepted']

    inverse_outcome_map = {
        "dropped": "dropped", "500": "500", "goaway": "goaway", "reset": "reset",
        "modified": "modified" if scope == 'full' else "accepted",
        "unmodified": "unmodified" if scope == 'full' else "accepted",
        "received": "accepted" if scope == 'client-only' else None,
        "other": None
    }
    N = len(categories)
    if N == 0: return # Should not happen if scope is valid

    # Calculate counts per proxy
    counts_per_proxy = {}
    valid_proxies_in_plot = []
    for proxy in proxies_to_plot:
        if proxy not in test_results:
            continue
        valid_proxies_in_plot.append(proxy)
        counts = {key: 0 for key in category_keys}
        for test_id, result_str in test_results[proxy].items():
            category = inverse_outcome_map.get(result_str)
            if category in counts: counts[category] += 1
        counts_per_proxy[proxy] = counts

    if not valid_proxies_in_plot:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, 0.5, "No data", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=9)
        ax.set_title(title_prefix + ": No Data", size=10, y=1.15)
        return

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1] # Close the loop

    # Configure ticks and labels on the passed ax
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=9) # Smaller font for subplots
    ax.set_yticks(global_tick_values_log)
    ax.set_yticklabels(global_tick_labels, size=7) # Smaller font for subplots
    ax.set_ylim(0, global_max_log_display * 1.1 if global_max_log_display > 0 else 0.1)

    # Get display names and colors
    proxy_label_map = {}
    proxy_color_map = {}
    default_color_idx = 0
    # Custom fallback colors (replace orange with red)
    custom_fallback_colors = [
        '#1f77b4',  # tab:blue
        '#d62728',  # tab:red (instead of orange)
        '#2ca02c',  # tab:green
        '#ff7f0e',  # tab:orange (moved here, was red)
        '#9467bd',  # tab:purple
        '#8c564b',  # tab:brown
        '#e377c2',  # tab:pink
        '#7f7f7f',  # tab:gray
        '#bcbd22',  # tab:olive
        '#17becf'   # tab:cyan
    ]
 
    for proxy in valid_proxies_in_plot:
         config = proxy_configs.get(proxy, {})
         proxy_label_map[proxy] = config.get('label', proxy)
         proxy_color_map[proxy] = config.get('color')
         if not proxy_color_map[proxy]:
             proxy_color_map[proxy] = custom_fallback_colors[default_color_idx % len(custom_fallback_colors)]
             default_color_idx += 1

    # Plot lines and annotations on the passed ax
    for proxy_index, proxy in enumerate(valid_proxies_in_plot):
        proxy_counts = counts_per_proxy[proxy]
        ordered_counts = [proxy_counts.get(key, 0) for key in category_keys]
        log_data = np.log10(np.array(ordered_counts) + 1)
        log_data_closed = np.concatenate((log_data, [log_data[0]]))

        label = proxy_label_map[proxy]
        color = proxy_color_map[proxy]

        ax.plot(angles, log_data_closed, linewidth=2.5, linestyle='solid', label=label, color=color) # Increased linewidth

        proxy_radial_offset = proxy_index * (global_max_log_display * 0.015)
        for i in range(N):
            count = ordered_counts[i]
            log_val = log_data[i]
            angle = angles[i]
            # Removed count annotation logic

    # Set title and legend on the passed ax
    plotted_labels = [proxy_label_map[p] for p in valid_proxies_in_plot]
    if len(plotted_labels) <= 2:
        # For pairs, just use the labels
        title_detail = ' vs '.join(plotted_labels)
    else:
        # For combined, use count
        title_detail = f"{len(plotted_labels)} Proxies"
    
    effective_title_prefix = title_prefix
    # Special handling for combined remaining charts to add scope
    if len(valid_proxies_in_plot) > 2 and 'Remaining' in title_prefix:
         effective_title_prefix = f"{title_prefix} (Scope: {scope})"

    title_str = f"{effective_title_prefix}: {title_detail}"
    # ax.set_title(title_str, size=9, y=1.18) # REMOVED subplot titles
    # Use a smaller legend, placed slightly differently for subplots
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=min(len(plotted_labels), 4), fontsize=10) # Increased legend fontsize

# Renamed original function - this now ONLY saves single charts (for remaining)
# It calls the helper function above.
def _save_single_radar_chart_figure(proxies_to_plot, scope, test_results, proxy_configs, output_path, 
                                    global_tick_values_log, global_tick_labels, global_max_log_display,
                                    title_prefix="Radar Chart"):
    """Creates and saves a single radar chart figure. Used for 'remaining' proxies."""
    
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True)) # Slightly smaller figure
    
    # Call the core plotting function to draw on the axes
    _plot_radar_on_ax(ax, proxies_to_plot, scope, test_results, proxy_configs, 
                      global_tick_values_log, global_tick_labels, global_max_log_display, 
                      title_prefix=title_prefix)
    
    # Save and close the individual figure
    try:
        plt.tight_layout(pad=2.0) # Adjust padding
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved single radar chart: {output_path}")
    except Exception as e:
        print(f"Error saving single radar chart {output_path}: {e}")
    finally:
        plt.close(fig) 

# // === End Refactor ===

# // ... function _calculate_global_radar_scale should be defined before this ...

# // ... function create_proxy_radar_chart needs modification in the next step ...

def _calculate_global_radar_scale(test_results, proxy_configs):
    """Calculate global max count and corresponding log ticks across all proxies."""
    # --- Use fixed ticks based on user request --- 
    target_counts = [0, 1, 10, 100]
    tick_labels = [str(c) for c in target_counts]
    tick_values_log = [np.log10(c + 1) for c in target_counts]
    max_log_display = tick_values_log[-1] # The log value corresponding to 166

    print(f"Using Fixed Radar Scale: Counts={target_counts}, Ticks={tick_labels}")
    return tick_values_log, tick_labels, max_log_display

def create_proxy_radar_chart(test_results, proxy_configs, output_directory):
    """Create radar charts: combined for pairs, separate for remaining."""
    charts_directory = os.path.join(output_directory, 'radar_charts')
    os.makedirs(charts_directory, exist_ok=True)

    # Identify old/new pairs
    print("Searching for old/new proxy pairs based on config...")
    old_new_pairs = [] # List of tuples: (old_proxy_name, new_proxy_name, scope)
    paired_proxies_set = set()
    proxies_by_base_name = defaultdict(list)

    for proxy_name, config in proxy_configs.items():
        parts = proxy_name.rsplit('-', 1)
        if len(parts) > 1:
            base_name = parts[0]
            proxies_by_base_name[base_name].append(proxy_name)
        else:
            proxies_by_base_name[proxy_name].append(proxy_name)

    for base_name, proxy_list in proxies_by_base_name.items():
        old_proxy, new_proxy = None, None
        for proxy_name in proxy_list:
            config = proxy_configs.get(proxy_name, {})
            version_tag = config.get('version')
            if version_tag == 'old': old_proxy = proxy_name
            elif version_tag == 'new': new_proxy = proxy_name

        if old_proxy and new_proxy:
            if old_proxy in test_results and new_proxy in test_results:
                scope_old = proxy_configs[old_proxy].get('scope')
                scope_new = proxy_configs[new_proxy].get('scope')
                if scope_old and scope_old == scope_new:
                    old_new_pairs.append((old_proxy, new_proxy, scope_old))
                    paired_proxies_set.add(old_proxy)
                    paired_proxies_set.add(new_proxy)
                    print(f"  Found valid pair for '{base_name}': ({old_proxy}, {new_proxy}) in scope {scope_old}")
                else:
                    print(f"  Skipping pair for '{base_name}': Scopes mismatch ('{scope_old}' vs '{scope_new}')")
            else:
                print(f"  Skipping pair for '{base_name}': One or both not in test_results.")

    # Identify remaining proxies
    print("Identifying remaining proxies...")
    remaining_proxies = {proxy: config for proxy, config in proxy_configs.items() 
                         if proxy in test_results and proxy not in paired_proxies_set}
    print(f"Found {len(remaining_proxies)} remaining proxies.")

    # Calculate global scale (based on all results)
    print("Calculating global radar scale...")
    global_tick_values_log, global_tick_labels, global_max_log_display = _calculate_global_radar_scale(test_results, proxy_configs)

    # --- Generate COMBINED chart for old/new pairs --- 
    num_pairs = len(old_new_pairs)
    if num_pairs > 0:
        print(f"Generating comparison radar charts for {num_pairs} pairs...")
        
        # Determine grid size (FIXED to 2x5)
        ncols = 5 # Fixed at 5 columns
        nrows = 2 # Fixed at 2 rows
        # Check if enough pairs exist for a 2x5 grid
        if num_pairs > nrows * ncols:
             print(f"Warning: More than {nrows*ncols} pairs found ({num_pairs}), but grid is fixed to {nrows}x{ncols}. Only the first {nrows*ncols} will be plotted.")
             num_pairs_to_plot = nrows * ncols
        else:
             num_pairs_to_plot = num_pairs # Plot all pairs if they fit

        figsize_width = ncols * 4.5 # Adjust size based on more columns
        figsize_height = nrows * 5  # Adjust size based on fewer rows

        fig, axes = plt.subplots(nrows, ncols, figsize=(figsize_width, figsize_height), 
                                 subplot_kw=dict(polar=True))
        
        # ... (rest of the function: flatten axes, loop through pairs up to num_pairs_to_plot, hide unused) ...
        if isinstance(axes, np.ndarray):
             axes_flat = axes.flatten()
        elif isinstance(axes, plt.Axes): # Single subplot case
             axes_flat = [axes]
        else: 
             axes_flat = []

        # Loop only up to the number of pairs we decided to plot
        plotted_count = 0
        for i, (old_proxy, new_proxy, scope) in enumerate(old_new_pairs):
            if plotted_count >= num_pairs_to_plot:
                 break # Stop if we filled the grid
            
            if i < len(axes_flat):
                ax = axes_flat[i]
                old_label = proxy_configs.get(old_proxy, {}).get('label', old_proxy)
                new_label = proxy_configs.get(new_proxy, {}).get('label', new_proxy)
                # Title prefix is still needed for _plot_radar_on_ax internal logic if needed, but won't be displayed
                title_for_helper = f"{old_label} vs {new_label}" 
                
                _plot_radar_on_ax(ax, [old_proxy, new_proxy], scope, test_results, proxy_configs, 
                                  global_tick_values_log, global_tick_labels, global_max_log_display, 
                                  title_prefix=title_for_helper)
                plotted_count += 1
            else:
                 # This shouldn't be reached if num_pairs_to_plot logic is correct
                 print("Warning: Indexing error during subplotting.")
                 break 

        # Hide unused subplots (all axes beyond the plotted count)
        for j in range(plotted_count, len(axes_flat)):
            axes_flat[j].axis('off')

        # Adjust layout and save the combined figure
        try:
            # Add a main title? Optional.
            # fig.suptitle("Old vs New Proxy Comparisons", fontsize=16)
            plt.tight_layout(rect=[0, 0.03, 1, 0.97]) # Adjust rect to make space for suptitle if used
            combined_output_path = os.path.join(charts_directory, "radar_comparison_all_pairs.png")
            plt.savefig(combined_output_path, dpi=300)
            print(f"Saved combined comparison radar chart: {combined_output_path}")
        except Exception as e:
            print(f"Error saving combined radar chart: {e}")
        finally:
            plt.close(fig)
    else:
        print("No old/new pairs found to generate combined chart.")

    # --- Generate SEPARATE charts for remaining proxies --- 
    print(f"Generating separate radar charts for {len(remaining_proxies)} remaining proxies...")
    remaining_by_scope = defaultdict(list)
    for proxy, config in remaining_proxies.items():
         scope = config.get('scope')
         if scope:
             remaining_by_scope[scope].append(proxy)

    for scope, proxies_in_scope in remaining_by_scope.items():
        if proxies_in_scope:
            print(f"  Generating chart for {len(proxies_in_scope)} remaining proxies in scope '{scope}'...")
            output_file = os.path.join(charts_directory, f"radar_remaining_{scope}.png")
            # Use the function that saves individual files
            _save_single_radar_chart_figure(proxies_in_scope, scope, test_results, proxy_configs, output_file, 
                                          global_tick_values_log, global_tick_labels, global_max_log_display,
                                          title_prefix="Remaining Proxies") # Pass specific title prefix

    print("Finished creating proxy radar charts.")

def _find_old_new_pairs(proxy_configs, test_results):
    """Identifies pairs of (old_proxy, new_proxy) based on config and availability in results."""
    old_new_pairs = []
    proxies_by_base_name = defaultdict(list)

    # Group proxies by base name (e.g., 'Nghttpx')
    for proxy_name, config in proxy_configs.items():
        parts = proxy_name.rsplit('-', 1)
        base_name = parts[0] if len(parts) > 1 else proxy_name
        proxies_by_base_name[base_name].append(proxy_name)

    # Find old/new pairs within each base name group
    for base_name, proxy_list in proxies_by_base_name.items():
        old_proxy, new_proxy = None, None
        for proxy_name in proxy_list:
            # Only consider proxies that actually have results
            if proxy_name not in test_results:
                continue

            config = proxy_configs.get(proxy_name, {})
            version_tag = config.get('version')
            if version_tag == 'old':
                old_proxy = proxy_name
            elif version_tag == 'new':
                new_proxy = proxy_name

        # Add pair if both found and have results
        if old_proxy and new_proxy:
             # No need to check scope similarity here, just need the pair
             old_new_pairs.append((old_proxy, new_proxy))
             # print(f"  Found valid pair for behavior change matrix: ({old_proxy}, {new_proxy})") # Optional debug print
        # else:
             # Optional: print why a pair wasn't formed for this base_name
             # print(f"  Could not form pair for '{base_name}': old='{old_proxy}', new='{new_proxy}'")


    return old_new_pairs

def create_behavior_change_matrix(all_test_results, proxy_configs, output_directory):
    """
    Creates a heatmap showing the change in proxy behavior counts by subtracting
    the total counts of 'old' proxies from the total counts of 'new' proxies
    for each test and result category. Includes a sum row (expected to be zero).
    (Refactored aggregation logic, updated aesthetics)
    """
    matrix_dir = os.path.join(output_directory, 'behavior_change')
    os.makedirs(matrix_dir, exist_ok=True)

    # 1. Define Categories and Mapping (using full names now)
    categories_display_full = ["Dropped", "Error 500", "GOAWAY", "RESET", "Unmodified", "Modified", "Accepted"]
    category_map_internal_to_full = {
        'dropped': "Dropped", '500': "Error 500", 'goaway': "GOAWAY", 'reset': "RESET",
        'unmodified': "Unmodified", 'modified': "Modified", 'received': "Accepted"
    }
    num_categories = len(categories_display_full)

    # 2. Identify Pairs and separate old/new proxies
    old_new_pairs = _find_old_new_pairs(proxy_configs, all_test_results)
    if not old_new_pairs:
        print("No old/new proxy pairs found for behavior change matrix.")
        return
    # Get unique lists of old and new proxies participating in pairs
    old_proxies_in_pairs = sorted(list(set(pair[0] for pair in old_new_pairs)))
    new_proxies_in_pairs = sorted(list(set(pair[1] for pair in old_new_pairs)))
    print(f"Calculating change based on {len(old_proxies_in_pairs)} old proxies and {len(new_proxies_in_pairs)} new proxies.")

    # 3. Get all relevant test IDs, sorted numerically
    all_test_ids = sorted(
        list(set().union(*(results.keys() for results in all_test_results.values()))),
        key=lambda x: int(x) if x.isdigit() else float('inf')
    )
    all_test_ids = [tid for tid in all_test_ids if tid != '0'] # Exclude test '0'

    num_tests = len(all_test_ids)
    if num_tests == 0:
        print("No valid test results found (excluding test '0') for behavior change matrix.")
        return

    # 4. Initialize Matrix using pandas DataFrame with full category names as index
    change_matrix = pd.DataFrame(0, index=categories_display_full, columns=all_test_ids)

    # 5. Populate Matrix using Aggregate Counts
    for test_id in all_test_ids:
        # <<< Add check for number of proxies reporting this test_id >>>
        old_proxies_with_test = 0
        new_proxies_with_test = 0

        for category_full_name in categories_display_full:
            total_old_count = 0
            total_new_count = 0

            # Sum counts across all old proxies
            for old_proxy in old_proxies_in_pairs:
                result_str = all_test_results.get(old_proxy, {}).get(test_id)
                if category_map_internal_to_full.get(result_str) == category_full_name:
                    total_old_count += 1
                # Count if proxy has *any* result for this test (only once per test)
                if category_full_name == categories_display_full[0] and result_str is not None:
                     old_proxies_with_test += 1


            # Sum counts across all new proxies
            for new_proxy in new_proxies_in_pairs:
                result_str = all_test_results.get(new_proxy, {}).get(test_id)
                if category_map_internal_to_full.get(result_str) == category_full_name:
                    total_new_count += 1
                # Count if proxy has *any* result for this test (only once per test)
                if category_full_name == categories_display_full[0] and result_str is not None:
                     new_proxies_with_test += 1


            # Store the difference of the aggregates
            change_matrix.loc[category_full_name, test_id] = total_new_count - total_old_count

        # Report discrepancy if counts of proxies reporting differ (optional)
        if old_proxies_with_test != new_proxies_with_test:
             print(f"Warning: Test ID {test_id} - Mismatch in reporting proxies: Old={old_proxies_with_test}, New={new_proxies_with_test}.")


    # --- Sum row calculation removed ---
    # column_sums = change_matrix.sum(axis=0)
    # change_matrix.loc['Sum'] = column_sums.astype(int)
    # categories_with_sum = categories_display + ['Sum']
    # num_categories_total = len(categories_with_sum)

    # 6. Create Visualization
    # Adjust figsize for roughly square cells
    cell_size = 0.2 # Inches per cell (adjust as needed)
    figsize_width = max(10, num_tests * cell_size)  # Min width 10 inches
    figsize_height = max(4, num_categories * cell_size) # Min height 4 inches
    # Add constrained_layout=True
    plt.figure(figsize=(figsize_width, figsize_height), constrained_layout=True)

    # Determine color scale bounds (using the final matrix without sum row)
    max_abs_change = change_matrix.abs().max().max()
    if max_abs_change == 0: vmin, vmax = -1, 1
    else: bound = max(1, max_abs_change); vmin, vmax = -bound, bound

    # Plot heatmap
    ax = sns.heatmap(change_matrix,
                annot=False, cmap="coolwarm", linewidths=0.3, linecolor='white',
                center=0, vmin=vmin, vmax=vmax)
    cbar = ax.collections[0].colorbar
    cbar.set_label('Change in Proxy Count', rotation=270, labelpad=15, fontsize=16)

    # Update axis labels
    plt.xlabel('Test ID', fontsize=20)
    plt.ylabel('Behavior', fontsize=20) # Changed Y-axis label

    # --- Set X ticks explicitly for 5, 10, 15, ... ---
    # Create a map from test ID string to its index
    test_id_to_index = {test_id: i for i, test_id in enumerate(all_test_ids)}

    # Determine the max test ID to set the limit for labels
    max_test_id_num = 0
    if all_test_ids:
        try:
            # Find the maximum numeric test ID
            max_test_id_num = max(int(tid) for tid in all_test_ids if tid.isdigit())
        except ValueError:
            pass # Handle cases where no numeric IDs are found

    # Generate desired labels (5, 10, 15...) and find their corresponding indices
    desired_labels = []
    tick_positions = []
    if max_test_id_num > 0:
        for i in range(5, max_test_id_num + 1, 5):
            label_str = str(i)
            if label_str in test_id_to_index: # Check if this test ID actually exists in the data
                desired_labels.append(label_str)
                tick_positions.append(test_id_to_index[label_str])

    # Set the ticks if any were found
    if tick_positions:
        ax.set_xticks(np.array(tick_positions) + 0.5) # Center ticks on the corresponding cells
        ax.set_xticklabels(desired_labels)
    else:
        # Fallback if no '5', '10', etc. ticks found (unlikely but safe)
        ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=min(num_tests, 15), integer=True))

    plt.xticks(rotation=90, fontsize=16)
    # Y ticks use the full category names from the index
    plt.yticks(rotation=0, fontsize=16)
    # Remove fig.subplots_adjust(...)
    # fig.subplots_adjust(left=0.15, right=0.9, bottom=0.2, top=0.95)

    # 7. Save Plot
    output_path = os.path.join(matrix_dir, "behavior_change_matrix_aggregated_square.png") # New filename
    try:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved aggregated square behavior change matrix: {output_path}")
    except Exception as e:
        print(f"Error saving aggregated square behavior change matrix {output_path}: {e}")
    finally:
        plt.close()

    # Add this function definition after create_proxy_matrix_graph 
# and before the main function or radar chart functions

def create_dual_scope_comparison_matrix(all_test_results_full, proxy_configs, client_side_tests_set, results_dir, output_directory):
    """
    Creates a matrix graph comparing full-scope and client-only scope results 
    for proxies tested under both configurations.

    Args:
        all_test_results_full: Dictionary containing results for primary (full) scope proxies.
        proxy_configs: Dictionary mapping proxy names to their configurations.
        client_side_tests_set: A set of test IDs classified as client-side tests.
        results_dir: The base directory where individual proxy result folders are located.
        output_directory: The directory to save the generated comparison graphs.
    """
    comparison_charts_directory = os.path.join(output_directory, 'dual_scope_comparison')
    os.makedirs(comparison_charts_directory, exist_ok=True)

    # Define colors and mapping for the comparison graph
    # Using distinct numerical values to avoid overlap where possible
    colors = {
        0: '#cccccc',  # Dropped (Gray) - Both
        1: '#ffd93d',  # Modified (Yellow) - Full Only
        2: '#ff6b6b',  # Unmodified (Red) - Full Only
        3: '#6bccee',  # Reset (Light Blue) - Both
        4: '#ff9f43',  # Goaway (Orange) - Both
        5: '#a26bcd',  # 500 Error (Purple) - Both
        6: '#000000',  # Not Applicable (Black) - NEW
        7: '#2ecc71',  # Accepted (Green) - Client Only (from received/modified/unmodified)
        -1: '#ffffff'  # Represents missing data point (White) - Not in legend
    }
    not_applicable_value = 6 # Define the value for N/A

    # Mapping for full scope row (client tests only)
    full_scope_map = {
        "modified": 1, "unmodified": 2, "reset": 3, "goaway": 4,
        "500": 5, "dropped": 0, "received": 0 # Treat 'received' in full scope on client test as 'dropped'
    }
    # Mapping for client-only scope row
    client_scope_map = {
        "received": 7, "modified": 7, "unmodified": 7, # Map all success types to 'Accepted'
        "reset": 3, "goaway": 4, "500": 5, "dropped": 0
    }

    # Legend definitions
    legend_labels = {
        1: "Modified (Full)", 2: "Unmodified (Full)", 7: "Accepted (Client)",
        3: "Reset", 4: "Goaway", 5: "Error 500", 0: "Dropped/Other",
        6: "Not Applicable" # Add N/A to legend labels
    }
    # Adjust legend order if desired, adding 6
    legend_order = [1, 2, 7, 3, 4, 5, 0, 6] 

    # Find proxies configured for dual scope
    dual_scope_proxies = []
    for proxy_name, config in proxy_configs.items():
        if config.get('scope') == 'full' and config.get('second-scope') == 'client-only':
            if proxy_name in all_test_results_full: # Check if primary results exist
                 dual_scope_proxies.append(proxy_name)
            else:
                 print(f"Skipping dual-scope comparison for {proxy_name}: Primary results missing.")


    print(f"Found {len(dual_scope_proxies)} proxies for dual-scope comparison: {dual_scope_proxies}")

    # Generate graph for each dual-scope proxy
    for proxy_name in dual_scope_proxies:
        print(f"Generating comparison matrix for: {proxy_name}")
        
        # 1. Get primary (full scope) results
        primary_results = all_test_results_full[proxy_name]

        # 2. Load secondary (client-only scope / H2H1) results
        secondary_proxy_name = proxy_name + "-H2H1"
        secondary_proxy_dir = os.path.join(results_dir, secondary_proxy_name)
        secondary_results = {}
        test_messages_secondary = {} # Placeholder if needed

        if not os.path.exists(secondary_proxy_dir):
            print(f"  Warning: Secondary results directory not found: {secondary_proxy_dir}. Skipping {proxy_name}.")
            continue
            
        latest_secondary_file = get_latest_file(secondary_proxy_dir)
        if not latest_secondary_file:
            print(f"  Warning: No results file found in {secondary_proxy_dir}. Skipping {proxy_name}.")
            continue

        try:
            # Analyze the secondary results explicitly using 'client-only' scope setting
            _, _, _, _, _, _, _, secondary_results, test_messages_secondary = analyze_results(latest_secondary_file, 'client-only')
            # No need to check if secondary_results is empty here, as we use a fixed range
        except Exception as e:
            print(f"  Error analyzing secondary results file {latest_secondary_file} for {proxy_name}: {e}. Skipping.")
            continue

        # 3. Define the fixed range of test IDs for the columns
        test_ids_1_to_105 = [str(i) for i in range(1, 106)] 
        num_tests = len(test_ids_1_to_105) # Will always be 105

        print(f"  Generating comparison matrix for fixed test IDs 1-105.")

        # 4. Create the 2xN numerical matrix (N=105)
        matrix_data_numeric = np.full((2, num_tests), -1, dtype=int) # Initialize with -1 (missing)

        # 5. Populate the matrix based on the fixed test ID list
        tests_marked_na = 0
        tests_missing_primary = 0
        tests_missing_secondary = 0

        for j, test_id in enumerate(test_ids_1_to_105):
            # Check if the test is classified as client-side
            if test_id not in client_side_tests_set:
                # Mark as Not Applicable in both rows
                matrix_data_numeric[0, j] = not_applicable_value 
                matrix_data_numeric[1, j] = not_applicable_value 
                tests_marked_na += 1
            else:
                # Test *is* classified as client-side

                # Row 0: Full Scope (Client Test)
                if test_id in primary_results: 
                    full_result_str = primary_results.get(test_id) 
                    matrix_data_numeric[0, j] = full_scope_map.get(full_result_str, 0) # Default mapped value to Dropped
                else:
                    # Primary results missing this specific client-side test
                    matrix_data_numeric[0, j] = 0 # Mark as Dropped 
                    tests_missing_primary += 1

                # Row 1: Client-Only Scope (Client Test)
                if test_id in secondary_results:
                    client_result_str = secondary_results.get(test_id) 
                    matrix_data_numeric[1, j] = client_scope_map.get(client_result_str, 0) # Default mapped value to Dropped
                else:
                    # Secondary results missing this specific client-side test
                    matrix_data_numeric[1, j] = 0 # Mark as Dropped
                    tests_missing_secondary += 1
        
        # Print summary stats for this proxy
        print(f"    Tests marked N/A: {tests_marked_na}")
        if tests_missing_primary > 0:
             print(f"    Client tests missing in primary results: {tests_missing_primary}")
        if tests_missing_secondary > 0:
             print(f"    Client tests missing in secondary results: {tests_missing_secondary}")


        # 6. Plotting Logic (Uses test_ids_1_to_105 for x-axis)
        num_scopes = 2
        row_labels = ['Full Scope', 'Client-Only Scope'] 

        # --- Figure and Axes Creation ---
        fig_height = num_scopes * 0.8 + 1.5 
        # Recalculate width based on fixed 105 tests
        fig_width = max(12, num_tests * 0.12 + 1) # Adjusted multiplier slightly for 105 tests
        fig = plt.figure(figsize=(fig_width, fig_height))
        ax_matrix = fig.add_subplot(111) 

        # --- Plot Matrix Rectangles ---
        # (This part remains the same)
        rect_height = 1.0 
        rect_width = 1.0
        for i in range(num_scopes):
            for j in range(num_tests): 
                outcome = matrix_data_numeric[i, j]
                color = colors.get(outcome, colors[-1]) 
                y_pos = (num_scopes - 1 - i) * rect_height 
                x_pos = j * rect_width
                rect = plt.Rectangle((x_pos, y_pos), rect_width, rect_height, facecolor=color, edgecolor='white', linewidth=0.5)
                ax_matrix.add_patch(rect)

        # --- Axis and Grid Configuration ---
        ax_matrix.set_xlim(0, num_tests * rect_width)
        ax_matrix.set_ylim(0, num_scopes * rect_height)

        # X-axis: Test IDs (Use test_ids_1_to_105)
        x_tick_positions = []
        x_tick_labels = []
        for i, test_id in enumerate(test_ids_1_to_105): # Iterate over the fixed list 1-105
            try:
                test_num = int(test_id)
                # Show labels every 5 tests
                if test_num % 5 == 0: 
                    x_tick_positions.append(i * rect_width + rect_width / 2)
                    x_tick_labels.append(test_id)
            except ValueError:
                pass # Should not happen for 1-105
        ax_matrix.set_xticks(x_tick_positions)
        ax_matrix.set_xticklabels(x_tick_labels, rotation=90, ha='center', fontsize=9) # Smaller font for more ticks
        ax_matrix.tick_params(axis='x', which='major', bottom=True, top=False, labelbottom=True)

        # Y-axis: Scope Labels (Remains the same)
        ax_matrix.set_yticks(np.arange(num_scopes) * rect_height + rect_height / 2)
        ax_matrix.set_yticklabels(row_labels[::-1], fontsize=12) 
        ax_matrix.tick_params(axis='y', which='major', left=True, right=False, labelleft=True)
        
        # --- Cleanup Ticks/Grid (Remains the same) ---
        ax_matrix.set_xticks([], minor=True)
        ax_matrix.set_yticks([], minor=True)
        ax_matrix.grid(False) 
        ax_matrix.tick_params(which='both', length=0) 
        
        # --- Add Legend (Remains the same) ---
        legend_patches = []
        for key in legend_order:
             if key in colors and key in legend_labels:
                 legend_patches.append(mpatches.Patch(color=colors[key], label=legend_labels[key]))
        num_legend_items = len(legend_patches)
        legend_cols = min(num_legend_items, 4) 
        fig.legend(handles=legend_patches, loc='lower center', ncol=legend_cols, 
                   bbox_to_anchor=(0.5, 0.01), frameon=False, fontsize=11)

        # --- Titles and Layout ---
        # plt.title(f'Dual Scope Comparison: {proxy_name}', fontsize=14, fontweight='bold', pad=20) 
        plt.xlabel('Test ID', fontsize=8) # Update X label
        plt.tight_layout(pad=2.0, rect=[0, 0.1, 1, 0.95]) # Adjust rect bottom for legend space

        # --- Save Figure ---
        # (Save logic remains the same)
        filename = f'dual_scope_comparison_{proxy_name}_1-105.png' # Added range to filename
        output_path = os.path.join(comparison_charts_directory, filename)
        try:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"  Saved comparison matrix: {output_path}")
        except Exception as e:
            print(f"  Error saving comparison matrix {output_path}: {e}")
        finally:
            plt.close(fig) 

    print("Finished dual-scope comparison matrix generation.")


# --- In main() function ---
# Find the block where client_server_dir and client_side_tests are handled


def main():
    # Create base directories if they don't exist
    # Define base directories and their subdirectories
    base_dirs_config = {
        'analysis': ['tables', 'outliers', 'cloudflare', 'behavior', 'conformance', 'correlation'],
        os.path.join('analysis', 'behavior'): ['proxies', 'radar_charts', 'matrix_graphs', 'behavior_change', 'dual_scope_comparison'] # Added 'behavior_change' and 'dual_scope_comparison'
    }

    # Create directories recursively based on the config
    created_dirs = set() # Keep track of created dirs to avoid redundant makedirs calls
    for base_dir, subdirs_or_nested in base_dirs_config.items():
        if base_dir not in created_dirs:
            os.makedirs(base_dir, exist_ok=True)
            created_dirs.add(base_dir)

        if isinstance(subdirs_or_nested, list):
            for subdir in subdirs_or_nested:
                dir_path = os.path.join(base_dir, subdir)
                if dir_path not in created_dirs:
                    os.makedirs(dir_path, exist_ok=True)
                    created_dirs.add(dir_path)
        elif isinstance(subdirs_or_nested, dict): # Handle potential future nested dicts if needed
             pass # Currently only lists are used for subdirs


    # List of proxy folders with their test scope
    # (Adding labels and colors for better plots later, if needed)
    proxy_configs = {
        'Nghttpx-1.62.1': {'scope': 'full', 'version': 'new', 'second-scope': 'client-only'},
        # 'Nghttpx-1.47.0': {'scope': 'full', 'version': 'old'},
        'HAproxy-2.9.10': {'scope': 'full', 'version': 'new', 'second-scope': 'client-only'},
        # 'HAproxy-2.6.0': {'scope': 'full', 'version': 'old'},
        'Apache-2.4.62': {'scope': 'full', 'version': 'new', 'second-scope': 'client-only'},
        # 'Apache-2.4.53': {'scope': 'full', 'version': 'old'},
        'Caddy-2.9.1': {'scope': 'full', 'version': 'new'},
        'Node-20.16.0': {'scope': 'full', 'version': 'new', 'second-scope': 'client-only'},
        # 'Node-14.19.3': {'scope': 'full', 'version': 'old'},
        'Envoy-1.32.2': {'scope': 'full', 'version': 'new', 'second-scope': 'client-only'},
        # 'Envoy-1.21.2': {'scope': 'full', 'version': 'old', 'second-scope': 'client-only'},
        'H2O-26b116e95': {'scope': 'full', 'version': 'new', 'second-scope': 'client-only'},
        # 'H2O-cf59e67c3': {'scope': 'full', 'version': 'old'},
        'Mitmproxy-11.1.0': {'scope': 'full', 'version': 'new'},
        'Traefik-3.3.5': {'scope': 'full', 'version': 'new', 'second-scope': 'client-only'},
        # 'Traefik-2.6.2': {'scope': 'full', 'version': 'old'},
        'Nginx-1.26.0': {'scope': 'client-only', 'version': 'new'},
        # 'Nginx-1.22.0': {'scope': 'client-only', 'version': 'old'},
        'Lighttpd-1.4.76': {'scope': 'client-only', 'version': 'new'},
        # 'Lighttpd-1.4.64': {'scope': 'client-only', 'version': 'old'},
        'Varnish-7.7.0': {'scope': 'client-only', 'version': 'new'},
        # 'Varnish-7.1.0': {'scope': 'client-only', 'version': 'old'},
        'Azure-AG': {'scope': 'client-only', 'version': 'N/A'},
        'Cloudflare': {'scope': 'full', 'version': 'N/A', 'second-scope': 'client-only'},
        'Fastly': {'scope': 'client-only', 'version': 'N/A'},
    }
    
    results_dir = 'results'
    
    # Prepare data for summary tables
    dropped_counts = {}
    error_500_counts = {}
    goaway_counts = {}
    reset_counts = {}
    received_counts = {}
    modified_counts = {}
    unmodified_counts = {}
    all_test_results = {}
    all_test_messages = {}
    
    for proxy, config in proxy_configs.items():
        proxy_dir = os.path.join(results_dir, proxy)
        if not os.path.exists(proxy_dir):
            continue
            
        latest_file = get_latest_file(proxy_dir)
        if not latest_file:
            continue

        dropped_count, error_500_count, goaway_count, reset_count, received_count, modified_count, unmodified_count, test_results, test_messages = analyze_results(latest_file, proxy_configs[proxy]['scope'])
        dropped_counts[proxy] = dropped_count
        error_500_counts[proxy] = error_500_count
        goaway_counts[proxy] = goaway_count
        reset_counts[proxy] = reset_count
        received_counts[proxy] = received_count
        modified_counts[proxy] = modified_count
        unmodified_counts[proxy] = unmodified_count
        all_test_results[proxy] = test_results
        all_test_messages[proxy] = test_messages

    # Split proxies by scope for different visualizations
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'full']
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'client-only']

    # Create tables with scope indicators
    tables_dir = os.path.join('analysis', 'tables')
    create_result_counts_table(dropped_counts, error_500_counts, goaway_counts, reset_counts, received_counts, all_test_results, proxy_configs, tables_dir)
    create_test_results_matrix(all_test_results, proxy_configs, tables_dir)
    create_test_outcome_by_id_table(all_test_results, tables_dir)
    create_modified_unmodified_summary(all_test_results, tables_dir) # Add call here
    
    # Extract and save outliers
    outliers_dir = os.path.join('analysis', 'outliers')
    extract_and_save_outliers(all_test_results, proxy_configs, outliers_dir)

    # Create correlation visualizations
    correlation_dir = os.path.join('analysis', 'correlation')
    create_proxy_correlation_matrix(all_test_results, proxy_configs, correlation_dir)
    
    # Create distribution visualizations
    distribution_dir = os.path.join('analysis', 'behavior')
    create_proxy_result_pies(all_test_results, proxy_configs, distribution_dir)
    create_proxy_line_graphs(all_test_results, proxy_configs, distribution_dir)
    create_proxy_radar_chart(all_test_results, proxy_configs, distribution_dir) # Call the new function
    # Removed call to create_test_timeline_graphs here, moved after loading client/server tests

    # run cloudflare_analysis.py
    os.system('python cloudflare_analysis.py')

    all_test_results_primary = all_test_results 
    
    # Load client-server classification and create client-server visualizations
    client_side_tests_set = set() # Initialize to empty set
    server_side_tests_set = set()
    try:
        client_server_dir = os.path.join('analysis', 'behavior')
        client_side_tests_set, server_side_tests_set = load_client_server_classification('docs/clientside_vs_serverside.json')
        
        # Run visualizations that depend on client/server classification
        create_client_server_proxy_line_graphs(all_test_results_primary, proxy_configs, client_side_tests_set, server_side_tests_set, client_server_dir)
        create_test_timeline_graphs(all_test_results_primary, proxy_configs, client_side_tests_set, server_side_tests_set, client_server_dir)
        
        conformance_dir = os.path.join('analysis', 'conformance')
        create_client_server_conformance_visualization(all_test_results_primary, client_side_tests_set, server_side_tests_set, proxy_configs, conformance_dir, scope_filter='all')
        create_client_server_conformance_visualization(all_test_results_primary, client_side_tests_set, server_side_tests_set, proxy_configs, conformance_dir, scope_filter='full')
        create_client_server_conformance_visualization(all_test_results_primary, client_side_tests_set, server_side_tests_set, proxy_configs, conformance_dir, scope_filter='client-only')

        # <<-- CALL THE NEW DUAL SCOPE FUNCTION HERE -->>
        if client_side_tests_set: # Ensure classification was loaded
             dual_scope_output_dir = os.path.join('analysis', 'behavior') # Output directory
             create_dual_scope_comparison_matrix(all_test_results_primary, proxy_configs, client_side_tests_set, results_dir, dual_scope_output_dir)
        else:
             print("Skipping dual-scope comparison matrix: Failed to load client-side test classification.")
             
    except FileNotFoundError:
        print("Warning: 'docs/clientside_vs_serverside.json' not found. Skipping client/server specific visualizations and dual-scope comparison.")
    except Exception as e:
        print(f"Error during client-server/dual-scope visualization setup: {e}")

    
    # Create client-server discrepancy visualization (only for full-scope proxies)
    try:
        test_pairs = load_test_pairs()
        full_scope_results = {proxy: results for proxy, results in all_test_results.items() 
                            if proxy_configs[proxy]['scope'] == 'full'}
        create_client_server_discrepancy_visualization(full_scope_results, test_pairs, client_server_dir)
    except Exception as e:
        print(f"Error creating client-server discrepancy visualization: {e}")

    # Create proxy matrix visualization (using behavior directory)
    behavior_dir = os.path.join('analysis', 'behavior') 
    # client_side_tests_set should be loaded from the try block above
        
    if all_test_results_primary:
        # Determine the global set of all test IDs encountered across all results
        global_all_test_ids = sorted(
            list(set().union(*(results.keys() for results in all_test_results_primary.values()))),
            key=lambda x: int(x) if x.isdigit() else float('inf')
        )

        # Full scope graph (uses its own derived test IDs, pass None for global)
        create_proxy_matrix_graph(all_test_results_primary, proxy_configs, 'full', behavior_dir, 
                                client_side_tests_set=None, global_test_ids=None) 
        # Client-only scope graph (pass the client-side test set and the global ID list)
        # Check if client_side_tests_set was loaded successfully before calling
        if client_side_tests_set:
            create_proxy_matrix_graph(all_test_results_primary, proxy_configs, 'client-only', behavior_dir, 
                                    client_side_tests_set=client_side_tests_set, global_test_ids=global_all_test_ids)
        else:
             print("Skipping client-only proxy matrix graph: Client-side test classification not available.")
    else:
        print("Skipping proxy matrix graph: No test results loaded.")

    # Call the new behavior change matrix function HERE
    distribution_dir = os.path.join('analysis', 'behavior') # Confirm correct dir for behavior change
    create_behavior_change_matrix(all_test_results_primary, proxy_configs, distribution_dir)
    # Add the call to the new line graph function
    create_behavior_change_line_graph(all_test_results_primary, proxy_configs, distribution_dir)

def create_behavior_change_line_graph(all_test_results, proxy_configs, output_directory):
    """
    Creates a line graph showing the change in proxy behavior counts (new - old) 
    for each category across different proxy pairs.
    """
    change_dir = os.path.join(output_directory, 'behavior_change')
    os.makedirs(change_dir, exist_ok=True)

    # 1. Define Categories and Mapping
    # Order matters for plotting
    categories_plot = ["Dropped", "Error 500", "GOAWAY", "RESET", "Unmodified", "Modified", "Accepted"]
    category_map_internal_to_plot = {
        'dropped': "Dropped", '500': "Error 500", 'goaway': "GOAWAY", 'reset': "RESET",
        'unmodified': "Unmodified", 'modified': "Modified", 'received': "Accepted"
        # 'other' is ignored
    }
    num_categories = len(categories_plot)

    # Define line styles and colors (ensure enough for num_categories)
    line_styles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 1)), (0, (1, 1))]
    # Using tab10 colors, repeating if necessary
    colors = plt.cm.tab10(np.linspace(0, 1, 10)) 

    # 2. Identify Pairs
    old_new_pairs = _find_old_new_pairs(proxy_configs, all_test_results)
    if not old_new_pairs:
        print("No old/new proxy pairs found for behavior change line graph.")
        return

    # 3. Calculate Differences per Pair and Scope
    differences_by_proxy_base = {} # { 'Nghttpx': {'full': {cat: diff, ...}, 'client-only': {cat: diff,...}}, ...}
    proxy_base_names_full = []
    proxy_base_names_client = []

    for old_proxy, new_proxy in old_new_pairs:
        # Determine base name (assuming format like 'ProxyName-Version')
        base_name = old_proxy.rsplit('-', 1)[0] if '-' in old_proxy else old_proxy
        
        # Get scopes (crucial for correct counting)
        scope_old = proxy_configs.get(old_proxy, {}).get('scope')
        scope_new = proxy_configs.get(new_proxy, {}).get('scope')

        # Process only if scopes match (essential for meaningful comparison)
        if scope_old and scope_new and scope_old == scope_new:
            scope = scope_old # The shared scope
            
            if base_name not in differences_by_proxy_base:
                 differences_by_proxy_base[base_name] = {}
                 if scope == 'full': proxy_base_names_full.append(base_name)
                 else: proxy_base_names_client.append(base_name)

            if scope not in differences_by_proxy_base[base_name]:
                 differences_by_proxy_base[base_name][scope] = {cat: 0 for cat in categories_plot}

            # Get results
            results_old = all_test_results.get(old_proxy, {})
            results_new = all_test_results.get(new_proxy, {})

            # Count occurrences for old and new versions within the scope
            counts_old = {cat: 0 for cat in categories_plot}
            counts_new = {cat: 0 for cat in categories_plot}

            for test_id, result_str in results_old.items():
                category = category_map_internal_to_plot.get(result_str)
                # Special handling for client-only: map modified/unmodified/received to Accepted
                if scope == 'client-only' and category in ["Modified", "Unmodified"]:
                    category = "Accepted" 
                if category in counts_old:
                    counts_old[category] += 1
            
            for test_id, result_str in results_new.items():
                category = category_map_internal_to_plot.get(result_str)
                if scope == 'client-only' and category in ["Modified", "Unmodified"]:
                     category = "Accepted"
                if category in counts_new:
                    counts_new[category] += 1
            
            # Calculate difference (new - old) for each category
            for cat in categories_plot:
                 # Special check for client-only: Modified/Unmodified have diff=0
                 if scope == 'client-only' and cat in ["Modified", "Unmodified"]:
                     diff = 0 
                 else:
                     diff = counts_new[cat] - counts_old[cat]
                 differences_by_proxy_base[base_name][scope][cat] = diff
        else:
             print(f"Skipping pair ({old_proxy}, {new_proxy}) for line graph due to scope mismatch or missing scope.")

    # --- START: Write differences to text file ---
    diff_file_path = os.path.join(change_dir, 'behavior_change_differences.txt')
    try:
        with open(diff_file_path, 'w') as f_diff:
            f_diff.write("Behavior Change Differences (New Count - Old Count)\n")
            f_diff.write("=================================================\n\n")
            
            sorted_proxy_base_names_for_file = sorted(proxy_base_names_full) + sorted(proxy_base_names_client)
            
            for base_name in sorted_proxy_base_names_for_file:
                scope_found = None
                if base_name in proxy_base_names_full:
                    scope_found = 'full'
                elif base_name in proxy_base_names_client:
                    scope_found = 'client-only'
                
                if scope_found and base_name in differences_by_proxy_base and scope_found in differences_by_proxy_base[base_name]:
                    f_diff.write(f"Proxy: {base_name} (Scope: {scope_found})\n")
                    f_diff.write("-------------------------------------\n")
                    diffs = differences_by_proxy_base[base_name][scope_found]
                    for cat in categories_plot:
                         # Only write categories relevant to the scope
                         if scope_found == 'client-only' and cat in ["Modified", "Unmodified"]:
                              continue # Skip M/U for client-only scope
                         if scope_found == 'full' and cat == "Accepted" and not any(diffs.get(c,0) != 0 for c in ["Modified", "Unmodified", "Received"]):
                              # Avoid writing "Accepted: 0" for full scope if M/U/R were all 0 difference
                              # (Since Accepted isn't directly calculated for full scope)
                              # This is a heuristic - might need refinement depending on exact desired output
                              pass # Or potentially continue, if explicit Accepted=0 isn't desired for full scope
                         
                         difference_value = diffs.get(cat, 0)
                         f_diff.write(f"  {cat}: {difference_value}\n")
                    f_diff.write("\n")
                else:
                     f_diff.write(f"Proxy: {base_name} - Data not found for expected scope.\n\n") # Indicate if something went wrong
                     
        print(f"Saved behavior change differences to: {diff_file_path}")
    except Exception as e:
        print(f"Error writing behavior change differences file {diff_file_path}: {e}")
    # --- END: Write differences to text file ---

    # 4. Prepare Data for Plotting
    # Combine and sort proxy names: full scope first, then client-only
    sorted_proxy_base_names = sorted(proxy_base_names_full) + sorted(proxy_base_names_client)
    if not sorted_proxy_base_names:
        print("No valid pairs with matching scopes found to plot.")
        return
        
    plot_data = {cat: [] for cat in categories_plot} # { 'Dropped': [diff1, diff2,...], ...}
    proxy_labels_for_plot = []

    for base_name in sorted_proxy_base_names:
         scope_found = None
         if base_name in proxy_base_names_full:
             scope_found = 'full'
         elif base_name in proxy_base_names_client:
             scope_found = 'client-only'
         
         if scope_found and scope_found in differences_by_proxy_base[base_name]:
             proxy_labels_for_plot.append(base_name)
             diffs = differences_by_proxy_base[base_name][scope_found]
             for cat in categories_plot:
                 plot_data[cat].append(diffs.get(cat, 0)) # Append difference, default to 0
         # Else: skip this base_name if data for its primary scope wasn't calculated

    # 5. Create Visualization
    plt.figure(figsize=(max(10, len(proxy_labels_for_plot) * 0.8), 7)) # Adjust width based on number of proxies
    
    num_full = len(proxy_base_names_full)
    num_client = len(proxy_base_names_client)
    num_total = len(proxy_labels_for_plot)

    for i, category in enumerate(categories_plot):
        style_index = i % len(line_styles)
        color_index = i % len(colors)
        
        # Get the full data series for this category
        full_data_series = np.array(plot_data[category])
        plot_series = full_data_series.astype(float) # Convert to float for NaN

        # Modify the series based on category relevance to scope
        if category in ["Modified", "Unmodified"]:
            # These only apply to full scope. Set client-only part to NaN.
            if num_client > 0 and num_full < num_total:
                plot_series[num_full:] = np.nan
        elif category == "Accepted":
            # This primarily applies to client-only. Set full-scope part to NaN.
            if num_full > 0:
                plot_series[:num_full] = np.nan
        # Else (Dropped, Error 500, GOAWAY, RESET): Plot the full series

        # Only add to plot if there's any non-NaN data in the relevant scope section
        should_plot = False
        if category in ["Modified", "Unmodified"]:
            if num_full > 0 and np.any(~np.isnan(plot_series[:num_full])):
                should_plot = True
        elif category == "Accepted":
            if num_client > 0 and np.any(~np.isnan(plot_series[num_full:])):
                should_plot = True
        else: # Shared categories
            if np.any(~np.isnan(plot_series)):
                should_plot = True
                
        if should_plot:
            plt.plot(proxy_labels_for_plot, plot_series, 
                     label=category, 
                     marker='o', markersize=5,
                     linestyle=line_styles[style_index], 
                     color=colors[color_index],
                     linewidth=1.5)

    # Add horizontal line at y=0
    plt.axhline(0, color='grey', linestyle='--', linewidth=1)

    # Add vertical separator if both full and client-only proxies exist
    # num_full = len(proxy_base_names_full)
    if num_full > 0 and len(proxy_base_names_client) > 0:
        plt.axvline(x=num_full - 0.5, color='black', linestyle=':', linewidth=1.5) # Removed label here to avoid duplication
        # Add text annotation for scopes
        # Determine y-position dynamically based on plot limits
        ymin, ymax = plt.ylim()
        text_y_pos = ymax - (ymax - ymin) * 0.05 # Place slightly below the top
        
        plt.text((num_full / 2.0) - 0.5, text_y_pos, 'Full Scope', ha='center', va='top', fontsize=10, color='black', backgroundcolor='white', alpha=0.8)
        plt.text(num_full + (len(proxy_base_names_client) / 2.0) - 0.5, text_y_pos, 'Client-Only Scope', ha='center', va='top', fontsize=10, color='black', backgroundcolor='white', alpha=0.8)


    # Customize plot
    plt.xlabel('Proxy', fontsize=12)
    plt.ylabel('Change in Count (New - Old)', fontsize=12)
    # plt.title('Change in Test Outcome Counts Between Proxy Versions', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10) # Legend outside plot
    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout for legend

    # 6. Save Plot
    output_path = os.path.join(change_dir, "behavior_change_line_graph.png")
    try:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved behavior change line graph: {output_path}")
    except Exception as e:
        print(f"Error saving behavior change line graph {output_path}: {e}")
    finally:
        plt.close()


# Add this function definition after create_proxy_matrix_graph 
# and before the main function or radar chart functions

if __name__ == "__main__":
    main()