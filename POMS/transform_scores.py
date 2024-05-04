import pandas as pd
import os

# conversion of POMS values
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
        return value 

# Function to convert poms values
def convert_poms_columns(df):
    for column in df.columns:
        if "POMS Before >>" in column or "POMS After >>" in column:
            df[column] = df[column].apply(convert_poms_values)
    return df

# Function to calculate score with mapping
def calculate_poms_scores(df):
    score_mappings = {
        'Tension': ['Panicky', 'Anxious', 'Nervous'],
        'Vigor': ['Lively', 'Energetic', 'Active', 'Alert'],
        'Confusion': ['Confused', 'Mixed up', 'Muddled', 'Uncertain'],
        'Fatigue': ['Worn out', 'Exhausted', 'Sleepy', 'Tired'],
        'Depression': ['Depressed', 'Downhearted', 'Unhappy', 'Miserable']
    }
    
    # Seperate data to store before and after scores 
    participant_scores = pd.DataFrame(columns=['Participant', 'Condition', 'Before Tension', 'After Tension', 'Before Vigor', 'After Vigor',
                                               'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue',
                                               'Before Depression', 'After Depression'])
    
    for index, participant in df.iterrows():
        participant_scores.loc[index] = [index + 1, participant['Condition']] + [0] * 10
        
        for score, mood_states in score_mappings.items():
            mood_state_score_before = 0
            mood_state_score_after = 0

            for col in df.columns:
                if "POMS Before >>" in col and col.split(" >> ")[1] in mood_states:
                    mood_state_score_before += convert_poms_values(participant[col])
                elif "POMS After >>" in col and col.split(" >> ")[1] in mood_states:
                    mood_state_score_after += convert_poms_values(participant[col])
            participant_scores.at[index, f'Before {score}'] = mood_state_score_before
            participant_scores.at[index, f'After {score}'] = mood_state_score_after
    
    return participant_scores

folder_path = 'POMS'
input_file = 'questionnaire.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)


converted_data = convert_poms_columns(data)

participant_scores = calculate_poms_scores(converted_data)

output_file = 'POMS/participant_scores.csv'
participant_scores.to_csv(output_file, index=False)

print("Participant scores saved to:", output_file)

# Merge participant scores with original questionnaire and save in new
merged_data = pd.merge(data, participant_scores, left_index=True, right_index=True)

output_file_merged = 'POMS/questionnaire_with_scores.csv'
merged_data.to_csv(output_file_merged, index=False)
