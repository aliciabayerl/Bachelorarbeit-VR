import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the data
folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Calculate change for each mood state
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood in mood_states:
    data[f'Change_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Prepare the figure layout
fig, axes = plt.subplots(3, 3, figsize=(15, 20))  # Adjust the subplot layout dimensions based on your number of plots
axes = axes.flatten()

# Define a color palette (you can choose different shades of blue)
palette = ["#abd9e9", "#74add1", "#4575b4"]

# Create a box plot for each mood state
for i, mood in enumerate(mood_states):
    sns.boxplot(x='Condition', y=f'Change_{mood}', data=data, ax=axes[i], palette=palette)

    axes[i].set_title(f'Change in {mood} by Condition')
    axes[i].set_xlabel('Condition')
    axes[i].set_ylabel(f'Change in {mood}')

# Remove unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

image_path = 'POMS/Plot_Images'
output_image = os.path.join(image_path, 'DEQ_Boxplot')
plt.tight_layout()
plt.savefig(output_image)
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))




