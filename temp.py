import os
import time
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from alive_progress import alive_bar
import plotly.graph_objects as go
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def parse_test_outcomes_table(content):
    lines = content.splitlines()
    data = []
    columns = []
    recording = False  # Flag to indicate when we're reading the desired table
    for line in lines:
        line = line.strip()
        if line.startswith('Test Outcomes:'):
            recording = True  # Start recording the table
            continue
        elif recording and line.startswith('Summary Table:'):
            recording = False  # Stop recording when we reach the next table
            break
        elif recording:
            if line.startswith('+') or line == '':
                continue
            elif line.startswith('|'):
                # Split the line on '|'
                items = line.strip('|').split('|')
                # Strip whitespace
                items = [item.strip() for item in items]
                if not columns:
                    # This is the header line
                    columns = items
                else:
                    # Data line
                    if len(items) == len(columns):
                        data.append(items)
    if not data:
        return None  # Return None if no data was found
    df = pd.DataFrame(data, columns=columns)
    return df

def create_distance_matrix(df):
    outcomes = []
    for _, row in df.iterrows():
        if int(row['Modified']) == 1:
            outcome = 1
        elif int(row['Rejected']) == 1:
            outcome = 2
        elif int(row['Unmodified']) == 1:
            outcome = 3
        else:
            outcome = 0  # No outcome
        outcomes.append(outcome)

    n = len(outcomes)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance_matrix[i, j] = 0 if outcomes[i] == outcomes[j] else 1
    return distance_matrix, outcomes

def create_result_matrices(results, file_names):
    corr_matrix = pd.DataFrame(index=file_names, columns=file_names)

    for (file_i, file_j), corr_coeff in results.items():
        corr_matrix.loc[file_i, file_j] = corr_matrix.loc[file_j, file_i] = corr_coeff

    for file_name in file_names:
        corr_matrix.loc[file_name, file_name] = 1.0

    return corr_matrix.astype(float)

def visualize_results(corr_matrix, output_directory):
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', xticklabels=True, yticklabels=True)
    plt.title('Mantel Test Correlation Coefficients between Matrices')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'correlation_coefficients_heatmap.png'))
    plt.close()

def categorize_correlations(corr_matrix):
    def categorize_correlation(r):
        if abs(r) >= 0.7:
            return 'Strongly Correlated (r >= 0.7)'
        elif abs(r) >= 0.4:
            return 'Moderately Correlated (0.4 <= r < 0.7)'
        elif abs(r) >= 0.2:
            return 'Weakly Correlated (0.2 <= r < 0.4)'
        else:
            return 'Not Correlated (r < 0.2)'

    categories_matrix = corr_matrix.map(categorize_correlation)
    return categories_matrix

def generate_markdown_table(categories_matrix, file_names, output_directory):
    table_header = '+------------------+------------------+----------------------------------------+\n'
    table_format = '| {:16} | {:16} | {:38} |\n'
    table_separator = '+------------------+------------------+----------------------------------------+\n'

    markdown_table = 'Correlation Categories:\n' + table_header
    markdown_table += table_format.format('File 1', 'File 2', 'Correlation Category') + table_header

    for i in range(len(file_names)):
        for j in range(i+1, len(file_names)):
            file_i, file_j = file_names[i], file_names[j]
            category = categories_matrix.loc[file_i, file_j]
            markdown_table += table_format.format(file_i, file_j, category) + table_separator

    with open(os.path.join(output_directory, 'correlation_categories.md'), 'w') as md_file:
        md_file.write(markdown_table)

