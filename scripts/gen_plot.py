import pandas as pd
import matplotlib.pyplot as plt
import os
import re # Import regex for advanced cleaning

# =========================================================================
# === USER INPUT REQUIRED: Set the path to your log file here. ===
# =========================================================================
input_file = '/workspaces/adsa_g14_assignment_1/logs/customer_log.txt' 
# For example, if your file is in a different location:
# input_file = '/Users/YourName/Desktop/customer_log.txt'
# =========================================================================


def clean_and_parse_line(line):
    """
    Cleans a single log line, removing timestamps, source tags, and inconsistent 
    spacing, and returns the 5 expected data fields.
    """
    # 1. Remove timestamp and log marker (e.g., "[2025-12-14 09:18:20] ")
    # This also handles the case where the timestamp might be missing at the start of a continuation line.
    match_timestamp = re.search(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] (.*)', line)
    if match_timestamp:
        data_part = match_timestamp.group(1).strip()
    else:
        # If no timestamp found, assume the entire line is the data part (useful for multi-line entries)
        data_part = line.strip()

    # 2. Remove source tags (e.g., "")
    data_part = re.sub('\'', '', data_part).strip()

    # 3. Clean up separators and extra white space around commas
    data_part = data_part.replace(', ', ',').replace(' ,', ',').strip()
    
    # 4. Use regex to split the line into exactly 5 parts based on the known structure:
    # (Scenario Name), (Iterations), (BST Time), (Splay Time), (Improved Time)
    # The split is complex because Scenario names have spaces. We use a defined pattern.
    
    # Pattern explanation:
    # (.*?),   -> Capture the scenario name (Scenario A, etc.) lazily until the first comma
    # (\d+),   -> Capture the iteration count (50, 1000, etc.)
    # ([\d\.]*), -> Capture the first time value (BST)
    # ([\d\.]*), -> Capture the second time value (Splay Tree)
    # ([\d\.]*)  -> Capture the third time value (Improved Splay Tree)
    
    match = re.search(r'^(.*?),([\d\s]+),([\d\.]+),([\d\.]+),([\d\.]+)$', data_part)

    if match:
        fields = list(match.groups())
        # Clean up the iteration field just in case
        fields[1] = fields[1].strip()
        return fields
    
    return None

def process_log_data(file_path):
    """
    Reads the performance log file, processes the data, and generates 
    grouped bar charts comparing tree performance for each scenario.
    """
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at path: {file_path}")
        return

    print(f"--- 1. Reading and Processing Data from: {file_path} ---")
    
    processed_lines = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                fields = clean_and_parse_line(line)
                if fields:
                    processed_lines.append(fields)

    except Exception as e:
        print(f"An error occurred during file reading or parsing: {e}")
        return

    if not processed_lines:
        print("No valid data lines were found in the file. Check the log format.")
        return

    # Create a DataFrame from the processed data
    columns = ['Scenario', 'Iterations', 'BST', 'Splay Tree', 'Improved Splay Tree']
    df = pd.DataFrame(processed_lines, columns=columns)

    # Convert the numerical columns to appropriate data types
    try:
        df['Iterations'] = pd.to_numeric(df['Iterations'])
        df['BST'] = pd.to_numeric(df['BST'])
        df['Splay Tree'] = pd.to_numeric(df['Splay Tree'])
        df['Improved Splay Tree'] = pd.to_numeric(df['Improved Splay Tree'])
    except ValueError as e:
        print(f"Error converting columns to numeric. Check for non-numeric data in time/iteration fields. Error: {e}")
        return

    # --- 2. Generate Bar Charts for Each Scenario ---

    scenarios = df['Scenario'].unique()
    print(f"\n--- 2. Generating Charts for {len(scenarios)} Scenarios: {', '.join(scenarios)} ---")

    for scenario in scenarios:
        scenario_df = df[df['Scenario'] == scenario].copy()

        fig, ax = plt.subplots(figsize=(10, 6))

        bar_width = 0.25
        x = range(len(scenario_df))
        
        r1 = [i - bar_width for i in x]
        r2 = x
        r3 = [i + bar_width for i in x]

        # Plot the bars
        ax.bar(r1, scenario_df['BST'], color='skyblue', width=bar_width, edgecolor='grey', label='BST')
        ax.bar(r2, scenario_df['Splay Tree'], color='lightcoral', width=bar_width, edgecolor='grey', label='Splay Tree')
        ax.bar(r3, scenario_df['Improved Splay Tree'], color='mediumseagreen', width=bar_width, edgecolor='grey', label='Improved Splay Tree')

        ax.set_xlabel('Number of Iterations', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(scenario_df['Iterations'].astype(str))

        # # Conditional log scale logic
        # time_data = scenario_df[['BST', 'Splay Tree', 'Improved Splay Tree']]
        # time_min = time_data.min().min()
        # time_max = time_data.max().max()
        
        # if time_min > 0 and (time_max / time_min) > 100:
        #     ax.set_yscale('log')
        #     ax.set_ylabel('Time Taken (seconds) - Log Scale', fontweight='bold')
        # else:
        #     ax.set_ylabel('Time Taken (seconds)', fontweight='bold')
        ax.set_ylabel('Time Taken (seconds)', fontweight='bold')
        ax.set_title(f'Performance Comparison for {scenario}', fontweight='bold')
        
        ax.legend()
        plt.grid(axis='y', linestyle='--')
        plt.tight_layout()
        
        # Save the figure
        log_dir = os.path.dirname(file_path) if os.path.dirname(file_path) else '.'
        output_filename = os.path.join(log_dir, f'performance_chart_{scenario.replace(" ", "_")}.png')
        plt.savefig(output_filename)
        print(f"Generated chart: {output_filename}")

        plt.close(fig)

    print("\n--- Script Finished Successfully ---")

# --- Main Execution Block ---
if __name__ == "__main__":
    process_log_data(input_file)