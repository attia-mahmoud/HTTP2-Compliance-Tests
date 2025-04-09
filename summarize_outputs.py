import json
import os
from datetime import datetime
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from collections import defaultdict

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
        filename = 'proxy_correlation_matrix_full.png' if scope == 'full' else 'proxy_correlation_matrix_client_only.png'
        plt.savefig(os.path.join(output_directory, filename), 
                    dpi=300, bbox_inches='tight')
        plt.close()

def create_proxy_vector_graph(test_results, proxy_configs, output_directory):
    """Create a vector visualization of proxy test results over time."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Split proxies by scope
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'full' and proxy in test_results]
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'client-only' and proxy in test_results]
    
    # Create separate vector graphs for each scope
    for scope, proxies in [('full', full_scope_proxies), ('client-only', client_only_proxies)]:
        if not proxies:  # Skip if no proxies in this category
            continue
            
        test_ids = sorted(list(set().union(*[results.keys() for proxy, results in test_results.items() 
                                           if proxy in proxies])),
                         key=lambda x: int(x) if x.isdigit() else float('inf'))
        
        fig, ax = plt.subplots(figsize=(20, len(proxies) * 2.5))
        
        # First, identify outliers and consistent tests
        outliers = {}
        consistent_tests = set()
        
        for test_id in test_ids:
            # Collect results for this test
            test_results_row = []
            for proxy in proxies:
                result = test_results[proxy].get(test_id, "other")
                # Convert to numeric values: 4 for received, 3 for reset, 2 for goaway, 1 for 500, 0 for dropped
                if result == "received":
                    test_results_row.append(4)
                elif result == "reset":
                    test_results_row.append(3)
                elif result == "goaway":
                    test_results_row.append(2)
                elif result == "500":
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
                result = test_results[proxy].get(test_id, "other")
                if result == "received":
                    y_val = 4
                    y_positions.append(y_val + i * 5)
                    x_positions.append(j)
                elif result == "reset":
                    y_val = 3
                    y_positions.append(y_val + i * 5)
                    x_positions.append(j)
                elif result == "goaway":
                    y_val = 2
                    y_positions.append(y_val + i * 5)
                    x_positions.append(j)
                elif result == "500":
                    y_val = 1
                    y_positions.append(y_val + i * 5)
                    x_positions.append(j)
                elif result == "dropped":
                    y_val = 0
                    y_positions.append(y_val + i * 5)
                    x_positions.append(j)
                else:  # other - don't plot a dot
                    y_val = None
                
                y_values.append(y_val)
                
                # Check if this point is an outlier and not "other"
                if y_val is not None and test_id in outliers and outliers[test_id] == proxy:
                    outlier_points_x.append(j)
                    outlier_points_y.append(y_val + i * 5)
            
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
        ax.set_ylim(-1, len(proxies) * 5 + 2)  # Expanded y-range to accommodate extra values
        
        # Set y-ticks and labels
        y_ticks = []
        y_labels = []
        for i in range(len(proxies)):
            y_ticks.extend([i * 5, i * 5 + 1, i * 5 + 2, i * 5 + 3, i * 5 + 4])
            y_labels.extend([
                f"{proxies[i]} (dropped)", 
                f"{proxies[i]} (500)", 
                f"{proxies[i]} (goaway)",
                f"{proxies[i]} (reset)",
                f"{proxies[i]} (received)"
            ])
        
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels, fontsize=9)
        
        # Add a legend explaining the values
        ax.text(0.01, 0.99, 'Values: 0=dropped, 1=500 error, 2=goaway, 3=reset, 4=received (dots not shown for "other" results)', 
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
        
        scope_title = 'Full Test Suite' if scope == 'full' else 'Client-side Tests Only'
        plt.title(f'Proxy Test Results Vector Graph ({scope_title})\n(* indicates outlier behavior, bold numbers indicate consistent behavior)', 
                  fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        filename = 'proxy_vector_graph_full.png' if scope == 'full' else 'proxy_vector_graph_client_only.png'
        plt.savefig(os.path.join(output_directory, filename), 
                    dpi=300, bbox_inches='tight')
        plt.close()

def create_proxy_result_pies(test_results, proxy_configs, output_directory):
    """Create pie charts showing dropped vs error vs reset vs goaway vs received vs other proportions for each proxy."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Split proxies by scope
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'full' and proxy in test_results]
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'client-only' and proxy in test_results]
    
    # Create separate figures for full scope and client-only proxies
    for scope, proxies in [('full', full_scope_proxies), ('client-only', client_only_proxies)]:
        if not proxies:  # Skip if no proxies in this category
            continue
            
        n_charts = len(proxies)
        n_cols = min(3, n_charts)
        n_rows = (n_charts + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        scope_title = 'Full Test Suite' if scope == 'full' else 'Client-side Tests Only'
        fig.suptitle(f'Result Distribution by Proxy ({scope_title})', fontsize=16, y=0.95)
        
        # Convert axes to a flat list for easier iteration
        if n_rows == 1 and n_cols == 1:
            axes = np.array([axes])
        elif n_rows == 1:
            axes = np.array([axes])
        axes_flat = axes.flatten()
        
        colors = ['#ff6b6b', '#ffd93d', '#ff9f43', '#6c5ce7', '#6bceff', '#4ecdc4', '#2ecc71', '#95a5a6']
        
        for i, proxy in enumerate(proxies):
            create_single_pie(axes_flat[i], test_results[proxy], colors, f"{proxy}")
        
        # Hide any unused subplots
        for j in range(n_charts, len(axes_flat)):
            axes_flat[j].set_visible(False)
        
        plt.tight_layout()
        filename = 'proxy_result_pies_full.png' if scope == 'full' else 'proxy_result_pies_client_only.png'
        plt.savefig(os.path.join(output_directory, filename), dpi=300, bbox_inches='tight')
        plt.close()

def create_proxy_line_graphs(test_results, proxy_configs, output_directory):
    """Create line graphs showing test result categories with different proxies as lines in CDF style."""
    os.makedirs(output_directory, exist_ok=True)
    
    # Split proxies by scope
    full_scope_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'full' and proxy in test_results]
    client_only_proxies = [proxy for proxy, config in proxy_configs.items() if config['scope'] == 'client-only' and proxy in test_results]
    
    # Define the categories in the order we want them on the x-axis
    categories = ['dropped', '500', 'goaway', 'reset', 'unmodified', 'modified']
    category_display_names = ['D', 'E', 'G', 'R', 'U', 'M']
    
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
        
        # Configure the plot
        plt.xticks(range(len(categories)), category_display_names, rotation=45)
        plt.xlim(-0.5, len(categories) - 0.5)
        plt.ylim(0, 110)  # Increased from 100 to 110 to provide more padding at the top
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Add test count annotation next to the 100% mark on the y-axis
        test_count = 165 if scope == 'full' else 83  # Hardcoded values as specified
        
        scope_title = 'HTTP/2 End-to-End' if scope == 'full' else 'HTTP/2 to HTTP/1.1'
        plt.title(f'HTTP/2 Test Result Distribution - {scope_title} ({test_count} tests)', fontsize=14, fontweight='bold')
        plt.ylabel('Cumulative Percentage (%)', fontsize=12)
        
        # Add legend with smaller font size
        plt.legend(loc='lower right', fontsize=10)
        
        plt.tight_layout()
        
        # Save the figure
        filename = 'proxy_result_cdf_full.png' if scope == 'full' else 'proxy_result_cdf_client_only.png'
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

