import pandas as pd

# Define the conversion function for POMS values
def convert_poms_values(value):
    if value == "Not at all":
        return 0
    elif value == "A little":
        return 1
    elif value == "Moderately":
        return 2
    elif value == "Quite a bit":
        return 3
    elif value == "Extremely":
        return 4
    else:
        return value  # Return the original value if it doesn't match any of the specified strings

# Function to convert POMS columns in the DataFrame
def convert_poms_columns(df):
    for column in df.columns:
        if "POMS Before >>" in column or "POMS After >>" in column:
            df[column] = df[column].apply(convert_poms_values)
    return df

# Function to calculate POMS scores for each participant
def calculate_poms_scores(df):
    # Define mood states corresponding to each score
    score_mappings = {
        'Tension': ['Panicky', 'Anxious', 'Nervous'],
        'Vigor': ['Lively', 'Energetic', 'Active', 'Alert'],
        'Confusion': ['Confused', 'Mixed up', 'Muddled', 'Uncertain'],
        'Fatigue': ['Worn out', 'Exhausted', 'Sleepy', 'Tired'],
        'Depression': ['Depressed', 'Downhearted', 'Unhappy', 'Miserable']
    }
    
    # Create a new DataFrame to store before and after POMS scores for each participant
    participant_scores = pd.DataFrame(columns=['Participant', 'Condition', 'Before Tension', 'After Tension', 'Before Vigor', 'After Vigor',
                                               'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue',
                                               'Before Depression', 'After Depression'])
    
    # Iterate over each participant
    for index, participant in df.iterrows():
        # Initialize scores for before and after for the participant
        participant_scores.loc[index] = [index + 1, participant['Condition']] + [0] * 10
        
        # Calculate before and after POMS scores for the participant
        for score, mood_states in score_mappings.items():
            # Initialize score for the mood state for before and after
            mood_state_score_before = 0
            mood_state_score_after = 0
            # Calculate score for the mood state for before and after
            for col in df.columns:
                if "POMS Before >>" in col and col.split(" >> ")[1] in mood_states:
                    mood_state_score_before += convert_poms_values(participant[col])
                elif "POMS After >>" in col and col.split(" >> ")[1] in mood_states:
                    mood_state_score_after += convert_poms_values(participant[col])
            participant_scores.at[index, f'Before {score}'] = mood_state_score_before
            participant_scores.at[index, f'After {score}'] = mood_state_score_after
    
    return participant_scores

# Read the CSV file into a pandas DataFrame
input_file = 'questionnaire.csv'
data = pd.read_csv(input_file)


# Convert POMS values in the DataFrame
converted_data = convert_poms_columns(data)

# Calculate POMS scores for each participant
participant_scores = calculate_poms_scores(converted_data)

# Save the participant scores to a new CSV file
output_file = 'participant_scores.csv'
participant_scores.to_csv(output_file, index=False)

print("Participant scores saved to:", output_file)

# Merge the participant scores DataFrame with the original questionnaire DataFrame
merged_data = pd.merge(data, participant_scores, left_index=True, right_index=True)

# Save the merged DataFrame to a new CSV file
output_file_merged = 'questionnaire_with_scores.csv'
merged_data.to_csv(output_file_merged, index=False)

print("Merged data with participant scores saved to:", output_file_merged)

import pandas as pd

# Read the participant scores CSV file
participant_scores = pd.read_csv('participant_scores.csv')

