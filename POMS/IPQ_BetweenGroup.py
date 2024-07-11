import pandas as pd
import os
from scipy.stats import f_oneway, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scikit_posthocs import posthoc_dunn
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
folder_path = 'POMS'
input_file = 'IPQ_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Prepare data for ANOVA and Kruskal-Wallis Test
grouped_data = data.groupby('Condition')

# Perform ANOVA and Kruskal-Wallis Test for each IPQ component
anova_results = {}
kruskal_results = {}
post_hoc_anova = {}
post_hoc_kruskal = {}

data['Overall_Presence'] = data[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

for column in ['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']:
    groups = [group[column].dropna() for name, group in grouped_data]
    anova_result = f_oneway(*groups)
    kruskal_result = kruskal(*groups)
    anova_results[column] = anova_result
    kruskal_results[column] = kruskal_result
    
    # Calculate effect size for ANOVA (Eta squared)
    if anova_result.pvalue < 0.05:
        eta_squared = anova_result.statistic * sum(groups) / (anova_result.statistic * sum(groups) + (len(data) - len(groups)))
        tukey = pairwise_tukeyhsd(endog=data[column], groups=data['Condition'], alpha=0.05)
        post_hoc_anova[column] = tukey.summary()
        print(f"Effect Size (η²) for {column}: {eta_squared:.4f}")
    
    # Calculate effect size for Kruskal-Wallis (Epsilon squared)
    if kruskal_result.pvalue < 0.05:
        epsilon_squared = kruskal_result.statistic / (len(data) - 1)
        dunn = posthoc_dunn(data, val_col=column, group_col='Condition', p_adjust='bonferroni')
        post_hoc_kruskal[column] = dunn
        print(f"Effect Size (ε²) for {column}: {epsilon_squared:.4f}")

# Display results
print("ANOVA Results:")
for key, result in anova_results.items():
    print(f"{key}: F-statistic = {result.statistic:.2f}, p-value = {result.pvalue:.4f}")
    if result.pvalue < 0.05:
        print("Tukey HSD Results:")
        print(post_hoc_anova[key])

print("\nKruskal-Wallis Test Results:")
for key, result in kruskal_results.items():
    print(f"{key}: H-statistic = {result.statistic:.2f}, p-value = {result.pvalue:.4f}")
    if result.pvalue < 0.05:
        print("Dunn's Test Results:")
        print(post_hoc_kruskal[key])
