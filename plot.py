import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_change_matrix(year):
    # Load data
    df = pd.read_csv('Results/ChangeMatrix20_25.csv', index_col=0)

    # Calculate percentages based on columns (initial year)
    row_sums = df.sum(axis=0)
    df_percent = df.div(row_sums, axis=1) * 100

    # Create custom labels: "Raw Value \n (Percentage%)"
    # We use a nested list comprehension to format each cell
    labels = np.array([
        [f"{val:.2f}\n({pct:.1f}%)" for val, pct in zip(row_val, row_pct)]
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
    
    plt.title("Land Cover Change Matrix from 2020 to 2025", fontsize=15, pad=20)
    plt.xlabel("2020 Land Cover Class", fontsize=12)
    plt.ylabel("2025 Land Cover Class", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('ChangeMatrix/ChangeMatrix20_25.png', dpi=300, bbox_inches='tight')

def plot_change_count():
    df = pd.read_csv('Results/ChangeCountNoRSC20_25.csv', header=None, names=['Changes', 'Value'])

    df['Changes'] = df['Changes'].astype(str)
    total_sum = df['Value'].sum()
    print(total_sum)
    df['Percentage'] = (df['Value'] / total_sum) * 100

    bars = plt.bar(df['Changes'], df['Percentage'], color='blue')

    plt.bar_label(bars, fmt='%.2f%%', padding=3)

    plt.xlabel('No. of Changes')
    plt.ylabel('Percentage (%)')
    plt.title('Bar Plot from CSV Data')

    plt.ylim(0, df['Percentage'].max() * 1.15)

    plt.tight_layout()
    plt.savefig('change_count_no_rsc.png')

def plot_classifications_separate():
    df = pd.read_csv('Results/ClassificationsDAA20_25.csv', index_col=0)

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
        plt.savefig('classifications_daa'+ str(year) + '.png')
        plt.clf() 

def plot_classifications_comparison():
    df = pd.read_csv('Results/ClassificationsDAA20_25.csv', index_col=0)
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
    plt.savefig('classifications_daa_comparison.png')

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
    df = pd.read_csv('Results/ClassificationsDAA20_25.csv', index_col=0)
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
                    ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # Formatting and Legend
    plt.title('Annual Classifications from Dynamic World', fontsize=16)
    plt.ylabel('Percentage (%)')
    plt.xticks(rotation=0)
    plt.legend(title='', bbox_to_anchor=(1.02, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('classifications_daa_comparison_stacked.png')

plot_change_matrix(22)