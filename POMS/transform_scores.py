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
    
def convert_deq_values(value):
    if value ==  "Not at all":
        return 1
    elif value == "Slightly":
        return 2.5
    elif value == "Moderatly":
        return 4
    elif value == "Quite a bit":
        return 5.5
    elif value == "Very much":
        return 7
    else:
        return value




# Function to convert poms values
def convert_poms_columns(df):
    for column in df.columns:
        if "POMS Before >>" in column or "POMS After >>" in column:
            df[column] = df[column].apply(convert_poms_values)
    return df

# Function to convert deq values
def convert_deq_columns(df):
    for column in df.columns:
        if "DEQ Before >>" in column or "DEQ After >>" in column:
            df[column] = df[column].apply(convert_deq_values)
    return df



# Function to calculate score with mapping POMS
def calculate_poms_scores(df):
    score_mappings = {
        'Tension': ['Panicky', 'Anxious', 'Nervous'],
        'Vigor': ['Lively', 'Energetic', 'Active', 'Alert'],
        'Confusion': ['Confused', 'Mixed up', 'Muddled', 'Uncertain'],
        'Fatigue': ['Worn out', 'Exhausted', 'Sleepy', 'Tired'],
        'Anger': ['Angry', 'Annoyed', 'Bad tempered', 'Bitter'],
        'Depression': ['Depressed', 'Downhearted', 'Unhappy', 'Miserable']
    }

    participant_scores = pd.DataFrame(columns=['Participant', 'Condition', 'Before Tension', 'After Tension', 'Before Vigor', 'After Vigor',
                                               'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue', 'Before Anger_x', 'After Anger_x',
                                               'Before Depression', 'After Depression'])

    for index, participant in df.iterrows():
        scores = [index + 1, participant['Condition']]
        for score, mood_states in score_mappings.items():
            before_score = sum(participant[f"POMS Before >> {mood}"] for mood in mood_states)
            after_score = sum(participant[f"POMS After >> {mood}"] for mood in mood_states)
            scores.extend([before_score, after_score])
        participant_scores.loc[index] = scores

    return participant_scores

# Function to calculate score with mapping DEQ
def calculate_deq_scores(df):
    score_mappings = {
        'Anger': ['Anger', 'Rage', 'Pissed off', 'Mad'],
        'Disgust': ['Grossed out', 'Nausea', 'Revulsion', 'Sickened'],
        'Fear': ['Terror', 'Fear', 'Panic', 'Scared'],
        'Anxiety': ['Dread', 'Anxiety', 'Nervous', 'Worry'],
        'Sadness': ['Empty', 'Lonely', 'Grief', 'Sad'],
        'Desire': ['Longing', 'Craving', 'Wanting', 'Desire'],
        'Relaxation': ['Chilled out', 'Easygoing', 'Relaxation', 'Calm'],
        'Happiness': ['Happy', 'Satisfaction', 'Enjoyment', 'Liking']


    }
    
    # Seperate data to store before and after scores 
    participant_scores_deq = pd.DataFrame(columns=['Participant', 'Condition', 
                                                    'Before Anger', 'After Anger', 
                                                    'Before Disgust', 'After Disgust',
                                                    'Before Fear', 'After Fear', 
                                                    'Before Anxiety', 'After Anxiety',
                                                    'Before Sadness', 'After Sadness', 
                                                    'Before Desire', 'After Desire', 
                                                    'Before Relaxation', 'After Relaxation',
                                                    'Before Happiness', 'After Happiness'])

    print("Columns before assignment:")
    print(participant_scores_deq.columns)
    
    # Loop through participants and calculate scores
    for index, participant in df.iterrows():
        # Score calculation logic
        print("Columns after assignment:")
        print(participant_scores_deq.columns)

    for index, participant in df.iterrows():
        participant_scores_deq.loc[index] = [index + 1, participant['Condition']] + [0] * (len(participant_scores_deq.columns) - 2)
            
        for score, mood_states in score_mappings.items():
            mood_state_score_before = 0
            mood_state_score_after = 0

            for col in df.columns:
                if "DEQ Before >>" in col and col.split(" >> ")[1] in mood_states:
                    mood_state_score_before += convert_deq_values(participant[col])
                elif "DEQ After >>" in col and col.split(" >> ")[1] in mood_states:
                    mood_state_score_after += convert_deq_values(participant[col])
            participant_scores_deq.at[index, f'Before {score}'] = mood_state_score_before
            participant_scores_deq.at[index, f'After {score}'] = mood_state_score_after

    
    return participant_scores_deq


folder_path = 'POMS'
input_file = 'questionnaire.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)


converted_data = convert_poms_columns(data)
converted_data2 = convert_deq_columns(data)

participant_scores = calculate_poms_scores(converted_data)
participant_scores_deq = calculate_deq_scores(converted_data2)

output_file = 'POMS/participant_scores.csv'
output_file2 = 'POMS/participant_scores_deq.csv'
output_file3 = 'POMS/participant_scores_psq.csv'
participant_scores.to_csv(output_file, index=False)
participant_scores_deq.to_csv(output_file2, index=False)

print("Participant scores saved to:", output_file)

combined_scores = pd.merge(participant_scores, participant_scores_deq, on=['Participant', 'Condition'])

merged_questionnaire = pd.merge(data, combined_scores, left_index=True, right_index=True)

output_file_combined = 'POMS/questionnaire_with_scores.csv'
merged_questionnaire.to_csv(output_file_combined, index=False)
