import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_change_matrix(year):
    df = pd.read_csv('Results/ChangeMatrix20_25.csv', index_col=0)

    df_percent = pd.DataFrame()
    row_sums = df.sum(axis=0)
    df_percent = df.div(row_sums, axis=1) * 100

    plt.figure(figsize=(12, 10))
    
    sns.heatmap(df_percent, 
                annot=df.values,
                fmt=".2f",
                cmap="Blues",
                vmin=0.0,
                vmax=100,
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

plot_change_matrix(21)