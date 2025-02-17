import json
import os
from datetime import datetime
import glob

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

if __name__ == "__main__":
    main()