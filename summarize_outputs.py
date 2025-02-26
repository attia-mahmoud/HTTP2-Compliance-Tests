import json
import os
from datetime import datetime
import glob
import matplotlib.pyplot as plt
import numpy as np

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
    
    dropped_count = 0
    error_count = 0
    received_count = 0
    test_results = {}
    test_messages = {}
    
    for test_id, test_data in data.items():
        if not test_data or not test_data.get('result'):
            test_results[test_id] = "other"
            test_messages[test_id] = "No result data"
            continue
        
        result = test_data['result']
        is_dropped = False
        is_error = False
        is_received = False
        message = ""
        
        if isinstance(result, str):
            # skip this test
            continue
        
        # Use safer access methods for worker data
        worker1 = result.get('Worker_1', {}) or {}
        worker2 = result.get('Worker_2', {}) or {}
        
        vars1 = worker1.get('Variables', {}) or {}
        vars2 = worker2.get('Variables', {}) or {}
        
        if vars1.get('client_result', '').startswith("Successfully received all") and \
            vars1.get('server_result', '').startswith("Successfully received all"):
            is_received = True
            message = vars1['client_result']
            
        if vars2.get('client_result', '').startswith("Successfully received all") and \
            vars2.get('server_result', '').startswith("Successfully received all"):
            is_received = True
            message = vars2['client_result']

        elif vars1.get('msg', '').startswith("No response received for test request"):
            is_dropped = True
            message = vars1['msg']
    
        elif vars1.get('client_result', '').startswith("Received 5xx status code"):
            is_error = True
            message = vars1['client_result']
        
        elif vars2.get('server_result', '').startswith("Received 5xx status code"):
            is_error = True
            message = vars2['server_result']

        elif "reset after receiving" in vars1.get('client_result', ''):
            is_error = True
            message = vars1['client_result']
        
        elif "reset after receiving" in vars2.get('server_result', ''):
            is_error = True
            message = vars2['server_result']

        elif vars2.get('msg', '').startswith("Connection established but client negotiated"):
            is_dropped = True
            message = vars2['msg']

        elif vars1.get('msg', '').startswith("Connection terminated by peer"):
            is_error = True
            message = vars1['msg']

        elif vars2.get('msg', '').startswith("Connection terminated by peer"):
            is_error = True
            message = vars2['msg']
            
        elif vars1.get('msg', '') == "Timeout after 5s while waiting for peer's preface (SETTINGS frame)":
            is_dropped = True
            message = vars1['msg']

        elif vars1.get('msg', '') == "Expected SETTINGS frame for preface but received error instead":
            is_error = True
            message = vars1['msg']

        elif vars2.get('msg', '').startswith("Timeout occurred after 5s while waiting for client connection"):
            is_dropped = True
            message = vars2['msg']

        elif worker1 and worker1.get('State', '') in ['CONTROL_CHANNEL_TIMEOUT_CLIENT_FRAMES_SENT_CLIENT', 'CONTROL_CHANNEL_TIMEOUT_SERVER_FRAMES_SENT_CLIENT']:
            is_dropped = True
            message = vars1['result']

        elif worker2 and worker2.get('State', '') in ['CONTROL_CHANNEL_TIMEOUT_CLIENT_FRAMES_SENT_SERVER', 'CONTROL_CHANNEL_TIMEOUT_SERVER_FRAMES_SENT_SERVER']:
            is_dropped = True
            message = vars2['result']

        # Store results
        if is_dropped:
            test_results[test_id] = "dropped"
            dropped_count += 1
        elif is_error:
            test_results[test_id] = "error"
            error_count += 1
        elif is_received:
            test_results[test_id] = "received"
            received_count += 1
        else:
            test_results[test_id] = "other"
        
        test_messages[test_id] = message
    
    return dropped_count, error_count, received_count, test_results, test_messages

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

