import pandas as pd
from fuzzywuzzy import process
from numpy import random


players = pd.read_csv('data_players.csv')
teams = pd.read_csv('data_teams.csv')
teams_official = pd.read_csv('data_teams_official.csv')
qs = pd.read_csv('data_questions.csv')

# print(questions)
qs.dropna(inplace=True)
# print(qs)
qs['Answer Match'] = ""
qs['Answer Match Certainty'] = ""
qs['Answer Type'] = ""
qs['Option 1'] = ""
qs['Option 2'] = ""
qs['Option 3'] = ""

display = True

for i in qs.index:
    ans = qs.loc[i, 'Answer']
    ratio_players = process.extract( ans, players['Players'].values)
    max_player_ratio = ratio_players[0]
    ratio_teams = process.extract( ans, teams['Teams'].values)
    max_team_ratio = ratio_teams[0]

    max_ratio = max(max_player_ratio[1], max_team_ratio[1])
    qs.loc[i, 'Answer Match Certainty'] = max_ratio
    max_result = (max_player_ratio[0] if max_ratio == max_player_ratio[1] else max_team_ratio[0])
    qs.loc[i, 'Answer Match'] = max_result

    if display:
        print('Index: ', i)
        print('Answer: ', ans)
        print('Match: ', max_result)
        print('Certainty: ', max_ratio)

    if ( max_ratio == max_player_ratio[1] ):
        qs.loc[i, 'Answer Type'] = 'Player'
        # answer_type = 'Player'
        wrong_choices = players['Players'].values[players['Players'].values != max_result]
    else:
        qs.loc[i, 'Answer Type'] = 'Team'
        # answer_type = 'Team'
        mask_team = ( max_result == teams['Teams'] )
        team_number = teams.loc[mask_team, 'Team Number'].values[0]
        wrong_choices = teams_official.loc[teams_official['Team Number'] != team_number, 'Teams'].values

    wrong_answers = random.choice(wrong_choices, 3, replace = False)
    qs.loc[i, 'Option 1'] = wrong_answers[0]
    qs.loc[i, 'Option 2'] = wrong_answers[1]
    qs.loc[i, 'Option 3'] = wrong_answers[2]

print(qs)
qs.to_csv('output.csv', index = False)
