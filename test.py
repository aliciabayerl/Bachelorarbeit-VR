import pandas as pd
import os

# Read the data into a DataFrame
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
df = pd.read_csv(file_path)

# For each mood state, calculate the change, median change, and IQR across conditions
mood_states = ["Anger", "Disgust", "Fear", "Anxiety", "Sadness", "Desire", "Relaxation", "Happiness"]
results = []

for mood in mood_states:
    for condition in [0, 1, 2]:  
        condition_data = df[df["Condition"] == condition]
        changes = condition_data[f"After {mood}"] - condition_data[f"Before {mood}"]
        median_change = changes.median()
        iqr_change = changes.quantile(0.75) - changes.quantile(0.25)
        results.append((mood, condition, median_change, iqr_change))

# Convert results to DataFrame
results_df = pd.DataFrame(results, columns=["Mood State", "Condition", "Median Change", "IQR Change"])

# Sort the DataFrame by the 'Condition' column
results_df = results_df.sort_values(by="Condition")

# Print the sorted DataFrame
print(results_df)