def create_test_summary_table(outcomes_dict, output_directory):
    # Initialize a dictionary to store counts for each test
    test_counts = {}
    total_proxies = len(outcomes_dict)

    # Count the outcomes for each test across all proxies
    for proxy, outcomes in outcomes_dict.items():
        for test_num, outcome in enumerate(outcomes, 1):
            if test_num not in test_counts:
                test_counts[test_num] = {'Modified': 0, 'Unmodified': 0, 'Rejected': 0}
            if outcome == 1:
                test_counts[test_num]['Modified'] += 1
            elif outcome == 2:
                test_counts[test_num]['Rejected'] += 1
            elif outcome == 3:
                test_counts[test_num]['Unmodified'] += 1

    # Create the Markdown table
    markdown_table = "# Test Summary Table\n\n"
    markdown_table += "| Test Number | Modified | Unmodified | Rejected | Inconclusive |\n"
    markdown_table += "|-------------|----------|------------|----------|--------------|"

    for test_num in sorted(test_counts.keys()):
        counts = test_counts[test_num]
        inconclusive = total_proxies - sum(counts.values())
        markdown_table += f"\n| {test_num:11d} | {counts['Modified']:8d} | {counts['Unmodified']:10d} | {counts['Rejected']:8d} | {inconclusive:12d} |"
        markdown_table += "\n|-------------|----------|------------|----------|--------------|"

    # Remove the last separator line
    markdown_table = markdown_table.rstrip("\n|-------------|----------|------------|----------|--------------|")

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Write the Markdown table to a file
    with open(os.path.join(output_directory, 'test_summary_table.md'), 'w') as mdfile:
        mdfile.write(markdown_table)

def create_overall_summary_table(outcomes_dict, output_directory):
    total_modified = 0
    total_unmodified = 0
    total_rejected = 0

    for outcomes in outcomes_dict.values():
        total_modified += outcomes.count(1)
        total_rejected += outcomes.count(2)
        total_unmodified += outcomes.count(3)

    total_tests = total_modified + total_unmodified + total_rejected

    # Create the Markdown table
    markdown_table = "# Overall Summary Table\n\n"
    markdown_table += "| Category   | Count | Percentage |\n"
    markdown_table += "|------------|-------|------------|\n"
    markdown_table += f"| Modified   | {total_modified:5d} | {total_modified/total_tests*100:10.2f}% |\n"
    markdown_table += f"| Unmodified | {total_unmodified:5d} | {total_unmodified/total_tests*100:10.2f}% |\n"
    markdown_table += f"| Rejected   | {total_rejected:5d} | {total_rejected/total_tests*100:10.2f}% |\n"
    markdown_table += f"| Total      | {total_tests:5d} | 100.00% |"

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Write the Markdown table to a file
    with open(os.path.join(output_directory, 'overall_summary_table.md'), 'w') as mdfile:
        mdfile.write(markdown_table)

