import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro

# Set folder path and file path for the data
folder_path = 'POMS'
file_path = f'{folder_path}/participant_scores_deq.csv'
data = pd.read_csv(file_path)

# Define mood states and calculate their change scores
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood in mood_states:
    data[f'Change_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Simulate sample means and apply the Shapiro-Wilk test for normality
def simulate_sample_means(data, column, sample_size, num_samples):
    np.random.seed(42)  # for reproducibility
    sample_means = []
    for _ in range(num_samples):
        sample = data[column].sample(sample_size, replace=True)
        sample_means.append(sample.mean())
    return sample_means

# Parameters for the simulation
sample_size = 30
num_samples = 1000

# Store results
results = {}

# Perform simulations and normality tests for each mood state
for mood in mood_states:
    column = f'Change_{mood}'
    sample_means = simulate_sample_means(data, column, sample_size, num_samples)
    stat, p_value = shapiro(sample_means)
    results[column] = {
        'Sample Means': sample_means,
        'Shapiro Stat': stat,
        'p-value': p_value
    }
    print(f'Shapiro-Wilk test statistic for {mood} : {stat}, p-value: {p_value}')

# Plot the distributions of sample means
fig, axs = plt.subplots(4, 2, figsize=(14, 20))
axs = axs.flatten()
for i, mood in enumerate(mood_states):
    axs[i].hist(results[f'Change_{mood}']['Sample Means'], bins=30, edgecolor='k', alpha=0.7)
    axs[i].set_title(f'Distribution of Sample Means for Change in {mood}')
    axs[i].set_xlabel('Sample Mean')
    axs[i].set_ylabel('Frequency')
    axs[i].grid(True)
    stat = results[f'Change_{mood}']['Shapiro Stat']
    p_val = results[f'Change_{mood}']['p-value']
    axs[i].annotate(f'Shapiro-Wilk: {stat:.2f}, p-value: {p_val:.4f}', xy=(0.5, 0.9), xycoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.show()
