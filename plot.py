import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_change_matrix(year):
    df = pd.read_csv('Results/ChangeMatrix' + str(year - 1) + '_' + str(year) + ".csv", index_col=0)

    df_percent = pd.DataFrame()
    row_sums = df.sum(axis=1)
    df_percent = df.div(row_sums, axis=0) * 100

    plt.figure(figsize=(12, 10))
    
    sns.heatmap(df_percent, 
                annot=df.values,
                fmt=".2f",
                cmap="Blues",
                vmin=0.0,
                vmax=100,
                cbar_kws={'label': 'Percentage Class Area Change'})
    
    plt.title("Land Cover Change Matrix from 20" + str(year - 1) + " to 20" + str(year), fontsize=15, pad=20)
    plt.xlabel("20" + str(year - 1) + " Land Cover Class", fontsize=12)
    plt.ylabel("20" + str(year) + " Land Cover Class", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('ChangeMatrix/ChangeMatrix' + str(year - 1) + '_' + str(year) + '.png', dpi=300, bbox_inches='tight')

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

plot_change_count()