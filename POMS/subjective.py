import pandas as pd
import os

# Load the CSV file
folder_path = 'POMS'  # Specify the folder path where the CSV file is located
input_file = 'questionnaire_with_scores.csv'  # Name of the CSV file containing the questionnaire data
file_path = os.path.join(folder_path, input_file)  # Combine folder path and file name to get the full file path
df = pd.read_csv(file_path)  # Load the CSV file into a pandas DataFrame for analysis

# Convert Yes/No answers to lowercase for consistency
df.replace({'Yes': 'yes', 'No': 'no'}, inplace=True)

# Questions with Yes/No responses
yes_no_questions = [
    'Is walking in nature in real life relaxing for you?',
    'Did you perceive the audio as calming?',
    'Did you feel like the audio had an impact on your emotions?',
    'Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?',
    'Did you notice any major technical issues during the virtual reality experience?'
]

# Calculate and print the percentage of "Yes" responses for Yes/No questions
print("Yes/No Questions:")
for question in yes_no_questions:
    yes_count = df[question].str.lower().value_counts().get('yes', 0)
    total_responses = len(df[question].dropna())  # Exclude NaN values from total responses
    percent_yes = (yes_count / total_responses) * 100
    print(f"Question: '{question}'")
    print(f"Number of 'Yes' Responses (yes_count): {yes_count}")
    print(f"Total Number of Responses (n): {total_responses}")
    print(f"Percentage of 'Yes' Responses: {percent_yes:.2f}%")
    print()

# Statements for participant agreement (percent agreeing)
statements = [
    'I felt like I could momentarily set aside my recent stresses during the VR intervention.',
    'I feel more optimistic towards my future.',
    'My general mood has improved.'
]

# Calculate and print the percentage of participants agreeing with each statement
print("Agreement Statements:")
for statement in statements:
    yes_count = df['Please tick the following statements that you agree with:'].str.contains(statement, case=False).sum()
    total_responses = len(df['Please tick the following statements that you agree with:'].dropna())  # Exclude NaN values
    percent_agree = (yes_count / total_responses) * 100
    print(f"Statement: '{statement}'")
    print(f"Number of 'Agree' Responses (yes_count): {yes_count}")
    print(f"Total Number of Responses (n): {total_responses}")
    print(f"Percentage of Agreement: {percent_agree:.2f}%")
    print()

# Questions with 1-5 scale responses (analyze average score)
scale_questions = [
    'Please indicate the positivity of this effect.',
    'Please indicate how much this affected your overall experience.',
    'Please indicate how much this affected your overall experience..1',
    'How open are you to using virtual reality as a tool for relaxation or stress reduction in the future?'
]

# Convert the relevant columns to numeric (1-5 scale)
df[scale_questions] = df[scale_questions].apply(pd.to_numeric, errors='coerce')

# Calculate and print the average response for 1-5 scale questions
print("Scale Questions:")
for question in scale_questions:
    average_score = df[question].mean()
    num_responses = df[question].notna().sum()  # Count the number of valid (non-NaN) responses
    print(f"Question: '{question}'")
    print(f"Average Score: {average_score:.2f}")
    print(f"Number of Responses (n): {num_responses}")
    print()

# Filter the data to include only rows where Condition_x is 1 or 2
filtered_df = df[df['Condition_x'].isin([1, 2])]

# Calculate the number and percentage of participants who perceived the audio as calming, by condition
calming_condition_1 = filtered_df[filtered_df['Condition_x'] == 1]['Did you perceive the audio as calming?'].str.lower().value_counts().get('yes', 0)
calming_condition_2 = filtered_df[filtered_df['Condition_x'] == 2]['Did you perceive the audio as calming?'].str.lower().value_counts().get('yes', 0)
total_condition_1 = len(filtered_df[filtered_df['Condition_x'] == 1])
total_condition_2 = len(filtered_df[filtered_df['Condition_x'] == 2])
percent_calming_condition_1 = (calming_condition_1 / total_condition_1) * 100 if total_condition_1 > 0 else 0
percent_calming_condition_2 = (calming_condition_2 / total_condition_2) * 100 if total_condition_2 > 0 else 0

# Calculate the average score for the positivity of the effect of audio, by condition
average_positivity_condition_1 = filtered_df[filtered_df['Condition_x'] == 1]['Please indicate the positivity of this effect.'].mean()
average_positivity_condition_2 = filtered_df[filtered_df['Condition_x'] == 2]['Please indicate the positivity of this effect.'].mean()

# Output the results for each condition
print("Audio Calming Perception by Condition:")
print(f"Condition 1: Number of 'Yes' Responses: {calming_condition_1}, Percentage: {percent_calming_condition_1:.2f}%")
print(f"Condition 2: Number of 'Yes' Responses: {calming_condition_2}, Percentage: {percent_calming_condition_2:.2f}%")
print()

print("Average Positivity of Audio's Effect by Condition:")
print(f"Condition 1: Average Score: {average_positivity_condition_1:.2f}")
print(f"Condition 2: Average Score: {average_positivity_condition_2:.2f}")
