import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
When you run this file, it will give you 12 different matplotlib visual charts: either [box plots] or [line plots with confidence intervals].

This data is from the 'experiment_results.csv' file, which contains ~12000 data. Most of the generated charts (except some)
are the result of averaging the results of the data from 'experiment_results.csv'. The other charts use the raw data.
"""


df = pd.read_csv('experiment_results.csv')

# print(df['num_qubits'].min(), df['num_qubits'].max())
# print(df['depth'].min(), df['depth'].max())
# print(df['count_2q'].min(), df['count_2q'].max())

# df['depth_bin'] = pd.cut(df['depth'], bins=5)
# df['count_2q_bin'] = pd.cut(df['count_2q'], bins=5)

# grouped = df.groupby(['depth_bin', 'count_2q_bin', 'num_qubits'])['tvd'].mean()
# print(grouped)

df = pd.read_csv('experiment_results.csv', dtype={'top_state': str})
df['two_qubit_ratio'] = (df['count_2q'] / (df['count_1q'] + df['count_2q'])).round(2)

# averaging the results after 'repeat' for more normalized data result
grouping_cols = ['circuit_name', 'shots', 'optimization_level', 'noise_rate', 
                  'n_qubits_config', 'depth_config']

df_averaged = df.groupby(grouping_cols, as_index=False)['tvd'].mean()

sns.set_style('whitegrid')

# circuits that actually vary qubit count (Bell and Variable Depth are fixed)
QUBIT_VARYING = ['GHZ', 'Parameterized', 'Grover']


# ONLY UNCOMMENT OUT TO CHECK VALUE DISTRIBUTION AMONGST 5 CIRCUITS
# print(df['circuit_name'].value_counts())

def clean_lineplot_multi(data, x, y, hue, title, xlabel, ylabel, palette=None):
    """One line per hue category, each with its own shaded 95% CI band."""
    plt.figure(figsize=(9, 5.5))
    sns.lineplot(data=data, x=x, y=y, hue=hue, marker='o',
                 errorbar='ci', linewidth=2.5, markersize=8,
                 palette=palette)
    plt.title(title, fontsize=13)
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.legend(title=None, fontsize=9, loc='upper left', bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.show()


def clean_lineplot_single(data, x, y, title, xlabel, ylabel, color='#4472C4'):
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=data, x=x, y=y, color=color, marker='o',
                 errorbar='ci', linewidth=2)
    plt.title(title, fontsize=13)
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.tight_layout()
    plt.show()


def clean_boxplot_multi(data, x, y, hue, title, xlabel, ylabel):
    """Grouped box plot, one color group per hue category."""
    plt.figure(figsize=(10, 5.5))
    sns.boxplot(data=data, x=x, y=y, hue=hue)
    plt.title(title, fontsize=13)
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.legend(title=None, fontsize=9, loc='best')
    plt.tight_layout()
    plt.show()


def clean_boxplot_single(data, x, y, title, xlabel, ylabel, color='#4472C4'):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=data, x=x, y=y, color=color)
    plt.title(title, fontsize=13)
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.tight_layout()
    plt.show()


clean_lineplot_multi(
    df, x='noise_rate', y='tvd', hue='circuit_name',
    title='TVD by Noise Rate, All Circuits',
    xlabel='Noise Rate', ylabel='TVD'
)


clean_lineplot_multi(
    df, x='optimization_level', y='tvd', hue='circuit_name',
    title='TVD by Optimization Level, All Circuits',
    xlabel='Optimization Level', ylabel='TVD'
)


clean_lineplot_multi(
    df, x='shots', y='tvd', hue='circuit_name',
    title='TVD Stability by Shot Count, All Circuits',
    xlabel='Number of Shots', ylabel='TVD'
)


clean_lineplot_multi(
    df, x='optimization_level', y='depth', hue='circuit_name',
    title='Transpiled Depth by Optimization Level, All Circuits',
    xlabel='Optimization Level', ylabel='Transpiled Depth'
)

qubit_df = df[df['circuit_name'].isin(QUBIT_VARYING)]
clean_lineplot_multi(
    qubit_df, x='num_qubits', y='tvd', hue='circuit_name',
    title='TVD by Number of Qubits (GHZ, Parameterized, Grover)',
    xlabel='Number of Qubits', ylabel='TVD'
)

qubit_df = df[df['circuit_name'].isin(['GHZ', 'Parameterized', 'Grover'])]
clean_lineplot_multi(
    qubit_df, x='num_qubits', y='count_2q', hue='circuit_name',
    title='Two-Qubit Gate Count by Number of Qubits',
    xlabel='Number of Qubits', ylabel='Count of 2-Qubit Gates'
)

clean_lineplot_multi(
    df, x='optimization_level', y='count_2q', hue='circuit_name',
    title='Two-Qubit Gate Count by Optimization Level, All Circuits',
    xlabel='Optimization Level', ylabel='Count of 2-Qubit Gates'
)

clean_lineplot_multi(
    qubit_df, x='num_qubits', y='runtime', hue='circuit_name',
    title='Runtime by Number of Qubits (GHZ, Parameterized, Grover)',
    xlabel='Number of Qubits', ylabel='Runtime (seconds)'
)

plt.figure(figsize=(9, 5.5))
sns.boxplot(data=df, x='circuit_name', y='runtime')
plt.title('Runtime Distribution by Circuit Type, All Circuits')
plt.xlabel('Circuit')
plt.ylabel('Runtime (seconds)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()


def noise_bucket(n):
    if n <= 0.001:
        return 'Low (≤0.001)'
    elif n <= 0.01:
        return 'Medium (0.005-0.01)'
    else:
        return 'High (≥0.03)'

depth_df = df[df['circuit_name'] == 'Variable Depth'].copy()
depth_df['noise_bucket'] = depth_df['noise_rate'].apply(noise_bucket)

bucket_order = ['Low (≤0.001)', 'Medium (0.005-0.01)', 'High (≥0.03)']

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

for ax, bucket in zip(axes, bucket_order):
    subset = depth_df[depth_df['noise_bucket'] == bucket]
    sns.lineplot(data=subset, x='depth_config', y='tvd',
                 marker='o', errorbar='ci', linewidth=2,
                 color='#4472C4', ax=ax)
    ax.set_title(bucket, fontsize=12)
    ax.set_xlabel('Circuit Depth', fontsize=10)
    ax.set_ylabel('TVD' if bucket == bucket_order[0] else '')

fig.suptitle('Variable Depth: TVD vs Circuit Depth, by Noise Level', fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.80])
plt.show()


grover_df = df[df['circuit_name'] == 'Grover']
clean_boxplot_single(
    grover_df, x='noise_rate', y='success_probability',
    title='Grover: Success Probability by Noise Rate',
    xlabel='Noise Rate', ylabel='Success Probability'
)


clean_boxplot_multi(
    df, x='noise_rate', y='tvd', hue='circuit_name',
    title='TVD Distribution by Noise Rate, All Circuits',
    xlabel='Noise Rate', ylabel='TVD'
)

def clean_boxplot_multi(data, x, y, hue, title, xlabel, ylabel, palette=None):
    """Grouped box plot, one color group per hue category."""
    plt.figure(figsize=(10, 5.5))
    sns.boxplot(data=data, x=x, y=y, hue=hue, palette=palette)
    plt.title(title, fontsize=13)
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.legend(title='Optimization Level', fontsize=9, loc='best')
    plt.tight_layout()
    plt.show()

grover_df = df[df['circuit_name'] == 'Grover']
clean_boxplot_multi(
    grover_df, x='noise_rate', y='success_probability', hue='optimization_level',
    title='Grover: Success Probability by Noise Rate, per Optimization Level',
    xlabel='Noise Rate', ylabel='Success Probability',
    palette='viridis'
)