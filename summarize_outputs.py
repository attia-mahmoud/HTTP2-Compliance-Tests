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
    """Analyze a single result file and return all Worker_2 messages."""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    timeout_count = 0
    test_results = {}
    test_messages = {}
    
    target_messages = [
        "Timeout occurred while waiting for client connection. Proxy dropped client's frames.",  # Worker_2
        "Proxy returned an error"  # Worker_1
    ]
    
    for test_id, test_data in data.items():
        # Check Worker_2 result
        worker_2 = test_data.get('result', {}).get('Worker_2', {})
        worker_1 = test_data.get('result', {}).get('Worker_1', {})
        
        message = ""
        
        # Check Worker_2 first
        if isinstance(worker_2, dict):
            variables = worker_2.get('Variables', {})
            message = variables.get('msg', '')
        
        # If no matching message from Worker_2, check Worker_1
        if message not in target_messages and isinstance(worker_1, dict):
            message = worker_1.get('Variables', {}).get('msg', '')
        
        # Record if either target message was found
        if message in target_messages:
            timeout_count += 1
            test_results[test_id] = True
        else:
            test_results[test_id] = False
        
        test_messages[test_id] = message
            
    return timeout_count, test_results, test_messages

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
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Get all test IDs and proxies
    test_ids = sorted(list(set().union(*[results.keys() for results in test_results.values()])),
                     key=lambda x: int(x) if x.isdigit() else float('inf'))
    proxies = list(test_results.keys())
    
    # Create matrix data
    matrix_data = np.zeros((len(proxies), len(test_ids)))
    for i, proxy in enumerate(proxies):
        for j, test_id in enumerate(test_ids):
            # Convert boolean results to numeric values (True = 1, False = 0)
            matrix_data[i][j] = 1 if test_results[proxy].get(test_id, False) else 0
    
    # Calculate correlation matrix
    correlation_matrix = np.corrcoef(matrix_data)
    
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
            result = '✓' if proxy in test_results and test_results[proxy].get(test_id, False) else ''
            test_results_row.append(result)
        
        # Check consistency
        unique_results = set(test_results_row)
        if len(unique_results) == 1:  # All proxies behaved the same way
            consistent_tests.add(test_id)
        
        # Check if there's an outlier
        check_count = test_results_row.count('✓')
        empty_count = test_results_row.count('')
        
        # If exactly one different from the others
        if (check_count == 1 and empty_count == len(proxies) - 1) or \
           (check_count == len(proxies) - 1 and empty_count == 1):
            # Find the outlier proxy
            for i, result in enumerate(test_results_row):
                if (check_count == 1 and result == '✓') or (empty_count == 1 and result == ''):
                    outliers[test_id] = proxies[i]
    
    # Plot vectors for each proxy
    for i, proxy in enumerate(proxies):
        y_values = []
        outlier_points_x = []
        outlier_points_y = []
        x_values = range(1, len(test_ids) + 1)
        
        for j, test_id in enumerate(test_ids, 1):
            y_val = 1 if test_results[proxy].get(str(test_id), False) else 0
            y_values.append(y_val)
            
            # Check if this point is an outlier
            if str(test_id) in outliers and outliers[str(test_id)] == proxy:
                outlier_points_x.append(j)
                outlier_points_y.append(y_val + i * 3)
        
        # Plot the main line with dots
        ax.plot(x_values, [y + i * 3 for y in y_values], '-o', 
                linewidth=2, markersize=4, label=proxy)
        
        # Highlight outlier points
        if outlier_points_x:
            ax.scatter(outlier_points_x, outlier_points_y, 
                      color='red', s=100, zorder=5, 
                      marker='*', label=f'{proxy} outliers')
    
    # Configure axis and labels
    ax.set_xlim(0, len(test_ids) + 1)
    ax.set_ylim(-1, len(proxies) * 3 + 1)
    
    # Set y-ticks and labels
    y_ticks = []
    y_labels = []
    for i in range(len(proxies)):
        y_ticks.extend([i * 3, i * 3 + 1])
        y_labels.extend([proxies[i], ''])
    
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=12)
    
    # Configure x-axis with highlighted consistent tests
    ax.set_xlabel('Test ID', fontsize=12)
    ax.set_xticks(x_values)
    
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