def create_proxy_correlation_matrix(test_results, output_directory):
    """Create a Pearson correlation matrix visualization of proxy test results."""
    os.makedirs(output_directory, exist_ok=True)
    
    test_ids = sorted(list(set().union(*[results.keys() for results in test_results.values()])),
                     key=lambda x: int(x) if x.isdigit() else float('inf'))
    proxies = list(test_results.keys())
    
    # Create matrix data with better encoding
    matrix_data = np.zeros((len(proxies), len(test_ids)))
    for i, proxy in enumerate(proxies):
        for j, test_id in enumerate(test_ids):
            # Convert result to numeric value with better separation
            result = test_results[proxy].get(test_id, "other")
            if result == "received":
                matrix_data[i][j] = 2  # Success
            elif result == "error":
                matrix_data[i][j] = 1  # Partial success
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
    
    plt.title('Proxy Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(output_directory, 'proxy_correlation_matrix.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_proxy_vector_graph(test_results, output_directory):
    """Create a vector visualization of proxy test results over time."""
    os.makedirs(output_directory, exist_ok=True)
    
    test_ids = sorted(list(set().union(*[results.keys() for results in test_results.values()])),
                     key=lambda x: int(x) if x.isdigit() else float('inf'))
    proxies = list(test_results.keys())
    
    fig, ax = plt.subplots(figsize=(20, len(proxies) * 1.5))
    
    # First, identify outliers and consistent tests
    outliers = {}
    consistent_tests = set()
    
    for test_id in test_ids:
        # Collect results for this test
        test_results_row = []
        for proxy in proxies:
            result = test_results[proxy].get(test_id, "other")
            # Convert to numeric values: 2 for received, 1 for error, 0 for dropped
            if result == "received":
                test_results_row.append(2)
            elif result == "error":
                test_results_row.append(1)
            elif result == "dropped":
                test_results_row.append(0)
            else:  # other - we'll handle these separately
                test_results_row.append(None)
        
        # Check consistency - only consider non-None values
        non_none_results = [r for r in test_results_row if r is not None]
        if non_none_results and len(set(non_none_results)) == 1:  # All proxies behaved the same way
            consistent_tests.add(test_id)
        
        # Check if there's an outlier (exactly one different from others)
        values = [r for r in test_results_row if r is not None]
        if values:
            value_set = set(values)
            if len(value_set) == 2:
                counts = [values.count(v) for v in value_set]
                if 1 in counts:  # If exactly one value is different
                    outlier_value = list(value_set)[counts.index(1)]
                    # Find the index of the outlier in the original list with Nones
                    for idx, val in enumerate(test_results_row):
                        if val == outlier_value and values.count(outlier_value) == 1:
                            outliers[test_id] = proxies[idx]
                            break
    
    # Plot vectors for each proxy
    for i, proxy in enumerate(proxies):
        y_values = []
        y_positions = []
        x_positions = []
        outlier_points_x = []
        outlier_points_y = []
        
        for j, test_id in enumerate(test_ids, 1):
            result = test_results[proxy].get(str(test_id), "other")
            if result == "received":
                y_val = 2
                y_positions.append(y_val + i * 3)
                x_positions.append(j)
            elif result == "error":
                y_val = 1
                y_positions.append(y_val + i * 3)
                x_positions.append(j)
            elif result == "dropped":
                y_val = 0
                y_positions.append(y_val + i * 3)
                x_positions.append(j)
            else:  # other - don't plot a dot
                y_val = None
            
            y_values.append(y_val)
            
            # Check if this point is an outlier and not "other"
            if y_val is not None and str(test_id) in outliers and outliers[str(test_id)] == proxy:
                outlier_points_x.append(j)
                outlier_points_y.append(y_val + i * 3)
        
        # Plot only the dots for non-other values (no connecting lines)
        ax.scatter(x_positions, y_positions, marker='o', s=40, 
                label=proxy, zorder=3)
        
        # Highlight outlier points
        if outlier_points_x:
            ax.scatter(outlier_points_x, outlier_points_y, 
                      color='red', s=100, zorder=5, 
                      marker='*', label=f'{proxy} outliers')
    
    # Configure axis and labels
    ax.set_xlim(0, len(test_ids) + 1)
    ax.set_ylim(-1, len(proxies) * 3 + 2)  # Expanded y-range to accommodate extra value
    
    # Set y-ticks and labels
    y_ticks = []
    y_labels = []
    for i in range(len(proxies)):
        y_ticks.extend([i * 3, i * 3 + 1, i * 3 + 2])
        y_labels.extend([f"{proxies[i]} (dropped)", f"{proxies[i]} (error)", f"{proxies[i]} (received)"])
    
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=9)
    
    # Add a legend explaining the values
    ax.text(0.01, 0.99, 'Values: 0=dropped, 1=error, 2=received (dots not shown for "other" results)', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Configure x-axis with highlighted consistent tests
    ax.set_xlabel('Test ID', fontsize=12)
    ax.set_xticks(range(1, len(test_ids) + 1))
    
    # Create tick labels with different styles for consistent vs inconsistent tests
    x_labels = []
    for test_id in test_ids:
        if test_id in consistent_tests:
            # Bold and different color for consistent tests
            x_labels.append(f'$\\bf{{{test_id}}}$')  # Bold using LaTeX
        else:
            x_labels.append(str(test_id))
    
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    
    # Color the consistent test labels
    for tick in ax.get_xticklabels():
        if tick.get_text().startswith('$\\bf'):  # If it's a consistent test
            tick.set_color('darkblue')
            tick.set_fontsize(8)  # Slightly larger font
        else:
            tick.set_fontsize(8)
    
    # Add grid
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    plt.title('Proxy Test Results Vector Graph\n(* indicates outlier behavior, bold numbers indicate consistent behavior)', 
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_directory, 'proxy_vector_graph.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_proxy_result_pies(test_results, output_directory):
    """Create pie charts showing dropped vs error vs received vs other proportions for each proxy."""
    os.makedirs(output_directory, exist_ok=True)
    
    proxies = list(test_results.keys())
    n_charts = len(proxies)
    n_cols = 3
    n_rows = (n_charts + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    fig.suptitle('Result Distribution by Proxy', fontsize=16, y=0.95)
    
    if n_rows > 1:
        axes = axes.flatten()
    
    colors = ['#ff6b6b', '#ffd93d', '#6bceff', '#4ecdc4']  # Red for dropped, Yellow for errors, Blue for received, Green for other
    
    for i, proxy in enumerate(proxies):
        # Count categories
        total_tests = len(test_results[proxy])
        dropped = sum(1 for result in test_results[proxy].values() if result == "dropped")
        errors = sum(1 for result in test_results[proxy].values() if result == "error")
        received = sum(1 for result in test_results[proxy].values() if result == "received")
        other = total_tests - dropped - errors - received
        
        # Calculate percentages
        dropped_pct = (dropped / total_tests) * 100
        error_pct = (errors / total_tests) * 100
        received_pct = (received / total_tests) * 100
        other_pct = (other / total_tests) * 100
        
        sizes = [dropped_pct, error_pct, received_pct, other_pct]
        labels = [f'Dropped\n{dropped} ({dropped_pct:.1f}%)', 
                 f'Error\n{errors} ({error_pct:.1f}%)',
                 f'Received\n{received} ({received_pct:.1f}%)',
                 f'Other\n{other} ({other_pct:.1f}%)']
        
        if n_rows == 1:
            ax = axes[i] if n_charts > 1 else axes
        else:
            ax = axes[i]
            
        ax.pie(sizes, labels=labels, colors=colors, autopct='', 
               startangle=90)
        ax.set_title(proxy, pad=20)
    
    if n_charts < len(axes):
        for j in range(n_charts, len(axes)):
            if n_rows == 1:
                axes[j].remove() if n_charts > 1 else None
            else:
                axes[j].remove()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'proxy_result_pies.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_result_counts_table(dropped_counts, error_counts, received_counts, summaries_dir):
    """Create a table with dropped, error, and received counts for each proxy."""
    combined_data = []
    for proxy in sorted(dropped_counts.keys()):
        combined_data.append([
            proxy, 
            dropped_counts.get(proxy, 0),
            error_counts.get(proxy, 0),
            received_counts.get(proxy, 0)
        ])
    
    combined_table = create_markdown_table(
        ['Proxy', 'Dropped Count', 'Error Count', 'Received Count'], 
        combined_data
    )
    
    with open(os.path.join(summaries_dir, 'result_counts.md'), 'w') as f:
        f.write(combined_table)

def create_test_results_matrix(all_test_results, proxy_folders, summaries_dir):
    """Create a matrix showing test results for each proxy and test ID."""
    all_test_ids = sorted(set().union(*[test_results.keys() for test_results in all_test_results.values()]),
                         key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    matrix_headers = ['Test ID'] + proxy_folders
    matrix_data = []
    outlier_counts = {proxy: 0 for proxy in proxy_folders}  # Track outliers for each proxy
    
    for test_id in all_test_ids:
        row = [test_id]
        # First collect all results for this test
        test_row = []
        for proxy in proxy_folders:
            if proxy in all_test_results:
                result = all_test_results[proxy].get(test_id, "")
                if result == "received":
                    test_row.append("✓R")
                elif result == "dropped":
                    test_row.append("✓D")
                elif result == "error":
                    test_row.append("✓E")
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
                    outlier_counts[proxy_folders[idx]] += 1
        
        row.extend(test_row)
        matrix_data.append(row)
    
    # Add empty row for spacing
    matrix_data.append([''] * (len(proxy_folders) + 1))
    
    # Add outlier count row
    outlier_row = ['Outlier Count']
    outlier_row.extend(str(outlier_counts[proxy]) for proxy in proxy_folders)
    matrix_data.append(outlier_row)
    
    matrix_table = create_markdown_table(matrix_headers, matrix_data)
    
    with open(os.path.join(summaries_dir, 'test_results_matrix.md'), 'w') as f:
        f.write(matrix_table)

def main():
    # Create summaries directory if it doesn't exist
    summaries_dir = 'summaries'
    if not os.path.exists(summaries_dir):
        os.makedirs(summaries_dir)
    
    # List of proxy folders
    proxy_folders = ['Envoy', 'Node', 'Nghttpx', 'HAproxy', 'Apache', 'H2O', 'Caddy', 'Cloudflare']
    results_dir = 'results'
    
    # Prepare data for summary tables
    dropped_counts = {}
    error_counts = {}
    received_counts = {}
    all_test_results = {}
    all_test_messages = {}
    
    for proxy in proxy_folders:
        proxy_dir = os.path.join(results_dir, proxy)
        if not os.path.exists(proxy_dir):
            continue
            
        latest_file = get_latest_file(proxy_dir)
        if not latest_file:
            continue

        dropped_count, error_count, received_count, test_results, test_messages = analyze_results(latest_file)
        dropped_counts[proxy] = dropped_count
        error_counts[proxy] = error_count
        received_counts[proxy] = received_count
        all_test_results[proxy] = test_results
        all_test_messages[proxy] = test_messages

    # Create tables
    create_result_counts_table(dropped_counts, error_counts, received_counts, summaries_dir)
    create_test_results_matrix(all_test_results, proxy_folders, summaries_dir)

    # Create visualizations
    output_dir = 'visualizations'
    create_proxy_correlation_matrix(all_test_results, output_dir)
    create_proxy_vector_graph(all_test_results, output_dir)
    create_proxy_result_pies(all_test_results, output_dir)

if __name__ == "__main__":
    main()