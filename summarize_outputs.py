import json
import os
from datetime import datetime
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from collections import defaultdict
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches

def get_latest_file(directory):
    """Get the most recent file in the directory."""
    files = glob.glob(os.path.join(directory, "*.json"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def analyze_results(filename):
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
            test_results[test_id] = "other"
            test_messages[test_id] = "No result data"
            continue
        
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
            # skip this test
            continue
        
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
            print(result)
        
        test_messages[test_id] = message
    
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
    plt.bar(x - width/2, client_non_conformant, width, label='Client Non-Conformant', color='#2ecc71')
    plt.bar(x + width/2, server_non_conformant, width, label='Server Non-Conformant', color='#3498db')
    
    # Customize the plot
    plt.xlabel('Proxy')
    plt.ylabel('Percentage of Non-Conformant Tests')
    
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
        
    plt.title(f'HTTP/2 Client-Side vs Server-Side Non-Conformance by Proxy{title_suffix}', pad=20)
    plt.xticks(x, proxies, rotation=45, ha='right')
    plt.legend()
    
    # Add percentage labels on the bars
    def add_labels(x_pos, heights):
        for i, height in enumerate(heights):
            if height > 0:  # Only add label if there's a non-zero value
                plt.text(x_pos[i], height + 1,
                        f'{height:.1f}%',
                        ha='center', va='bottom')
    
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
    plt.figure(figsize=(10, 6))
    
    # Summary bar chart
    bar_plot = plt.barh(summary['Proxy'], summary['Discrepancy Rate'], color='skyblue')
    
    # Add percentage labels to the bars
    for i, v in enumerate(summary['Discrepancy Rate']):
        plt.text(v + 0.01, i, f"{v:.1%}", va='center')
    
    plt.title('Client/Server Test Pair Discrepancy Rates by Proxy', fontsize=14, fontweight='bold')
    plt.xlabel('Percentage of Test Pairs with Discrepancies', fontsize=12)
    plt.ylabel('Proxy', fontsize=12)
    plt.xlim(0, max(summary['Discrepancy Rate']) * 1.2)  # Add some space for labels
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
    # 1: Modified (Red)
    # 2: Unmodified (Yellow)
    # 3: Reset (Light Blue)
    # 4: Goaway (Orange)
    # 5: 500 Error (Purple)
    # 6: Not Considered (Black) - Added for client-only scope
    # 0: Dropped (Gray)
    colors = {
        1: '#ff6b6b',  # Modified (M)
        2: '#ffd93d',  # Unmodified (U)
        3: '#6bccee',  # Reset (R) - Light Blue
        4: '#ff9f43',  # Goaway (G) - Orange
        5: '#a26bcd',  # 500 Error (E) - Purple
        6: '#000000',  # Not Considered (N) - Black
        0: '#cccccc'   # Dropped/Received/Other (D) - Gray
    }
    outcome_map = {
        "modified": 1,
        "unmodified": 2,
        "reset": 3,
        "goaway": 4,
        "500": 5,
        "not_considered": 6, # Added mapping
        "dropped": 0,
        "received": 0, # Re-add mapping to Dropped/Gray
        "other": 0     # Re-add mapping to Dropped/Gray
    }

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
    else:
        # For full scope, derive IDs only from the filtered proxies' results
        test_ids_for_graph = sorted(
            list(set().union(*(outcomes_dict[proxy].keys() for proxy in filtered_proxies))),
            key=lambda x: int(x) if x.isdigit() else float('inf')
        )
        
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
            # Check if this test should be marked as "Not Considered" for client-only scope
            if scope_filter == 'client-only' and client_side_tests_set is not None and test_id not in client_side_tests_set:
                numerical_outcomes.append(outcome_map["not_considered"]) # Assign 6 (Black)
            else:
                # Otherwise, use the normal result mapping
                result_str = outcomes.get(test_id, "other") # Default to "other" if test missing for this proxy
                # Ensure default is 0 if result_str isn't explicitly mapped anymore
                numerical_outcomes.append(outcome_map.get(result_str, 0)) 

        matrix_data_numeric.append(numerical_outcomes)
        proxy_labels.append(proxy) # Use original proxy name

    matrix_data = np.array(matrix_data_numeric) # No transpose
    # num_tests_display, num_proxies_display = matrix_data.shape # Original order
    num_proxies_display = len(proxy_labels)
    num_tests_display = num_tests # Use num_tests determined earlier

    # --- Figure and Axes Creation ---
    # Revert figsize: height ~ proxies, width ~ tests
    fig_height = num_proxies_display * 0.4 + 1.5 # Adjust multiplier and base as needed
    fig_width = num_tests_display * 0.15 + 1 # Adjust multiplier and base as needed
    fig = plt.figure(figsize=(fig_width, fig_height))
    
    # Revert subplot grid: rows ~ proxies, cols ~ tests
    ax_matrix = plt.subplot2grid((num_proxies_display + 2, num_tests_display + 1), 
                               (0, 0), 
                               rowspan=num_proxies_display, 
                               colspan=num_tests_display)
                               
    # --- Plot Matrix Rectangles ---
    rect_height = 1.0 # Represents height for one proxy
    rect_width = 1.0  # Represents width for one test
    for i in range(num_proxies_display):  # Iterate over proxies (rows)
        for j in range(num_tests_display):  # Iterate over tests (columns)
            outcome = matrix_data[i][j]
            color = colors.get(outcome, colors[0])
            # Y position based on proxy index `i`
            y_pos = (num_proxies_display - 1 - i) * rect_height 
            # X position based on test index `j`
            x_pos = j * rect_width
            rect = plt.Rectangle((x_pos, y_pos), rect_width, rect_height, facecolor=color, edgecolor='white', linewidth=0.5)
            ax_matrix.add_patch(rect)
            
    # --- Axis and Grid Configuration ---
    # Revert limits
    ax_matrix.set_xlim(0, num_tests_display * rect_width)
    ax_matrix.set_ylim(0, num_proxies_display * rect_height)
    
    # Set major ticks for grid lines
    ax_matrix.set_xticks(np.arange(num_tests_display + 1) * rect_width)
    ax_matrix.set_yticks(np.arange(num_proxies_display + 1) * rect_height)
    
    # Set minor ticks and labels for X axis (Tests - every 5th)
    x_tick_positions = []
    x_tick_labels = []
    # Iterate using the correct test ID list for ticks
    for i, test_id in enumerate(test_ids_for_graph): 
        try:
            test_num = int(test_id)
            if test_num % 10 == 0:
                # Position centered horizontally in the test's column
                x_tick_positions.append(i * rect_width + rect_width / 2)
                x_tick_labels.append(test_id)
        except ValueError:
            pass
    ax_matrix.set_xticks(x_tick_positions, minor=True)
    ax_matrix.set_xticklabels(x_tick_labels, minor=True, rotation=0, ha='center', fontsize=10) # No rotation

    # Set minor ticks and labels for Y axis (Proxies)
    ax_matrix.set_yticks(np.arange(num_proxies_display) * rect_height + rect_height / 2, minor=True)
    ax_matrix.set_yticklabels(proxy_labels[::-1], minor=True, fontsize=10) # Increased size

    # Configure label appearance and grid
    ax_matrix.tick_params(axis='x', which='minor', labelsize=16, bottom=True, top=False, labelbottom=True) # Adjusted size
    ax_matrix.tick_params(axis='y', which='minor', labelsize=16, left=True, right=False, labelleft=True) # Adjusted size
    ax_matrix.set_xticklabels([], minor=False)
    ax_matrix.set_yticklabels([], minor=False)
    ax_matrix.tick_params(which='major', length=0)
    ax_matrix.grid(True, which='major', color='white', linewidth=1)
    ax_matrix.tick_params(which='minor', length=0)

    # Adjust layout and save
    plt.tight_layout(pad=1.0, rect=[0, 0.05, 1, 0.95]) # Adjusted pad and rect
    
    # Revert filename
    filename = f'proxy_outcome_matrix_{scope_filter}.png' 

    # --- Add Legend ---
    # Create reverse mapping from outcome number to name (optional, used for debugging)
    # reverse_outcome_map = {v: k for k, v in outcome_map.items()}
    
    # Map numerical value back to a display name
    outcome_display_names = {
        1: "Modified",
        2: "Unmodified",
        3: "Reset",
        4: "Goaway",
        5: "500 Error",
        6: "Not Considered",
        0: "Dropped/Other"
    }
    legend_patches = []
    ordered_keys = [1, 2, 3, 4, 5, 0, 6]
    for key in ordered_keys:
        if key in colors:
            display_name = outcome_display_names.get(key, f"Unknown ({key})")
            legend_patches.append(mpatches.Patch(color=colors[key], label=display_name))
    fig.legend(handles=legend_patches, loc='lower center', ncol=len(legend_patches), 
               bbox_to_anchor=(0.5, 0), frameon=False, fontsize=16)

    plt.savefig(os.path.join(charts_directory, filename), 
                dpi=300, bbox_inches='tight')

def main():
    # Create base directories if they don't exist
    base_dirs = {
        'analysis': ['tables', 'outliers', 'cloudflare', 'behavior', 'conformance', 'correlation'],
    }
    
    for base_dir, subdirs in base_dirs.items():
        for subdir in subdirs:
            os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)
    
    # List of proxy folders with their test scope
    proxy_configs = {
        'Nghttpx': {'scope': 'full'},
        'HAproxy': {'scope': 'full'},
        'Apache': {'scope': 'full'},
        'Caddy': {'scope': 'full'},
        'Node': {'scope': 'full'},
        'Envoy': {'scope': 'full'},
        'H2O': {'scope': 'full'},
        'Cloudflare': {'scope': 'full'},
        'Mitmproxy': {'scope': 'full'},
        'Traefik': {'scope': 'client-only'},
        'Azure-AG': {'scope': 'client-only'},
        'Nginx': {'scope': 'client-only'},
        'Lighttpd': {'scope': 'client-only'},
        'Fastly': {'scope': 'client-only'}
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

        dropped_count, error_500_count, goaway_count, reset_count, received_count, modified_count, unmodified_count, test_results, test_messages = analyze_results(latest_file)
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
    # Removed call to create_test_timeline_graphs here, moved after loading client/server tests

    # run cloudflare_analysis.py
    os.system('python cloudflare_analysis.py')
    
    # Load client-server classification and create client-server visualizations
    try:
        client_server_dir = os.path.join('analysis', 'behavior')
        client_side_tests, server_side_tests = load_client_server_classification('docs/clientside_vs_serverside.json')
        create_client_server_proxy_line_graphs(all_test_results, proxy_configs, client_side_tests, server_side_tests, client_server_dir)
        create_test_timeline_graphs(all_test_results, proxy_configs, client_side_tests, server_side_tests, client_server_dir)
        
        conformance_dir = os.path.join('analysis', 'conformance')
        # Generate conformance graphs for all, full, and client-only scopes
        create_client_server_conformance_visualization(all_test_results, client_side_tests, server_side_tests, proxy_configs, conformance_dir, scope_filter='all')
        create_client_server_conformance_visualization(all_test_results, client_side_tests, server_side_tests, proxy_configs, conformance_dir, scope_filter='full')
        create_client_server_conformance_visualization(all_test_results, client_side_tests, server_side_tests, proxy_configs, conformance_dir, scope_filter='client-only')
    except Exception as e:
        print(f"Error creating client-server visualizations: {e}")
    
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
    client_side_tests_set = None # Default to None
    try:
        # Load client-side test IDs needed for the matrix graph
        _, server_side_tests = load_client_server_classification('docs/clientside_vs_serverside.json')
        # Assuming load_client_server_classification returns (client_set, server_set)
        # We actually need the client set for this specific feature
        client_side_tests_set, _ = load_client_server_classification('docs/clientside_vs_serverside.json') 
    except Exception as e:
        print(f"Warning: Could not load client/server classification for matrix graph: {e}")
        
    if all_test_results:
        # Determine the global set of all test IDs encountered across all results
        global_all_test_ids = sorted(
            list(set().union(*(results.keys() for results in all_test_results.values()))),
            key=lambda x: int(x) if x.isdigit() else float('inf')
        )

        # Full scope graph (uses its own derived test IDs, pass None for global)
        create_proxy_matrix_graph(all_test_results, proxy_configs, 'full', behavior_dir, 
                                client_side_tests_set=None, global_test_ids=None)
        # Client-only scope graph (pass the client-side test set and the global ID list)
        create_proxy_matrix_graph(all_test_results, proxy_configs, 'client-only', behavior_dir, 
                                client_side_tests_set=client_side_tests_set, global_test_ids=global_all_test_ids)
    else:
        print("Skipping proxy matrix graph: No test results loaded.")

if __name__ == "__main__":
    main()