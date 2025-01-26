import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

column_headers = [
    'index', 'counter', 'instance', 'satisfiability', 'problem_type',
    'est_type', 'est_val', 'counter_type', 'count_precision', 'count_notation',
    'count_value', 'timed_out', 'error', 'generator', 'verified', 'elapsed_time'
]

df_bb = pd.read_csv("experiment1_results_bb.csv", header=0, names=column_headers)
df_bb_filtered = df_bb[~df_bb['counter'].str.contains('SharpSAT', na=False)]


df_custom_bonus = pd.read_csv("experiment1_results_custom_bonus.csv", header=0, names=column_headers)
df_custom = pd.read_csv("experiment1_results_custom.csv", header=0, names=column_headers)

rows = ['gpmc', 'ganak-conf-1', 'ganak-conf-2', 'SharpSAT-TD-weighted', 'SharpSATTD-CH-weighted']
columns = ['Timeout', 'Wsat', 'Wsum']
count_table = pd.DataFrame(0, index=rows, columns=columns)

grouped_bb = df_bb_filtered.groupby('instance')
grouped_custom = df_custom.groupby('instance')
grouped_custom_bonus = df_custom_bonus.groupby('instance')

for table in [grouped_bb, grouped_custom, grouped_custom_bonus]:
    for instance, group in table:
        # Timeout
        for counter in group['counter'].unique():
            if group[group['counter'] == counter]['timed_out'].any():
                count_table.at[counter, 'Timeout'] += 1

        # Wsat
        satisfiability_counts = group['satisfiability'].value_counts()
        if 'SATISFIABLE' in satisfiability_counts and 'UNSATISFIABLE' in satisfiability_counts:
            minority_value = 'SATISFIABLE' if satisfiability_counts['SATISFIABLE'] < satisfiability_counts[
                'UNSATISFIABLE'] else 'UNSATISFIABLE'

            for counter in group['counter'].unique():
                if group[group['counter'] == counter]['satisfiability'].iloc[0] == minority_value:
                    count_table.at[counter, 'Wsat'] += 1

        # Wsum
        if ((group['est_val'] == -np.inf) & (group['satisfiability'] == "SATISFIABLE")).any():
            for counter in group['counter'].unique():
                count_table.at[counter, 'Wsum'] += 1

    print(count_table)
    count_table = pd.DataFrame(0, index=rows, columns=columns)

df_bb_filtered = df_bb_filtered[df_bb_filtered['timed_out'] != True]
df_custom = df_custom[df_custom['timed_out'] != True]
df_custom_bonus = df_custom_bonus[df_custom_bonus['timed_out'] != True]

updates = {
    "EXTREMEgen_TREE_set1": "EXTREMEgen_TREE_set2",
    "EXTREMEgen_GRID_set1": "EXTREMEgen_GRID_set2",
    "EXTREMEgen_DQMR_set1": "EXTREMEgen_DQMR_set2"
}

df_custom_bonus['generator'] = df_custom_bonus['generator'].replace(updates)
combined_df = pd.concat([df_bb_filtered, df_custom_bonus], axis=0)
combined_df.reset_index(drop=True, inplace=True)

combined_df['instance_count'] = combined_df.groupby(['generator', 'counter'])['instance'].transform('nunique')
total_elapsed_time = combined_df.groupby(['generator', 'counter'])['elapsed_time'].sum().reset_index()
instance_counts = combined_df[['generator', 'counter', 'instance_count']].drop_duplicates()
total_elapsed_time = total_elapsed_time.merge(instance_counts, on=['generator', 'counter'], how='left')
total_elapsed_time['normalized_elapsed_time'] = total_elapsed_time['elapsed_time'] / total_elapsed_time['instance_count']

plt.figure(figsize=(10, 6))
sns.barplot(data=total_elapsed_time, x='counter', y='normalized_elapsed_time', palette='')
plt.title('Average Time to Solve Instances per Counter and Generator')
plt.xlabel('Counter')
plt.ylabel('Average Elapsed Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