def calculate_proxy_conformance_scores(outcomes_dict, output_directory):
    with open('categories.json', 'r') as f:
        test_categories = json.load(f)
    
    request_tests = set(test_categories['requests'])
    response_tests = set(test_categories['responses'])
    
    conformance_scores = {}
    
    for proxy, outcomes in outcomes_dict.items():
        total_tests = len(outcomes)
        
        overall_modified = sum(1 for outcome in outcomes if outcome == 1)
        overall_rejected = sum(1 for outcome in outcomes if outcome == 2)
        overall_unmodified = sum(1 for outcome in outcomes if outcome == 3)
        
        request_modified = sum(1 for i, outcome in enumerate(outcomes, 1) if i in request_tests and outcome == 1)
        request_rejected = sum(1 for i, outcome in enumerate(outcomes, 1) if i in request_tests and outcome == 2)
        request_unmodified = sum(1 for i, outcome in enumerate(outcomes, 1) if i in request_tests and outcome == 3)
        
        response_modified = sum(1 for i, outcome in enumerate(outcomes, 1) if i in response_tests and outcome == 1)
        response_rejected = sum(1 for i, outcome in enumerate(outcomes, 1) if i in response_tests and outcome == 2)
        response_unmodified = sum(1 for i, outcome in enumerate(outcomes, 1) if i in response_tests and outcome == 3)
        
        conformance_scores[proxy] = {
            'overall': {
                'modified': overall_modified,
                'rejected': overall_rejected,
                'unmodified': overall_unmodified,
            },
            'request': {
                'modified': request_modified,
                'rejected': request_rejected,
                'unmodified': request_unmodified,
            },
            'response': {
                'modified': response_modified,
                'rejected': response_rejected,
                'unmodified': response_unmodified,
            }
        }
    
    # Find the longest proxy name for consistent column width
    max_proxy_name_length = max(len(os.path.splitext(proxy)[0]) for proxy in conformance_scores.keys())
    proxy_column_width = max(max_proxy_name_length, 30)  # Ensure it's at least 30 characters wide
    
    # Create the Markdown tables
    markdown_tables = "# Proxy Conformance Scores\n\n"
    
    for category in ['overall', 'request', 'response']:
        markdown_tables += f"## {category.capitalize()} Conformance\n\n"
        markdown_tables += "| {:<{width}} | {:^10} | {:^10} | {:^10} |\n".format(
            "Proxy", "Modified", "Rejected", "Unmodified", width=proxy_column_width)
        markdown_tables += "|{:-<{width}}|{:-^10}|{:-^10}|{:-^10}|\n".format(
            "", "", "", "", width=proxy_column_width)
        
        sorted_scores = sorted(conformance_scores.items(), 
                               key=lambda x: (x[1][category]['modified'] + x[1][category]['rejected'], x[1][category]['modified']), 
                               reverse=True)
        
        for proxy, scores in sorted_scores:
            proxy_name = os.path.splitext(proxy)[0].ljust(proxy_column_width)
            modified = scores[category]['modified']
            rejected = scores[category]['rejected']
            unmodified = scores[category]['unmodified']
            
            markdown_tables += "| {:<{width}} | {:^10} | {:^10} | {:^10} |\n".format(
                proxy_name, modified, rejected, unmodified, width=proxy_column_width)
        
        markdown_tables += "\n\n"
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Write the Markdown tables to a file
    with open(os.path.join(output_directory, 'proxy_conformance_scores.md'), 'w') as mdfile:
        mdfile.write(markdown_tables)

    return conformance_scores  # Add this line to return the dictionary

