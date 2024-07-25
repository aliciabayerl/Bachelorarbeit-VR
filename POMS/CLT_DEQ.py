import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro
import scipy.stats as stats


# Set folder path and file path for the data
folder_path = 'POMS'
file_path = f'{folder_path}/participant_scores.csv'
data = pd.read_csv(file_path)

# Define mood states and calculate their change scores
mood_states = ['Anger_x', 'Fatigue', 'Tension', 'Vigor', 'Depression']
for mood in mood_states:
    data[f'Change_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Number of resamples
n_resamples = 5000
sample_size = len(data)

# Initialize dictionary to store resample means
resample_means_dict = {}

# Generate resamples and calculate means for each mood state
for mood in mood_states:
    resample_means = [np.mean(np.random.choice(data[f'Change_{mood}'], size=sample_size, replace=True)) for _ in range(n_resamples)]
    resample_means_dict[mood] = np.array(resample_means)

    # Plot histogram of the resample means
    plt.hist(resample_means, bins=30, density=True, alpha=0.6, color='g')

    # Fit a normal distribution to the data and plot it
    mu, std = stats.norm.fit(resample_means)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    plt.title(f"Histogram of Resample Means for {mood} with Normal Fit")
    plt.xlabel('Resample Means')
    plt.ylabel('Density')
    plt.show()

    # Perform Shapiro-Wilk test on the distribution of sample means
    shapiro_stat, shapiro_p_value = shapiro(resample_means)
    print(f'Shapiro-Wilk test for {mood}: statistic={shapiro_stat}, p-value={shapiro_p_value}')

    # Interpret the result
    if shapiro_p_value > 0.05:
        print(f"The distribution of sample means for {mood} approximates normality (fail to reject H0).")
    else:
        print(f"The distribution of sample means for {mood} does not approximate normality (reject H0).")