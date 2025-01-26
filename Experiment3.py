import matplotlib.pyplot as plt
import seaborn as sns

generators = [
    "EXTREMEgen_DQMR_set2",
    "EXTREMEgen_GRID_set2",
    "EXTREMEgen_TREE_set2",
    "biere-mc",
    "brummayer-mc"
]

user_sys_times = [
    9 * 60 + 34.524 + 19 * 60 + 3.621,  # generator_1000_DQMR.json
    9 * 60 + 39.677 + 18 * 60 + 58.386,  # generator_1000_GRID.json
    9 * 60 + 0.039 + 18 * 60 + 55.316,   # generator_1000_TREE.json
    1.942 + 1.302,                       # generator_1000_biere.json
    20.708 + 4.989                       # generator_1000_brummayer.json
]

import pandas as pd
df = pd.DataFrame({
    'generator': generators,
    'User + Sys Time (seconds)': user_sys_times
})

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(x='generator', y='User + Sys Time (seconds)', data=df, palette=sns.color_palette("tab10"))
plt.xlabel('Generator')
plt.ylabel('User + Sys Time (seconds)')
plt.title('Time to Generate 1000 Instances per Generator')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
