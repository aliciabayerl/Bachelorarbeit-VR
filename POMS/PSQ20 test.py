import pandas as pd
import os

def convert_psq_values(value):
    if value == "Almost never ":
        return 1
    elif value == "Rarely":
        return 2
    elif value == "Sometimes":
        return 3
    elif value == "Often":
        return 4
    elif value == "Always":
        return 5
    else:
        return value

def convert_psq_columns(df):
    for column in df.columns:
        if "PSQ20 >>" in column:
            df[column] = df[column].apply(convert_psq_values)
    return df

def add_transformed_values(df):
    transformed_columns = ['PSQ20 >> You feel rested', 'PSQ20 >> You feel calm', 'PSQ20 >> You have enough time for yourself']
    for col in transformed_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = 6 - df[col]  
    return df

folder_path = 'POMS'
input_file = 'questionnaire_with_scores.csv'
output_file = 'POMS/questionnaire_with_transformed_scores.csv'

data_with_scores = pd.read_csv(os.path.join(folder_path, input_file))

data_with_scores = convert_psq_columns(data_with_scores)
data_with_transformed_values = add_transformed_values(data_with_scores)

data_with_transformed_values.to_csv(output_file, index=False)

print("Transformed values added and saved to:", output_file)

def calculate_psq_scores(df):
    score_mappings = {
        'Worries': ['You fear you may not manage to attain your goals', 'You feel frustrated', 'Your problems seem to be piling up', 'You have many worries', 'You are afraid for the future'],
        'Tension': ['You feel rested', 'You feel calm', 'You feel tense', 'You feel mentally exhausted', 'You have trouble relaxing'],
        'Joy': ['You feel you’re doing things you really like', 'You are full of energy', 'You feel safe and protected', 'You enjoy yourself', 'You are lighthearted'],
        'Demands': ['You feel that too many demands are being made on you', 'You have too many things to do', 'You feel you’re in a hurry', 'You have enough time for yourself', 'You feel under pressure from deadlines']
    }

    first_participant_name = df.iloc[0]['Name']
    print("Name of the first participant:", first_participant_name)
    participant_scores_psq = pd.DataFrame(columns=['Participant', 'Condition', 'Gender', 'Worries', 'Tension', 'Joy', 'Demands', 'Overall_Score'])

    for index, participant in df.iterrows():
        participant_scores_psq.loc[index] = [index + 1, participant['Condition'], participant['Gender'], 0, 0, 0, 0, 0]

        individual_scores = []

        for score, mood_states in score_mappings.items():
            mood_state_score = 0
            count = 0 

            for col in df.columns:
                if "PSQ20 >>" in col and col.split(" >> ")[1] in mood_states:
                    score_value = convert_psq_values(participant[col])
                    if col.split(" >> ")[1] in ['You feel rested', 'You feel calm', 'You have enough time for yourself']:
                        score_value = 6 - score_value
                    if score == 'Joy':
                        score_value = 6 - score_value  # Invert Joy items for the overall score

                    mood_state_score += score_value
                    count += 1

            if count > 0:
                mood_state_score = (((mood_state_score / count) - 1) / 4) * 100

            participant_scores_psq.at[index, score] = mood_state_score
            individual_scores.append(mood_state_score)

        # Calculate overall score as the mean of the individual scores
        overall_score = sum(individual_scores) / len(individual_scores)
        participant_scores_psq.at[index, 'Overall_Score'] = overall_score

    participant_scores_psq[['Worries', 'Tension', 'Joy', 'Demands', 'Overall_Score']] = participant_scores_psq[['Worries', 'Tension', 'Joy', 'Demands', 'Overall_Score']].astype(int)
    print(participant_scores_psq)

    return participant_scores_psq

folder_path = 'POMS'
input_file = 'questionnaire.csv'
output_file = 'POMS/participant_scores_psq.csv'

data = pd.read_csv(os.path.join(folder_path, input_file))

converted_data = convert_psq_columns(data)

participant_scores_psq = calculate_psq_scores(converted_data)

participant_scores_psq.to_csv(output_file, index=False)

print("Participant scores saved to:", output_file)
