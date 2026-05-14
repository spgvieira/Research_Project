import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# This file contains functions generated with the help of Google LLM GEMINI to plot
# the visualizations used throughout the project

def plot_change_matrix():
    # Load data
    df = pd.read_csv('Results/ChangeMatrixSumNoRSC.csv', index_col=0)

    # Calculate percentages based on columns (initial year)
    row_sums = df.sum(axis=0)
    df_percent = df.div(row_sums, axis=1) * 100

    # Create custom labels: "Raw Value \n (Percentage%)"
    # We use a nested list comprehension to format each cell
    labels = np.array([
        [f"{pct:.1f}%\n({val:.2f})" for val, pct in zip(row_val, row_pct)]
        for row_val, row_pct in zip(df.values, df_percent.values)
    ])

    plt.figure(figsize=(14, 12))
    
    # We pass 'labels' to annot and set fmt to "" since the strings are pre-formatted
    sns.heatmap(df_percent, 
                annot=labels,
                fmt="",
                cmap="Blues",
                vmin=0.0,
                vmax=100,
                annot_kws={'size': 12}, # Adjust font size here to fit both lines
                cbar_kws={'label': 'Percentage Class Area Change'})
    
    plt.xlabel("Original Land Cover Class", fontsize=12)
    plt.ylabel("Year After Land Cover Class", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('ChangeMatrix/ChangeMatrixSumNoRSC.png', dpi=300, bbox_inches='tight')

def plot_change_count():
    # Load the data
    df = pd.read_csv('Results/ChangeCount/ChangeCount20_25.csv', header=None, names=['Changes', 'Value'])
    df_no_rsc = pd.read_csv('Results/ChangeCount/ChangeCountNoRSC20_25.csv', header=None, names=['Changes', 'Value'])

    # Convert 'Changes' to string
    df['Changes'] = df['Changes'].astype(str)
    df_no_rsc['Changes'] = df_no_rsc['Changes'].astype(str)

    # Calculate percentages
    total_sum = df['Value'].sum()
    df['Percentage'] = (df['Value'] / total_sum) * 100

    total_sum_no_rsc = df_no_rsc['Value'].sum()
    df_no_rsc['Percentage'] = (df_no_rsc['Value'] / total_sum_no_rsc) * 100

    # Set the positions and width for the bars
    x = np.arange(len(df['Changes']))  # the label locations
    width = 0.39  # the width of the bars

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the bars
    bars1 = ax.bar(x - width/2, df['Percentage'], width, label='With RSC', color='#e49635')
    bars2 = ax.bar(x + width/2, df_no_rsc['Percentage'], width, label='Without RSC', color='#88b053')

    # Add labels and title
    ax.set_xlabel('No. of Classification Changes per Pixel from 2020 to 2025')
    ax.set_ylabel('Percentage of Pixels (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(df['Changes'])
    ax.legend()

    # Add bar labels
    ax.bar_label(bars1, fmt='%.2f%%', padding=5, size=12)
    ax.bar_label(bars2, fmt='%.2f%%', padding=5, size=12)

    # Adjust the y-axis limit
    ax.set_ylim(0, 100)

    # Save the plot
    plt.tight_layout()
    plt.savefig('change_count_comparison.png', dpi=300, bbox_inches='tight')

def plot_classifications_separate():
    df = pd.read_csv('Results/ClassificationsDAANoRSC20_25.csv', index_col=0)

    years = df.index.tolist()

    for year in years:
        row = df.loc[year]
        total_sum = row.values.sum()
        percentage = (row.values/total_sum) * 100
        bars = plt.bar(row.index, percentage, color='blue')
        plt.title(f'Land Cover Distribution - {year}', fontweight='bold')
        plt.ylabel('Percentage')
        plt.ylim(0, percentage.max() * 1.15)
        plt.bar_label(bars, fmt='%.2f%%', padding=3)
        plt.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig('classifications_daa_no_rsc'+ str(year) + '.png')
        plt.clf() 

def plot_classifications_comparison():
    df = pd.read_csv('Results/ClassificationsDAANoRSC20_25.csv', index_col=0)
    df_percent = df.div(df.sum(axis=1), axis=0) * 100

    ax = df_percent.T.plot(kind='bar', figsize=(16, 8), edgecolor='black', width=0.85)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3, fontsize=8, rotation=90)

    plt.title('Comparison of Land Cover Categories (2020-2025)')
    plt.ylabel('Value')
    plt.xlabel('Category')
    plt.xticks(rotation=45)
    plt.legend(title='Year')

    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust y-limit to provide space for vertical labels
    plt.ylim(0, df_percent.max().max() * 1.2)
    plt.tight_layout()
    plt.savefig('classifications_daa_comparison_no_rsc.png')

# Your provided color set
DW_CLASS = {
    'water': '#419bdf',
    'trees': '#397d49',
    'grass': '#88b053',
    'flooded_vegetation': '#7a87c6',
    'crops': '#e49635',
    'shrub_and_scrub': '#dfc35a',
    'built': '#c4281b',
    'bare': '#a59b8f',
    'snow_and_ice': '#b39fe1',
}

def plot_percentage_stacked_bar_custom():
    # Load and normalize data to percentages
    df = pd.read_csv('Results/ClassificationsDAA/ClassificationsDAANoRSC20_25.csv', index_col=0)
    df_perc = df.divide(df.sum(axis=1), axis=0) * 100
    
    # 2. Sort columns by their total sum across all years (descending)
    # The first item in this list will be the "biggest" and placed at the bottom.
    sorted_columns = df_perc.sum().sort_values(ascending=False).index.tolist()
    df_perc_sorted = df_perc[sorted_columns]
    
    # 3. Map colors to the new column order
    def format_key(name):
        return name.lower().replace(' & ', '_and_').replace(' ', '_')
    
    color_list = [DW_CLASS[format_key(col)] for col in sorted_columns]
    
    # 4. Create the plot
    ax = df_perc_sorted.plot(kind='bar', stacked=True, figsize=(14, 8), color=color_list, width=0.8)
    
    # 5. Add text labels
    for p in ax.patches:
        h = p.get_height()
        if h > 2.5:
            ax.text(p.get_x() + p.get_width()/2, p.get_y() + h/2, f'{h:.1f}%', 
                    ha='center', va='center', fontsize=12, color='white', fontweight='bold')

    # Formatting and Legend
    plt.ylabel('Percentage of DAA Area Per Class (%)')
    plt.xticks(rotation=0)
    plt.legend(title='', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('classifications_daa_comparison_no_rsc_stacked.png')

def calculate_land_dynamics(file_path):
    # Load the CSV, setting the first column as the index
    df = pd.read_csv(file_path, index_col=0)
    
    # Convert dataframe to a numpy matrix for easy math
    matrix = df.to_numpy()
    
    # 1. Total area represented in the matrix
    total_area = matrix.sum()
    
    # 2. Area that stayed the same (sum of the diagonal)
    stayed_same_area = np.trace(matrix)
    
    # 3. Area that changed (total minus diagonal)
    changed_area = total_area - stayed_same_area
    
    # Calculate percentages
    percent_stayed = (stayed_same_area / total_area) * 100
    percent_changed = (changed_area / total_area) * 100
    
    print("Stayed Same:" + str(stayed_same_area) + "Percentage Changed:" + str(changed_area))
    print("Percentage Stayed Same:" + str(round(percent_stayed, 2)) + "Percentage Changed:" + str(round(percent_changed, 2)))

def plot_rsc_changes():
    # Data from your table
    periods = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
    
    # Values scaled to Millions
    total_pre = np.array([67223154, 88837093, 85195804, 62425362, 85806833]) / 1e6
    rsc_counts = np.array([28416582, 47183936, 21401276, 22893903, 0]) / 1e6
    total_post = np.array([38806572, 19232937, 26587985, 25518499, 66320215]) / 1e6
    rsc_percents = [42, 53, 25, 37, 0] # From your % RSC column

    x = np.arange(len(periods))
    width = 0.30

    fig, ax = plt.subplots(figsize=(10, 7))

    # 1. Pre-Filter Bar: RSC on BOTTOM, Remainder on TOP
    remainder_pre = total_pre - rsc_counts
    bar_rsc = ax.bar(x - width/2, rsc_counts, width, label='RSC', color='#c4281b') # Red for noise
    bar_rem = ax.bar(x - width/2, remainder_pre, width, bottom=rsc_counts, 
                     label='Pre-Filter', color='#e49635')

    # 2. Post-Filter Bar
    bar_post = ax.bar(x + width/2, total_post, width, label='Post-Filter', color='#88b053')

    # Add Text: Values on top of bars
    for i in range(len(periods)):
        # Total Pre-filter value on top
        ax.text(x[i] - width/2, total_pre[i] + 1, f'{total_pre[i]:.1f}M', ha='center', fontweight='bold')
        # Total Post-filter value on top
        ax.text(x[i] + width/2, total_post[i] + 1, f'{total_post[i]:.1f}M', ha='center', fontweight='bold')
        
        # RSC Percentages inside the bottom segment
        if rsc_percents[i] > 0:
            ax.text(x[i] - width/2, rsc_counts[i]/2, f'{rsc_percents[i]}%', 
                    ha='center', va='center', color='white', fontweight='bold')

    # Formatting
    ax.set_ylabel('Total No. Pixels Changed')
    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    ax.set_ylim(0, max(total_pre) * 1.15) # Leave room for labels
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig('change_number.png')
    
plot_rsc_changes()