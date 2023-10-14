import sys
import random
import itertools
import pandas as pd
import numpy as np

## need to have bye groups and rotation (create bye groups)
## no teams play back to back. 

def generate_schedule_without_bye(num_teams=int, num_weeks=int, num_courts=int):
    counts = []
    
    if num_teams < 2:
        return "Number of teams must be at least 2."
    
    time_slots = 2

    # Create a schedule dictionary to store matchups for each week
    schedule_dict = {f'Week {i}': [] for i in range(1, num_weeks + 1)}

    # Create a schedule dictionary to store matchups for each slot
    slots = {f'Game {i}': [] for i in range(1, time_slots + 1)}
    
    # Create a list of team names (you can customize this)
    teams = [f'Team {i}' for i in range(1, num_teams + 1)]
    
    if len(teams) % 2 != 0:
        teams.append(None)  # Add a "bye" or dummy team if the number of teams is odd

    matches = []

    for week in range(num_weeks):
        matchups = []
        for i in range(len(teams) // 2):
            match = (teams[i], teams[-i - 1])
            matchups.append(match)
        matches.append(matchups)

        # Rotate the teams in a circular manner, excluding the first team
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        
    for match in matches:
        random.shuffle(match)
    
    # Create list to create a dataframe
    Week = []
    Game = []
    Courts = []
    
    match_round = 0
    # Generate the schedule
    for week in schedule_dict:

        for slot in slots:
            Week.append(week)
            Game.append(slot)
            
            # Create a schedule dictionary to store matchups for each slot
            courts = {f'court {i}': [] for i in range(1, num_courts + 1)}
            
            match = 0
            # for each court, add teams remaining
            for court in courts:
                team1 = matches[match_round][match][0]
                team2 = matches[match_round][match][1]
                match = match+1
                
                if team1[-1] < team2[-1]:
                    courts[court].append(f'{team1} vs. {team2}')

                else:
                    courts[court].append(f'{team2} vs. {team1}')
                    
            if match_round < (num_weeks-1):         
                match_round = match_round+1
            else:
                match_round = 0
            
            #print(match_round)
            # Add court schedule dictionary to Courts list
            Courts.append(courts)
        

    Courts = pd.DataFrame(Courts)
    schedule = pd.DataFrame({'Week': Week, 'Game': Game})
    schedule = pd.merge(schedule, Courts, left_index=True, right_index=True)
    schedule = schedule.astype(str)

    court_columns = [col for col in schedule.columns if col.startswith('court')]
    unique_values = np.unique(schedule[court_columns].values)

    for value in unique_values:
        count = (schedule == value).sum().sum()
        counts.append(count)
    
    return schedule

def create_group_matches(group1, group2, num_weeks):
    matches = []
    teams = group1 + group2

    for week in range(num_weeks+1):
        matchups = []
        for i in range(len(teams) // 2):
            match = (teams[i], teams[-i - 1])
            matchups.append(match)
        matches.append(matchups)

        # Rotate the teams in a circular manner, excluding the first team
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        
    return matches

def generate_schedule_with_bye(num_teams =int, num_weeks=int, num_courts=int):
    
    counts = []
    
    if num_teams < 2:
        return "Number of teams must be at least 2."
    
    time_slots = 3

    # Create a schedule dictionary to store matchups for each week
    schedule = {f'Week {i}': [] for i in range(1, num_weeks + 1)}

    # Create a schedule dictionary to store matchups for each slot
    slots = {f'Game {i}': [] for i in range(1, time_slots + 1)}
    
    # Create a list of team names (you can customize this)
    teams = [f'Team {i}' for i in range(1, num_teams + 1)]
    n = int(num_teams/3)
    
    # creat a dictionary for bye groups
    group_dict = {
        'bye1':teams[0:n],
        'bye2':teams[n:(n+n)],
        'bye3':teams[-n:]
    }
    groups = ['bye1','bye2','bye3']
    
    # create group scehdule
    byeGroup_1_2 = create_group_matches(group_dict['bye1'], group_dict['bye2'], num_weeks)
    byeGroup_1_3 = create_group_matches(group_dict['bye3'], group_dict['bye1'], num_weeks)
    byeGroup_2_3 = create_group_matches(group_dict['bye2'], group_dict['bye3'], num_weeks)

    # Create list to create dataframe
    Week = []
    Game = []
    Courts = []
    Bye = []
    match_round_1 = 0
    match_round_2 = 0
    match_round_3 = 0
    
    # Generate the schedule
    for week in schedule:
        week_matches = []
        for slot in slots:
            Week.append(week)
            Game.append(slot)
            # add bye groups to slot
            bye = groups[0]
            Bye.append(group_dict[groups[0]])
            
            # Create a schedule dictionary to store matchups for each slot
            courts = {f'courts {i}': [] for i in range(1, num_courts + 1)}
            
            if bye == 'bye1':
                match = 0
                # for each court, add teams remaining
                for court in courts:
                    team1 = byeGroup_2_3[match_round_1][match][0]
                    team2 = byeGroup_2_3[match_round_1][match][1]
                    match = match+1

                    if team1[-1] < team2[-1]:
                        courts[court].append(f'{team1} vs. {team2}')

                    else:
                        courts[court].append(f'{team2} vs. {team1}')

                if match_round_1 < (num_weeks):         
                    match_round_1 = match_round_1+1
                else:
                    match_round_1 = 0
            
            elif bye == 'bye2':
                match = 0
                # for each court, add teams remaining
                for court in courts:
                    team1 = byeGroup_1_3[match_round_2][match][0]
                    team2 = byeGroup_1_3[match_round_2][match][1]
                    match = match+1

                    if team1[-1] < team2[-1]:
                        courts[court].append(f'{team1} vs. {team2}')

                    else:
                        courts[court].append(f'{team2} vs. {team1}')

                if match_round_2 < (num_weeks):         
                    match_round_2 = match_round_2+1
                else:
                    match_round_2 = 0
                    
            elif bye == 'bye3':
                match = 0
                # for each court, add teams remaining
                for court in courts:
                    team1 = byeGroup_1_2[match_round_3][match][0]
                    team2 = byeGroup_1_2[match_round_3][match][1]
                    match = match+1

                    if team1[-1] < team2[-1]:
                        courts[court].append(f'{team1} vs. {team2}')

                    else:
                        courts[court].append(f'{team2} vs. {team1}')

                if match_round_3 < (num_weeks):         
                    match_round_3 = match_round_3+1
                else:
                    match_round_3 = 0

            
            #rotate bye groups for matches
            groups.append(groups.pop(0))

            # add court dictionary to court column
            Courts.append(courts)
        
        #rotate bye groups for matches
        groups.append(groups.pop(0))

    #create dataframe for schedule
    Courts = pd.DataFrame(Courts)
    schedule = pd.DataFrame({'Week': Week, 'Game': Game, 'Bye': Bye})
    schedule = pd.merge(schedule, Courts, left_index=True, right_index=True)
    schedule = schedule.astype(str)

    court_columns = [col for col in schedule.columns if col.startswith('court')]
    unique_values = np.unique(schedule[court_columns].values)

    for value in unique_values:
        count = (schedule == value).sum().sum()
        counts.append(count)
    

    return schedule, max(counts), min(counts)

def main(num_teams = int, num_weeks = int, num_courts = int, bye = str):

    if bye == 'True':
        print(f'Creating schedule with 3 time slots, 1 bye, {num_teams} teams')
        schedule, max_count, min_count = generate_schedule_with_bye(num_teams = num_teams,
                                                        num_weeks = num_weeks, 
                                                        num_courts = num_courts
                                                    )
        # check schedule that teams dont play more than n and every team plays eachother at least once
        while (max_count > 3) and (min_count < 1):
            schedule, max_count, min_count = generate_schedule_with_bye(num_teams = num_teams,
                                                            num_weeks = num_weeks, 
                                                            num_courts = num_courts
                                                        )

        return schedule

    elif bye == 'False':
       schedule = generate_schedule_without_bye(num_teams=num_teams, 
                                                num_weeks=num_weeks, 
                                                num_courts=num_courts)
       return schedule
    
    else:
        return print('error in inputs')

num_teams = int(input('Number of Teams:'))
num_weeks = int(input('Number fo Weeks:'))
num_courts = int(input('Number of Courts:'))
bye = input('Bye (True or False):')
FILE_NAME = input('File Name:')

schedule = main(num_teams = num_teams, num_weeks = num_weeks , num_courts = num_courts , bye = bye)

schedule.to_csv(f'schedules/{FILE_NAME}.csv', index=False)
