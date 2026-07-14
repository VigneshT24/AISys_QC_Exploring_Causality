import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
When you run this file, it will give you 20 different matplotlib visual charts: either [box plots] or [line plots with confidence intervals].

This data is from the 'experiment_results.csv' file, which contains 12672 datas. Most of the generated charts (except some)
are the result of averaging the results of the data from 'experiment_results.csv'. The other charts use the raw data.
"""

df = pd.read_csv('experiment_results.csv', dtype={'top_state': str})
df['two_qubit_ratio'] = (df['count_2q'] / (df['count_1q'] + df['count_2q'])).round(2)

# averaging the results after 'repeat' for more normalized data result
grouping_cols = ['circuit_name', 'shots', 'optimization_level', 'noise_rate', 
                  'num_qubits', 'depth_config']

df_averaged = df.groupby(grouping_cols, as_index=False)['tvd'].mean()

sns.set_style('whitegrid')

# circuits that actually vary qubit count (Bell circuit qubit count is fixed)
QUBIT_VARYING = ['GHZ', 'Parameterized', 'Grover', 'Variable Depth']


def clean_lineplot_multi(data, x, y, hue, title, xlabel, ylabel, palette=None):
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

# Chart 1
clean_lineplot_multi(
    df, x='noise_rate', y='tvd', hue='circuit_name',
    title='TVD by Noise Rate, All Circuits',
    xlabel='Noise Rate', ylabel='TVD'
)

# Chart 2
clean_lineplot_multi(
    df, x='optimization_level', y='tvd', hue='circuit_name',
    title='TVD by Optimization Level, All Circuits',
    xlabel='Optimization Level', ylabel='TVD'
)

# Chart 3
clean_lineplot_multi(
    df, x='shots', y='tvd', hue='circuit_name',
    title='TVD Stability by Shot Count, All Circuits',
    xlabel='Number of Shots', ylabel='TVD'
)

# Chart 4
clean_lineplot_multi(
    df, x='optimization_level', y='depth', hue='circuit_name',
    title='Transpiled Depth by Optimization Level, All Circuits',
    xlabel='Optimization Level', ylabel='Transpiled Depth'
)

# Chart 5
qubit_df = df[df['circuit_name'].isin(QUBIT_VARYING)]
clean_lineplot_multi(
    qubit_df, x='num_qubits', y='tvd', hue='circuit_name',
    title='TVD by Number of Qubits (All Circuits Except Bell)',
    xlabel='Number of Qubits', ylabel='TVD'
)


# Chart 6
qubit_df = df[df['circuit_name'].isin(QUBIT_VARYING)]

plt.figure(figsize=(9, 5.5))
ax = sns.lineplot(data=qubit_df, x='num_qubits', y='count_2q', hue='circuit_name',
                  marker='o', errorbar='ci', linewidth=2.5, markersize=8)

ax.lines[0].set_linewidth(5)
ax.lines[0].set_markersize(14)
ax.lines[0].set_linestyle('dashdot')

plt.title('Two-Qubit Gate Count by Number of Qubits (All Circuits Except Bell)')
plt.xlabel('Number of Qubits')
plt.ylabel('Count of 2-Qubit Gates')
plt.legend(title=None, fontsize=9)
plt.tight_layout()
plt.show()


# Chart 7
clean_lineplot_multi(
    df, x='optimization_level', y='count_2q', hue='circuit_name',
    title='Two-Qubit Gate Count by Optimization Level, All Circuits',
    xlabel='Optimization Level', ylabel='Count of 2-Qubit Gates'
)

# Chart 8
clean_lineplot_multi(
    qubit_df, x='num_qubits', y='runtime', hue='circuit_name',
    title='Runtime by Number of Qubits (All Circuits Except Bell)',
    xlabel='Number of Qubits', ylabel='Runtime (seconds)'
)

# Chart 9
qubit_df = df[df['circuit_name'].isin(QUBIT_VARYING)]

plt.figure(figsize=(9, 5.5))
ax = sns.lineplot(data=qubit_df, x='num_qubits', y='depth', hue='circuit_name',
                  marker='o', errorbar='ci', linewidth=2.5, markersize=8)

ax.lines[0].set_linewidth(6)
ax.lines[0].set_markersize(12)
ax.lines[0].set_linestyle('dashdot')

plt.title('Transpiled Depth by Number of Qubits (All Circuits Except Bell)')
plt.xlabel('Number of Qubits')
plt.ylabel('Transpiled Depth')
plt.legend(title=None, fontsize=9)
plt.tight_layout()
plt.show()


# Chart 10
clean_lineplot_single(
    df, x='depth', y='tvd',
    title='TVD by Transpiled Depth, All Circuits',
    xlabel='Transpiled Depth', ylabel='TVD'
)

# Chart 11
clean_lineplot_single(
    df, x='depth', y='runtime',
    title='Runtime by Transpiled Depth, All Circuits',
    xlabel='Transpiled Depth', ylabel='Runtime (seconds)'
)

# Chart 12
grover_df = df[df['circuit_name'] == 'Grover']
clean_lineplot_single(
    grover_df, x='depth', y='success_probability',
    title='Grover: Success Probability by Transpiled Depth',
    xlabel='Transpiled Depth', ylabel='Success Probability'
)

# Chart 13
clean_lineplot_single(
    df, x='count_2q', y='tvd',
    title='TVD by Two-Qubit Gate Count, All Circuits',
    xlabel='Count of 2-Qubit Gates', ylabel='TVD'
)

# Chart 14
clean_lineplot_single(
    df, x='count_2q', y='runtime',
    title='Runtime by Two-Qubit Gate Count, All Circuits',
    xlabel='Count of 2-Qubit Gates', ylabel='Runtime (seconds)'
)

# Chart 15
clean_lineplot_single(
    grover_df, x='count_2q', y='success_probability',
    title='Grover: Success Probability by Two-Qubit Gate Count',
    xlabel='Count of 2-Qubit Gates', ylabel='Success Probability'
)

# Chart 16
plt.figure(figsize=(9, 5.5))
sns.boxplot(data=df, x='circuit_name', y='runtime')
plt.title('Runtime Distribution by Circuit Type, All Circuits')
plt.xlabel('Circuit')
plt.ylabel('Runtime (seconds)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()


# Chart 17
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


# Chart 18
grover_df = df[df['circuit_name'] == 'Grover']
clean_boxplot_single(
    grover_df, x='noise_rate', y='success_probability',
    title='Grover: Success Probability by Noise Rate',
    xlabel='Noise Rate', ylabel='Success Probability'
)

# Chart 19
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

# Chart 20
grover_df = df[df['circuit_name'] == 'Grover']
clean_boxplot_multi(
    grover_df, x='noise_rate', y='success_probability', hue='optimization_level',
    title='Grover: Success Probability by Noise Rate, per Optimization Level',
    xlabel='Noise Rate', ylabel='Success Probability',
    palette='viridis'
)