def create_proxy_timeout_pies(test_results, output_directory):
    """Create pie charts showing timeout vs no-timeout proportions for each proxy."""
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Get proxies
    proxies = list(test_results.keys())
    
    # Calculate number of rows and columns for subplot grid
    n_charts = len(proxies)
    n_cols = 3  # You can adjust this number to change the layout
    n_rows = (n_charts + n_cols - 1) // n_cols
    
    # Create figure
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    fig.suptitle('Timeout vs No-Timeout Distribution by Proxy', fontsize=16, y=0.95)
    
    # Flatten axes array for easier iteration
    if n_rows > 1:
        axes = axes.flatten()
    
    # Colors for the pie charts
    colors = ['#ff6b6b', '#4ecdc4']  # Red for timeouts, Green for no timeouts
    
    # Create pie chart for each proxy
    for i, proxy in enumerate(proxies):
        # Count timeouts and no timeouts
        total_tests = len(test_results[proxy])
        timeouts = sum(1 for result in test_results[proxy].values() if result)
        no_timeouts = total_tests - timeouts
        
        # Calculate percentages
        timeout_pct = (timeouts / total_tests) * 100
        no_timeout_pct = (no_timeouts / total_tests) * 100
        
        # Data for pie chart
        sizes = [timeout_pct, no_timeout_pct]
        labels = [f'Timeout\n{timeouts} ({timeout_pct:.1f}%)', 
                 f'No Timeout\n{no_timeouts} ({no_timeout_pct:.1f}%)']
        
        # Create pie chart
        if n_rows == 1:
            ax = axes[i] if n_charts > 1 else axes
        else:
            ax = axes[i]
            
        ax.pie(sizes, labels=labels, colors=colors, autopct='', 
               startangle=90)
        ax.set_title(proxy, pad=20)
    
    # Remove empty subplots if any
    if n_charts < len(axes):
        for j in range(n_charts, len(axes)):
            if n_rows == 1:
                axes[j].remove() if n_charts > 1 else None
            else:
                axes[j].remove()
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(output_directory, 'proxy_timeout_pies.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Create summaries directory if it doesn't exist
    summaries_dir = 'summaries'
    if not os.path.exists(summaries_dir):
        os.makedirs(summaries_dir)
    
    # List of proxy folders
    proxy_folders = ['Envoy', 'Node', 'Nghttpx', 'HAproxy', 'Apache', 'H2O']
    results_dir = 'results'
    
    # Prepare data for summary tables
    timeout_counts = {}
    all_test_results = {}
    all_test_messages = {}
    
    for proxy in proxy_folders:
        proxy_dir = os.path.join(results_dir, proxy)
        if not os.path.exists(proxy_dir):
            continue
            
        latest_file = get_latest_file(proxy_dir)
        if not latest_file:
            continue

        count, test_results, test_messages = analyze_results(latest_file)
        timeout_counts[proxy] = count
        all_test_results[proxy] = test_results
        all_test_messages[proxy] = test_messages

    # Generate first table - timeout counts
    count_data = [[proxy, count] for proxy, count in timeout_counts.items()]
    count_table = create_markdown_table(['Proxy', 'Timeout Count'], count_data)
    
    with open(os.path.join(summaries_dir, 'timeout_counts.md'), 'w') as f:
        f.write(count_table)
    
    # Generate second table - detailed test results matrix
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
            result = '✓' if proxy in all_test_results and all_test_results[proxy].get(test_id, False) else ''
            test_row.append(result)
        
        # Check if there's an outlier
        check_count = test_row.count('✓')
        empty_count = test_row.count('')
        
        # If exactly one different from the others (either one ✓ among empty or one empty among ✓)
        if (check_count == 1 and empty_count == len(proxy_folders) - 1) or \
           (check_count == len(proxy_folders) - 1 and empty_count == 1):
            # Find the outlier and make it bold
            for i, result in enumerate(test_row):
                if (check_count == 1 and result == '✓') or (empty_count == 1 and result == ''):
                    test_row[i] = f'**{result}**' if result else '**-**'
                    outlier_counts[proxy_folders[i]] += 1  # Increment outlier count
        
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
    
    # Generate third table - behavior consistency analysis
    consistency_data = []
    consistent_count = 0
    consistent_timeout_count = 0
    consistent_no_timeout_count = 0
    
    for test_id in all_test_ids:
        messages = {proxy: all_test_messages[proxy].get(test_id, '') for proxy in proxy_folders if proxy in all_test_messages}
        unique_messages = set(messages.values())
        
        if len(unique_messages) == 1:
            consistent_count += 1
            message = next(iter(unique_messages))
            consistency_data.append([test_id, '✓', message if message else 'No message'])
            
            # Track specific consistency types
            if message in ["Timeout occurred while waiting for client connection. Proxy dropped client's frames.",
                         "Proxy returned an error"]:
                consistent_timeout_count += 1
            else:
                consistent_no_timeout_count += 1
        else:
            consistency_data.append([test_id, '', 'Inconsistent behavior across proxies'])
    
    # Add summary rows
    consistency_data.append(['', '', ''])
    consistency_data.append(['Total consistent tests:', str(consistent_count), ''])
    consistency_data.append(['Consistent timeout/error tests:', str(consistent_timeout_count), ''])
    consistency_data.append(['Consistent no-timeout tests:', str(consistent_no_timeout_count), ''])
    
    consistency_table = create_markdown_table(
        ['Test ID', 'Consistent', 'Behavior'],
        consistency_data
    )
    
    with open(os.path.join(summaries_dir, 'behavior_consistency.md'), 'w') as f:
        f.write(consistency_table)

    # Add these lines after analyzing results:
    
    output_dir = 'visualizations'
    create_proxy_correlation_matrix(all_test_results, output_dir)
    create_proxy_vector_graph(all_test_results, output_dir)
    create_proxy_timeout_pies(all_test_results, output_dir)

if __name__ == "__main__":
    main()