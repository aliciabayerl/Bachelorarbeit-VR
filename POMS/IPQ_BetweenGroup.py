import pandas as pd
import os
from scipy.stats import f_oneway, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scikit_posthocs import posthoc_dunn
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
folder_path = 'POMS'
mean_input_file = 'IPQ_scores.csv'
median_input_file = 'IPQ_scores_median.csv'
mean_file_path = os.path.join(folder_path, mean_input_file)
median_file_path = os.path.join(folder_path, median_input_file)
data_means = pd.read_csv(mean_file_path)
data_medians = pd.read_csv(median_file_path)

# Prepare data for ANOVA and Kruskal-Wallis Test
anova_results = {}
kruskal_results = {}
post_hoc_anova = {}
post_hoc_kruskal = {}

# Compute Overall Presence for both mean and median data
data_means['Overall_Presence'] = data_means[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)
data_medians['Overall_Presence'] = data_medians[['SP_median', 'INV_median', 'REAL_median']].median(axis=1)

# ANOVA on mean scores
for column in ['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']:
    groups_means = [group[column].dropna() for name, group in data_means.groupby('Condition')]
    anova_result = f_oneway(*groups_means)
    anova_results[column] = anova_result

    if anova_result.pvalue < 0.05:
        tukey = pairwise_tukeyhsd(endog=data_means[column], groups=data_means['Condition'], alpha=0.05)
        post_hoc_anova[column] = tukey.summary()

# Kruskal-Wallis on median scores
for column in ['SP_median', 'INV_median', 'REAL_median', 'Overall_Presence']:
    groups_medians = [group[column].dropna() for name, group in data_medians.groupby('Condition')]
    kruskal_result = kruskal(*groups_medians)
    kruskal_results[column] = kruskal_result

    if kruskal_result.pvalue < 0.05:
        dunn = posthoc_dunn(data_medians, val_col=column, group_col='Condition', p_adjust='bonferroni')
        post_hoc_kruskal[column] = dunn

# Display results
print("ANOVA Results:")
for key, result in anova_results.items():
    print(f"{key} - ANOVA: F={result.statistic:.2f}, p={result.pvalue:.4f}")
    if result.pvalue < 0.05:
        print("Tukey HSD Results for", key)
        print(post_hoc_anova[key])

print("\nKruskal-Wallis Test Results:")
for key, result in kruskal_results.items():
    print(f"{key} - Kruskal-Wallis: H={result.statistic:.2f}, p={result.pvalue:.4f}")
    if result.pvalue < 0.05:
        print("Dunn's Test Results for", key)
        print(post_hoc_kruskal[key])