def create_proxy_conformance_distribution(outcomes_dict, output_directory):
    # Create the plane z + x + y = 47 for both Matplotlib and Plotly
    x = y = np.linspace(0, 47, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.clip(47 - X - Y, 0, 10)  # Clip Z values to max of 10
    
    # Matplotlib (static) version
    fig_mpl = plt.figure(figsize=(12, 8))
    ax = fig_mpl.add_subplot(111, projection='3d')

    colors = plt.cm.rainbow(np.linspace(0, 1, len(outcomes_dict)))

    for (proxy, outcomes), color in zip(outcomes_dict.items(), colors):
        modified = sum(1 for outcome in outcomes if outcome == 1)
        rejected = sum(1 for outcome in outcomes if outcome == 2)
        unmodified = sum(1 for outcome in outcomes if outcome == 3)
        
        ax.scatter(modified, unmodified, rejected, c=[color], s=100, label=proxy)

    ax.plot_surface(X, Y, Z, alpha=0.3, color='gray')

    ax.set_xlabel('Modified')
    ax.set_ylabel('Unmodified')
    ax.set_zlabel('Rejected')
    ax.set_title('Proxy Conformance Distribution')

    # Set axis limits
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 30)
    ax.set_zlim(0, 10)

    # Adjust the legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()

    # Plotly (interactive) version
    fig_plotly = go.Figure()

    for proxy, outcomes in outcomes_dict.items():
        modified = sum(1 for outcome in outcomes if outcome == 1)
        rejected = sum(1 for outcome in outcomes if outcome == 2)
        unmodified = sum(1 for outcome in outcomes if outcome == 3)
        
        fig_plotly.add_trace(go.Scatter3d(
            x=[modified],
            y=[unmodified],
            z=[rejected],
            mode='markers',
            name=proxy,
            marker=dict(size=5),
            text=[f"{proxy}<br>Modified: {modified}<br>Unmodified: {unmodified}<br>Rejected: {rejected}"],
            hoverinfo='text'
        ))

    # Add the plane to the Plotly figure
    fig_plotly.add_trace(go.Surface(
        x=X,
        y=Y,
        z=Z,
        opacity=0.3,
        showscale=False,
        name='z + x + y = 47 (z <= 10)'
    ))

    # Update Plotly layout
    fig_plotly.update_layout(
        scene=dict(
            xaxis_title='Modified',
            yaxis_title='Unmodified',
            zaxis_title='Rejected',
            xaxis=dict(range=[0, 30]),
            yaxis=dict(range=[0, 30]),
            zaxis=dict(range=[0, 10]),
        ),
        title='Proxy Conformance Distribution',
        margin=dict(r=0, b=0, l=0, t=40),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
    )

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Save the Matplotlib plot
    plt.savefig(os.path.join(output_directory, 'proxy_conformance_distribution_static.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Save the Plotly plot as an interactive HTML file
    fig_plotly.write_html(os.path.join(output_directory, 'proxy_conformance_distribution_interactive.html'))

def create_test_bar_charts(outcomes_dict, output_directory):
    # Create a subdirectory for the bar charts
    charts_directory = os.path.join(output_directory, 'test_bar_charts')
    os.makedirs(charts_directory, exist_ok=True)

    # Get the number of tests
    num_tests = len(next(iter(outcomes_dict.values())))

    # Prepare data for each test
    for i in range(1, num_tests + 1):
        # Adjust the test number to skip 27-31
        if i <= 26:
            test_num = i
        else:
            test_num = i + 5

        modified = 0
        unmodified = 0
        rejected = 0
        inconclusive = 0

        for outcomes in outcomes_dict.values():
            outcome = outcomes[i - 1]  # Use i-1 as index since i starts from 1
            if outcome == 1:
                modified += 1
            elif outcome == 2:
                rejected += 1
            elif outcome == 3:
                unmodified += 1
            else:
                inconclusive += 1

        # Create bar chart
        categories = ['Modified', 'Unmodified', 'Rejected', 'Inconclusive']
        values = [modified, unmodified, rejected, inconclusive]
        colors = ['green', 'blue', 'red', 'gray']

        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, values, color=colors)
        plt.title(f'Test {test_num} Outcomes', fontsize=16, fontweight='bold')
        plt.ylabel('Number of Proxies', fontsize=14, fontweight='bold')
        plt.ylim(0, len(outcomes_dict))  # Set y-axis limit to total number of proxies

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height}',
                     ha='center', va='bottom', fontsize=12, fontweight='bold')

        # Increase font size for x-axis and y-axis labels
        plt.xticks(fontsize=12, fontweight='bold')
        plt.yticks(fontsize=12, fontweight='bold')

        # Save the chart
        plt.tight_layout()
        plt.savefig(os.path.join(charts_directory, f'test_{test_num}_bar_chart.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
def create_proxy_bar_charts(outcomes_dict, output_directory):
    # Create a subdirectory for the proxy bar charts
    charts_directory = os.path.join(output_directory, 'proxy_bar_charts')
    os.makedirs(charts_directory, exist_ok=True)

    categories = ['Modified', 'Unmodified', 'Rejected']
    colors = ['green', 'blue', 'red']

    for proxy, outcomes in outcomes_dict.items():
        modified = outcomes.count(1)
        unmodified = outcomes.count(3)
        rejected = outcomes.count(2)

        values = [modified, unmodified, rejected]

        plt.figure(figsize=(12, 8))  # Increased figure size
        bars = plt.bar(range(len(categories)), values, color=colors)
        plt.ylabel('Number of Tests', fontsize=18, fontweight='bold')
        plt.ylim(0, max(modified, unmodified, rejected) + 2)  # Set y-axis limit

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height}',
                     ha='center', va='bottom', fontsize=16, fontweight='bold')

        # Set x-ticks and labels
        plt.xticks(range(len(categories)), categories, fontsize=16, fontweight='bold')
        
        # Set y-ticks
        plt.yticks(range(0, 31, 5), fontsize=16, fontweight='bold')

        # Save the chart
        plt.tight_layout()
        plt.savefig(os.path.join(charts_directory, f'{os.path.splitext(proxy)[0]}_bar_chart.png'), dpi=300, bbox_inches='tight')
        plt.close()

