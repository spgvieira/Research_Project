import pandas as pd
import glob

# 1. Get a list of all your transition CSV files
# Adjust the pattern if your files have a specific naming convention (e.g., 'transition_*.csv')
file_list = glob.glob("Results/ChangeMatrix2*.csv")

# 2. Load and sum the dataframes
# We use index_col=0 because the first column contains the 'From' class names
dfs = [pd.read_csv(f, index_col=0) for f in file_list]
combined_df = sum(dfs)

# 3. Reshape the data to find the most common transitions
# This converts the matrix into a list of: [Source Class, Target Class, Total Count]
melted = combined_df.stack().reset_index()
melted.columns = ['From_Class', 'To_Class', 'Total_Count']

# 4. Identify most common transitions (excluding self-transitions/stability)
# We filter out cases where 'From' is the same as 'To' to see actual changes
changes_only = melted[melted['From_Class'] != melted['To_Class']]
top_changes = changes_only.sort_values(by='Total_Count', ascending=False)

# 5. Identify the most common stability (staying the same class)
stability = melted[melted['From_Class'] == melted['To_Class']]
top_stability = stability.sort_values(by='Total_Count', ascending=False)

# Output results
print("--- Top 15 Most Common Transitions (Changes) ---")
print(top_changes.head(15))

print("\n--- Top 15 Most Common Stability (No Change) ---")
print(top_stability.head(15))

# Optional: Save the combined matrix to a new file
combined_df.to_csv("summed_transitions.csv")