def create_result_counts_table(dropped_counts, error_500_counts, goaway_counts, reset_counts, received_counts, all_test_results, proxy_configs, summaries_dir):
    """Create a markdown table summarizing the counts of dropped, error, reset, goaway, and received results."""
    if not os.path.exists(summaries_dir):
        os.makedirs(summaries_dir)
    
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
    with open(os.path.join(summaries_dir, "result_counts.txt"), "w") as f:
        f.write(table)

def create_test_results_matrix(all_test_results, proxy_configs, summaries_dir):
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
    
    with open(os.path.join(summaries_dir, 'test_results_matrix.md'), 'w') as f:
        f.write(matrix_table)

def extract_and_save_outliers(all_test_results, proxy_configs, summaries_dir):
    """
    Extract outliers from test results and save them to dedicated files based on test scope.
    
    Outliers are defined as tests where exactly one proxy behaves differently from all others
    that have the same scope (full or client-only).
    
    Args:
        all_test_results: Dictionary mapping proxy names to their test results
        proxy_configs: Dictionary mapping proxy names to their configurations
        summaries_dir: Directory to save the output report
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
        output_file = os.path.join(summaries_dir, filename)
        
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
    write_outliers_file(full_scope_outliers, "outlier_behaviors_full.md", "Full")
    write_outliers_file(client_only_outliers, "outlier_behaviors_client_only.md", "Client-Only")
    
    return full_scope_outliers, client_only_outliers

def load_client_server_classification(json_path):
    """Load the classification of tests as client-side or server-side."""
    with open(json_path, 'r') as f:
        classification = json.load(f)
    
    # Convert frame numbers to strings to match test IDs
    client_side_tests = set(str(frame) for frame in classification['client_side_non_conformant_frames'])
    server_side_tests = set(str(frame) for frame in classification['server_side_non_conformant_frames'])
    
    return client_side_tests, server_side_tests

def create_client_server_pie_charts(test_results, client_side_tests, server_side_tests, proxy_configs, output_directory):
    """
    Create pie charts showing dropped vs 500 error vs goaway vs reset vs received vs other proportions for each proxy,
    separated into client-side and server-side tests.
    """
    os.makedirs(output_directory, exist_ok=True)
    
    proxies = list(test_results.keys())
    n_charts = len(proxies) * 2  # Two charts per proxy (client and server)
    n_cols = 2  # Client and server side by side
    n_rows = len(proxies)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 5*n_rows))
    fig.suptitle('Client vs Server Test Result Distribution by Proxy', fontsize=16, y=0.95)
    
    colors = ['#ff6b6b', '#ffd93d', '#ff9f43', '#6c5ce7', '#6bceff', '#4ecdc4', '#2ecc71', '#95a5a6']  # Red for dropped, Yellow for 500, Orange for goaway, Purple for reset, Blue for received, Teal for modified, Green for unmodified, Gray for other
    
    # Handle the case where there's only one proxy
    if n_rows == 1:
        axes = np.array([axes])  # Convert to 2D array with shape (1, 2)
    
    for i, proxy in enumerate(proxies):
        proxy_results = test_results[proxy]
        
        # Process client-side tests
        client_tests = {test_id: result for test_id, result in proxy_results.items() 
                       if test_id in client_side_tests}
        
        # Process server-side tests
        server_tests = {test_id: result for test_id, result in proxy_results.items() 
                       if test_id in server_side_tests}
        
        # Create pie chart for client-side tests
        create_single_pie(axes[i, 0], client_tests, colors, f"{proxy} - Client Side")
        
        # Create pie chart for server-side tests
        create_single_pie(axes[i, 1], server_tests, colors, f"{proxy} - Server Side")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'client_server_pies.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_client_server_discrepancy_visualization(test_results, test_pairs, output_directory):
    """
    Create visualizations showing discrepancies between client and server test pairs.
    
    Args:
        test_results: Dict mapping proxy names to their test results
        test_pairs: List of [client_test, server_test] pairs
        output_directory: Directory to save the visualization
    """
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

def create_client_server_conformance_visualization(test_results, client_side_tests, server_side_tests, proxy_configs, output_directory):
    """
    Create visualizations showing how well each proxy conforms to client-side and server-side tests separately.
    """
    os.makedirs(output_directory, exist_ok=True)
    
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
    proxies = list(test_results.keys())
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
    plt.title('HTTP/2 Client-Side vs Server-Side Non-Conformance by Proxy', pad=20)
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
    
    # Save the plot
    plt.savefig(os.path.join(output_directory, 'client_server_non_conformance.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def load_test_pairs(pairs_file='docs/pairs.json'):
    """Load the test pairs from the JSON file."""
    with open(pairs_file, 'r') as f:
        data = json.load(f)
    return data['pairs']

def create_test_outcome_by_id_table(all_test_results, summaries_dir):
    """Create a text file listing proxies that had modified, unmodified, or received results for each test ID."""
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
    output_file = os.path.join(summaries_dir, "test_outcomes_by_id.txt")
    
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

def compare_cloudflare_variants(all_test_results, summaries_dir):
    """
    Compare test results between Cloudflare, Cloudflare2, and Cloudflare3 and identify differences.
    
    Args:
        all_test_results: Dictionary mapping proxy names to their test results
        summaries_dir: Directory to save the output report
    """
    # Check if all Cloudflare variants are present
    cf_variants = ["Cloudflare", "Cloudflare2", "Cloudflare3", "Cloudflare4"]
    for variant in cf_variants:
        if variant not in all_test_results:
            print(f"Warning: {variant} results not found in the dataset")
    
    # Filter available Cloudflare variants
    available_variants = [v for v in cf_variants if v in all_test_results]
    if len(available_variants) < 2:
        print("Not enough Cloudflare variants to compare")
        return
    
    # Get the common test IDs across available variants
    common_test_ids = set()
    for variant in available_variants:
        if common_test_ids:
            common_test_ids &= set(all_test_results[variant].keys())
        else:
            common_test_ids = set(all_test_results[variant].keys())
    
    # Find tests with different outcomes
    different_outcomes = {}
    for test_id in common_test_ids:
        # Collect results for this test across variants
        test_results = {variant: all_test_results[variant][test_id] for variant in available_variants}
        
        # Check if there are differences
        if len(set(test_results.values())) > 1:
            different_outcomes[test_id] = test_results
    
    # Load test descriptions
    try:
        with open('test_cases.json', 'r') as f:
            test_cases = json.load(f)
        test_descriptions = {str(case['id']): case['description'] for case in test_cases}
    except:
        print("Warning: Could not load test descriptions from test_cases.json")
        test_descriptions = {}
    
    # Create the output file
    output_file = os.path.join(summaries_dir, "cloudflare_variant_differences.txt")
    
    with open(output_file, 'w') as f:
        f.write("# Differences Between Cloudflare Variants\n\n")
        f.write(f"Comparing {', '.join(available_variants)}\n\n")
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
            
            for variant in available_variants:
                f.write(f"| {variant} | {results[variant]} |\n")
            
            f.write("\n")

    return different_outcomes

def create_cloudflare_correlation_matrix(all_test_results, output_directory):
    """
    Create a Pearson correlation matrix visualization specifically for Cloudflare variants.
    
    Args:
        all_test_results: Dictionary mapping proxy names to their test results
        output_directory: Directory to save the visualization
    """
    os.makedirs(output_directory, exist_ok=True)
    
    # Filter for Cloudflare variants
    cf_variants = ["Cloudflare", "Cloudflare2", "Cloudflare3", "Cloudflare4"]
    available_variants = [v for v in cf_variants if v in all_test_results]
    
    if len(available_variants) < 2:
        print("Not enough Cloudflare variants to create correlation matrix")
        return
    
    # Get test IDs from all available variants
    test_ids = sorted(list(set().union(*[results.keys() for proxy, results in all_test_results.items() 
                                       if proxy in available_variants])),
                     key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    # Create matrix data with the same encoding as the original function
    matrix_data = np.zeros((len(available_variants), len(test_ids)))
    for i, proxy in enumerate(available_variants):
        for j, test_id in enumerate(test_ids):
            # Convert result to numeric value with better separation
            result = all_test_results[proxy].get(test_id, "other")
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
    correlation_matrix = np.zeros((len(available_variants), len(available_variants)))
    for i in range(len(available_variants)):
        for j in range(len(available_variants)):
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
    plt.xticks(np.arange(len(available_variants)), available_variants, rotation=45, ha='right')
    plt.yticks(np.arange(len(available_variants)), available_variants)
    
    # Add correlation values as text
    for i in range(len(available_variants)):
        for j in range(len(available_variants)):
            text = plt.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                          ha='center', va='center', color='black')
            
            # Make text white for dark background
            if abs(correlation_matrix[i, j]) > 0.5:
                text.set_color('white')
    
    plt.title('Cloudflare Variants Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save the plot
    filename = 'cloudflare_correlation_matrix.png'
    plt.savefig(os.path.join(output_directory, filename), 
                dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Create summaries directory if it doesn't exist
    summaries_dir = 'summaries'
    if not os.path.exists(summaries_dir):
        os.makedirs(summaries_dir)
    
    # List of proxy folders with their test scope
    proxy_configs = {
        'Nghttpx': {'scope': 'full'},
        'HAproxy': {'scope': 'full'},
        'Apache': {'scope': 'full'},
        # 'ApacheTest': {'scope': 'full'},
        'Caddy': {'scope': 'full'},
        'Node': {'scope': 'full'},
        'Envoy': {'scope': 'full'},
        'H2O': {'scope': 'full'},
        'Cloudflare': {'scope': 'full'},
        # 'Cloudflare2': {'scope': 'full'},
        # 'Cloudflare3': {'scope': 'full'},
        # 'Cloudflare4': {'scope': 'full'},
        'Mitmproxy': {'scope': 'full'},
        'Azure-AG': {'scope': 'client-only'},
        'Nginx': {'scope': 'client-only'},
        'Lighttpd': {'scope': 'client-only'}
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
    create_result_counts_table(dropped_counts, error_500_counts, goaway_counts, reset_counts, received_counts, all_test_results, proxy_configs, summaries_dir)
    create_test_results_matrix(all_test_results, proxy_configs, summaries_dir)
    
    # Extract and save outliers
    extract_and_save_outliers(all_test_results, proxy_configs, summaries_dir)

    # Create visualizations
    output_dir = 'visualizations'
    create_proxy_correlation_matrix(all_test_results, proxy_configs, output_dir)
    create_proxy_vector_graph(all_test_results, proxy_configs, output_dir)
    create_proxy_result_pies(all_test_results, proxy_configs, output_dir)
    create_proxy_line_graphs(all_test_results, proxy_configs, output_dir)

    # Compare Cloudflare variants
    compare_cloudflare_variants(all_test_results, summaries_dir)
    
    # Create Cloudflare correlation matrix
    create_cloudflare_correlation_matrix(all_test_results, output_dir)
    
    # Load client-server classification and create client-server visualizations
    try:
        client_side_tests, server_side_tests = load_client_server_classification('docs/clientside_vs_serverside.json')
        create_client_server_pie_charts(all_test_results, client_side_tests, server_side_tests, proxy_configs, output_dir)
        create_client_server_conformance_visualization(all_test_results, client_side_tests, server_side_tests, proxy_configs, output_dir)
    except Exception as e:
        print(f"Error creating client-server visualizations: {e}")
    
    # Create client-server discrepancy visualization (only for full-scope proxies)
    try:
        test_pairs = load_test_pairs()
        full_scope_results = {proxy: results for proxy, results in all_test_results.items() 
                            if proxy_configs[proxy]['scope'] == 'full'}
        create_client_server_discrepancy_visualization(full_scope_results, test_pairs, output_dir)
    except Exception as e:
        print(f"Error creating client-server discrepancy visualization: {e}")
    
    # Create test outcomes by ID table
    create_test_outcome_by_id_table(all_test_results, summaries_dir)

if __name__ == "__main__":
    main()