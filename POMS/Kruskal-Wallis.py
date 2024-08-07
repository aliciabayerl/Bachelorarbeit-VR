import pandas as pd
import os
import pandas as pd
import os
from scipy.stats import shapiro, levene, kruskal
import matplotlib.pyplot as plt
import seaborn as sns
import scikit_posthocs as sp

# Load the data
folder_path = 'POMS'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Calculate change scores
mood_states = ['Tension', 'Depression', 'Anger_x', 'Vigor', 'Fatigue', 'Confusion']
for mood in mood_states:
    data[f'Change_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

change_scores = [f'Change_{mood}' for mood in mood_states]
groups = [data[data['Condition'] == i] for i in range(3)]

print("Kruskal-Wallis Test Results and Effect Sizes:")
for score in change_scores:
    stat, p_value = kruskal(*[group[score] for group in groups])
    n = len(data)
    k = len(groups)
    epsilon_squared = (stat - k + 1) / (n - k)
    print(f'{score}: Statistics={stat:.2f}, p-value={p_value:.4f}, Epsilon Squared={epsilon_squared:.4f}')
    
    if p_value < 0.05:
        print(f'There is a significant difference in {score} across the groups')
        
        # Perform Dunn's post-hoc test with Holm-Bonferroni correction
        dunn_results = sp.posthoc_dunn(data, val_col=score, group_col='Condition', p_adjust='holm')
        print("Dunn's Post-Hoc Test Results with Holm-Bonferroni Correction:")
        print(dunn_results)
        
        # Calculate effect size for Dunn's test pairwise comparisons
        print("Pairwise Effect Sizes (r):")
        for i in range(k):
            for j in range(i + 1, k):
                group_i = groups[i][score].dropna()
                group_j = groups[j][score].dropna()
                pooled_std = ((len(group_i) - 1) * group_i.std() ** 2 + (len(group_j) - 1) * group_j.std() ** 2) / (len(group_i) + len(group_j) - 2)
                pooled_std = pooled_std ** 0.5
                mean_diff = group_i.mean() - group_j.mean()
                r = mean_diff / pooled_std
                print(f'Condition {i} vs Condition {j}: r = {r:.4f}')
    else:
        print(f'There is no significant difference in {score} across the groups')
    print()