def create_proxy_vector_graph(outcomes_dict, output_directory):
    charts_directory = os.path.join(output_directory, 'vector_graphs')
    os.makedirs(charts_directory, exist_ok=True)

    num_proxies = len(outcomes_dict)
    num_tests = len(next(iter(outcomes_dict.values())))

    fig, ax = plt.subplots(figsize=(20, num_proxies * 1.5))

    for i, (proxy, outcomes) in enumerate(outcomes_dict.items()):
        y_values = [2 if outcome == 3 else 1 if outcome == 2 else 0 for outcome in outcomes]
        x_values = range(1, num_tests + 1)
        
        # Plot the line without filling
        ax.plot(x_values, [y + i * 3 for y in y_values], '-o', linewidth=2, markersize=4)

    # Set y-ticks and labels
    y_ticks = []
    y_labels_left = []
    y_labels_right = []
    for i, proxy in enumerate(outcomes_dict.keys()):
        y_ticks.extend([i * 3, i * 3 + 1, i * 3 + 2])
        proxy_name = os.path.splitext(proxy)[0]
        if proxy_name == "Azure Application Gateway (Standard V2)":
            proxy_name = "Azure AG (SV2)"
        else:
            proxy_name = proxy_name.capitalize()
        y_labels_left.extend(['', proxy_name, ''])
        y_labels_right.extend(['M', 'R', 'U'])

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels_left, fontsize=16, fontweight='bold')  # Increased font size and made bold
    
    # Add labels on the right side
    ax2 = ax.twinx()
    ax2.set_yticks(y_ticks)
    ax2.set_yticklabels(y_labels_right, fontsize=18, fontweight='bold')
    ax2.set_ylim(ax.get_ylim())  # Align the right y-axis with the left one

    ax.set_xlabel('Test Identifier', fontsize=18, fontweight='bold')  # Increased font size
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Increase font size for x-axis tick labels and make them bold
    ax.tick_params(axis='x', labelsize=14)

    # Add legend/mapping
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='M: Modified',
                   markerfacecolor='black', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='R: Rejected',
                   markerfacecolor='black', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='U: Unmodified',
                   markerfacecolor='black', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=3, fontsize=16)

    # Adjust layout to make room for labels and legend
    plt.subplots_adjust(left=0.2, right=0.85, bottom=0.15)
    
    plt.savefig(os.path.join(charts_directory, 'proxy_vector_graph.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_pearson_correlation_heatmap(outcomes_dict, output_directory):
    charts_directory = os.path.join(output_directory, 'correlation_heatmaps')
    os.makedirs(charts_directory, exist_ok=True)

    # Convert outcomes to numerical arrays
    proxy_arrays = {proxy: np.array([1 if o == 1 else -1 if o == 2 else 0 for o in outcomes]) 
                    for proxy, outcomes in outcomes_dict.items()}

    # Calculate correlation matrix
    proxies = list(proxy_arrays.keys())
    corr_matrix = np.zeros((len(proxies), len(proxies)))
    for i, proxy1 in enumerate(proxies):
        for j, proxy2 in enumerate(proxies):
            if i != j:
                corr, _ = pearsonr(proxy_arrays[proxy1], proxy_arrays[proxy2])
                corr_matrix[i, j] = corr
            else:
                corr_matrix[i, j] = 1.0  # Correlation with itself is always 1

    # Prepare labels with abbreviated names
    labels = []
    for proxy in proxies:
        proxy_name = os.path.splitext(proxy)[0]
        if proxy_name == "Azure Application Gateway (Standard V2)":
            proxy_name = "Azure AG (SV2)"
        else:
            proxy_name = proxy_name.capitalize()
        labels.append(proxy_name)

    # Create heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, 
                xticklabels=labels, yticklabels=labels, cbar=False,
                annot_kws={'size': 14, 'weight': 'bold'})
    plt.xticks(rotation=45, ha='right', fontsize=16, fontweight='bold')
    plt.yticks(fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_directory, 'proxy_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_overall_conformance_dot_plot(conformance_scores, output_directory):
    # Prepare data for the dot plot
    proxies = []
    modified = []
    rejected = []
    unmodified = []

    for proxy, scores in conformance_scores.items():
        proxies.append(os.path.splitext(proxy)[0])  # Remove file extension
        modified.append(scores['overall']['modified'])
        rejected.append(scores['overall']['rejected'])
        unmodified.append(scores['overall']['unmodified'])

    # Create the dot plot
    plt.figure(figsize=(12, 8))
    
    # Plot only the dots without lines
    plt.scatter(modified, proxies, color='green', label='Modified', s=64)
    plt.scatter(rejected, proxies, color='red', label='Rejected', s=64)
    plt.scatter(unmodified, proxies, color='blue', label='Unmodified', s=64)

    # Customize the plot
    plt.title('Overall Conformance by Proxy', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Tests', fontsize=14, fontweight='bold')
    plt.ylabel('Proxy', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Adjust y-axis labels
    plt.yticks(fontsize=12)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'overall_conformance_dot_plot.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_test_conformance_dot_plot(test_summary, output_directory):
    # Prepare data for the dot plot
    tests = []
    modified = []
    rejected = []
    unmodified = []

    for test, outcomes in test_summary.items():
        tests.append(test)
        modified.append(outcomes['Modified'])
        rejected.append(outcomes['Rejected'])
        unmodified.append(outcomes['Unmodified'])

    # Create the dot plot
    plt.figure(figsize=(20, 12))

    # Plot dots and lines for each test
    for i, test in enumerate(tests):
        x = [test] * 3
        y = [modified[i], unmodified[i], rejected[i]]
        colors = ['green', 'blue', 'red']
        labels = ['Modified', 'Unmodified', 'Rejected'] if i == 0 else [None, None, None]

        # Plot the line
        plt.plot(x, y, color='gray', alpha=0.5, zorder=1)

        # Plot the dots
        for j, (yi, color, label) in enumerate(zip(y, colors, labels)):
            plt.scatter(x[j], yi, color=color, s=64, label=label, zorder=2)

    # Customize the plot
    plt.title('Test Conformance Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Test Number', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Proxies', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adjust x-axis labels
    plt.xticks(tests, fontsize=10, rotation=45, ha='right')

    # Set y-axis limit
    plt.ylim(0, max(max(modified), max(rejected), max(unmodified)) + 1)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'test_conformance_dot_plot.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_proxy_matrix_graph(outcomes_dict, output_directory):
    charts_directory = os.path.join(output_directory, 'matrix_graphs')
    os.makedirs(charts_directory, exist_ok=True)

    # Define colors
    colors = {
        1: '#ff6b6b',  # Modified (red)
        2: '#4ecdc4',  # Rejected (green)
        3: '#ffd93d',  # Unmodified (yellow)
        0: '#95a5a6'   # Default/Unknown (gray)
    }

    # Group proxies by configurability
    non_configurable = [
        "Azure", 
        "bunny",
        "Imperva",
        "Cloudflare"
    ]
    
    # Sort proxies into configurable and non-configurable
    sorted_proxies = {
        'Configurable': [],
        'Non-configurable': []
    }
    
    for proxy in outcomes_dict.keys():
        if any(proxy.lower().startswith(conf_proxy.lower()) for conf_proxy in non_configurable):
            sorted_proxies['Non-configurable'].append(proxy)
        else:
            sorted_proxies['Configurable'].append(proxy)
    
    # Sort within each category
    for category in sorted_proxies:
        sorted_proxies[category].sort()

    # Initialize the matrix data and labels
    matrix_data = []
    proxy_labels = []
    
    # Process data and create labels
    for category in ['Configurable', 'Non-configurable']:
        if sorted_proxies[category]:
            if matrix_data:  # Add separator between categories
                matrix_data.append([0] * len(next(iter(outcomes_dict.values()))))
                proxy_labels.append('')
            
            for proxy in sorted_proxies[category]:
                outcomes = outcomes_dict[proxy]
                matrix_data.append(outcomes)
                proxy_name = os.path.splitext(proxy)[0]
                if proxy_name == "Azure Application Gateway (Standard V2)":
                    proxy_name = "Azure AG (SV2)"
                proxy_labels.append(proxy_name)

    # Later, after creating the grid, add a thicker line at the separator position

    matrix_data = np.array(matrix_data)
    num_tests = matrix_data.shape[1]
    
    # Create figure with adjusted size (increased height multiplier from 0.4 to 0.6)
    fig = plt.figure(figsize=(16, len(matrix_data) * 0.6 + 1))
    
    # Create main matrix subplot with adjusted spacing
    ax_matrix = plt.subplot2grid((len(matrix_data) + 1, num_tests + 6), 
                               (0, 0), 
                               rowspan=len(matrix_data), 
                               colspan=num_tests)
    
    # if separator_index is not None:
    #     ax_matrix.axhline(y=len(matrix_data) - separator_index, color='white', linewidth=20)

    # Plot matrix with taller rectangles
    height = 1.25  # Rectangle height
    
    for i in range(len(matrix_data)):
        for j in range(num_tests):
            outcome = matrix_data[i][j]
            if proxy_labels[i]:
                color = colors[outcome]
                y_pos = (len(matrix_data)-1-i) * height
                rect = plt.Rectangle((j, y_pos), 1, height, facecolor=color)
                ax_matrix.add_patch(rect)

    # Adjust axis limits and grid
    ax_matrix.set_xlim(0, num_tests)
    ax_matrix.set_ylim(0, len(matrix_data) * height)
    
    # Set grid lines to match the new height
    ax_matrix.set_xticks(np.arange(num_tests + 1))
    ax_matrix.set_yticks(np.arange(0, len(matrix_data) * height + height, height))
    
    # Set label positions
    ax_matrix.set_xticks(np.arange(0.5, num_tests + 0.5), minor=True)
    ax_matrix.set_yticks(np.arange(height/2, len(matrix_data) * height, height), minor=True)

    # Configure labels with larger font size
    ax_matrix.tick_params(axis='x', which='minor', labelsize=10)  # Increased from 8
    ax_matrix.tick_params(axis='y', which='minor', labelsize=12)  # Increased from 8

    # Configure labels
    ax_matrix.set_xticklabels(range(1, num_tests + 1), minor=True)
    ax_matrix.set_yticklabels(proxy_labels[::-1], minor=True)
    ax_matrix.set_xticklabels([], minor=False)
    ax_matrix.set_yticklabels([], minor=False)
    
    # Configure grid
    ax_matrix.grid(True, which='major', color='white', linewidth=1.5)  # Reduced linewidth from 2
    ax_matrix.tick_params(which='both', length=0)

    # Add "Tests" label with larger font
    plt.text(num_tests/2, -1, 'Tests', 
             horizontalalignment='center', 
             verticalalignment='center', 
             fontsize=12,  # Increased from 10
             fontweight='bold')

    # Add column totals with headers (larger font)
    plt.text(-0.5, -1.5, "M", horizontalalignment='right', verticalalignment='top', fontsize=12)  # Increased from 8
    plt.text(-0.5, -2.1, "R", horizontalalignment='right', verticalalignment='top', fontsize=12)
    plt.text(-0.5, -2.7, "U", horizontalalignment='right', verticalalignment='top', fontsize=12)

    # Add column totals in table format with larger font
    for j in range(num_tests):
        modified = sum(1 for i in range(len(matrix_data)) 
                      if proxy_labels[i] and matrix_data[i][j] == 1)
        rejected = sum(1 for i in range(len(matrix_data)) 
                      if proxy_labels[i] and matrix_data[i][j] == 2)
        unmodified = sum(1 for i in range(len(matrix_data)) 
                        if proxy_labels[i] and matrix_data[i][j] == 3)
        
        # Display numbers with larger font
        plt.text(j + 0.5, -1.5, str(modified), 
                horizontalalignment='center', verticalalignment='top', fontsize=10)
        plt.text(j + 0.5, -2.1, str(rejected), 
                horizontalalignment='center', verticalalignment='top', fontsize=10)
        plt.text(j + 0.5, -2.7, str(unmodified), 
                horizontalalignment='center', verticalalignment='top', fontsize=10)

    # Add row totals header with proper spacing and alignment
    header_text = f"{'M':>4}  {'R':>4}  {'U':>4}"
    plt.text(num_tests + 1, (len(matrix_data) * height) + height/2, header_text,
            horizontalalignment='left', verticalalignment='center', fontsize=12)

    # Add row totals with aligned columns
    for i, label in enumerate(proxy_labels):
        if label:
            modified = sum(1 for x in matrix_data[i] if x == 1)
            rejected = sum(1 for x in matrix_data[i] if x == 2)
            unmodified = sum(1 for x in matrix_data[i] if x == 3)
            
            # Format each number with right alignment and consistent spacing
            total_text = f"{modified:>4}  {rejected:>3}  {unmodified:>2}"
            
            # Adjust y-position to match the new rectangle height
            y_pos = (len(matrix_data)-1-i) * height + height/2
            
            plt.text(num_tests + 1, y_pos, total_text,
                    horizontalalignment='left', verticalalignment='center',
                    family='monospace', fontsize=10)

    # Adjust layout with tighter spacing
    plt.tight_layout(h_pad=1, w_pad=1)  # Added tighter spacing parameters
    
    plt.savefig(os.path.join(charts_directory, 'proxy_matrix_graph.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def run_analysis(input_directory='../../output/analysis', output_directory='../../output/results'):
    start_time = time.time()
    
    with alive_bar(title="Running comparator", spinner="dots", stats=None, bar=None) as bar:
        distance_matrices = {}
        outcomes_dict = {}
        file_list = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
        
        for filename in file_list:
            filepath = os.path.join(input_directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()

            df = parse_test_outcomes_table(content)
            if df is None or not all(col in df.columns for col in ['Test Number', 'Modified', 'Rejected', 'Unmodified']):
                print(f"Invalid data in file {filename}")
                continue

            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            for col in ['Test Number', 'Modified', 'Rejected', 'Unmodified']:
                df[col] = df[col].astype(int)

            distance_matrix, outcomes = create_distance_matrix(df)
            distance_matrices[filename] = distance_matrix
            outcomes_dict[filename] = outcomes

        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Create the test summary table
        # create_test_summary_table(outcomes_dict, output_directory)

        # Create the overall summary table
        # create_overall_summary_table(outcomes_dict, output_directory)

        # Calculate proxy conformance scores
        conformance_scores = calculate_proxy_conformance_scores(outcomes_dict, output_directory)

        # Add this line to create the dot plot
        # create_overall_conformance_dot_plot(conformance_scores, output_directory)

        # Create proxy conformance distribution
        # create_proxy_conformance_distribution(outcomes_dict, output_directory)

        # Create bar charts for each test
        # create_test_bar_charts(outcomes_dict, output_directory)

        # Create bar charts for each proxy
        # create_proxy_bar_charts(outcomes_dict, output_directory)

        # Create the vector graph for all proxies
        # create_proxy_vector_graph(outcomes_dict, output_directory)

        # Create the Pearson correlation heatmap
        # create_pearson_correlation_heatmap(outcomes_dict, output_directory)

        # Create the proxy matrix graph
        create_proxy_matrix_graph(outcomes_dict, output_directory)

        # Create test summary data
        test_summary = {}
        for outcomes in outcomes_dict.values():
            for i, outcome in enumerate(outcomes, 1):
                if i not in test_summary:
                    test_summary[i] = {'Modified': 0, 'Rejected': 0, 'Unmodified': 0}
                if outcome == 1:
                    test_summary[i]['Modified'] += 1
                elif outcome == 2:
                    test_summary[i]['Rejected'] += 1
                elif outcome == 3:
                    test_summary[i]['Unmodified'] += 1

        # Create the test conformance dot plot
        create_test_conformance_dot_plot(test_summary, output_directory)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Analysis complete. Results have been saved to the output directory.")

if __name__ == "__main__":
    run_analysis()