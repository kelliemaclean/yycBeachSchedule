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
    schedule = {f'Week {i}': [] for i in range(1, num_weeks + 1)}

    # Create a schedule dictionary to store matchups for each slot
    slots = {f'Game {i}': [] for i in range(1, time_slots + 1)}
    
    # Create a list of team names (you can customize this)
    teams = [f'Team {i}' for i in range(1, num_teams + 1)]
    
    # Create list to create a dataframe
    Week = []
    Game = []
    Courts = []
    
    # Initialize the previous week's matchups
    prev_week_matches = []

    # Generate the schedule
    for week in schedule:
        random.shuffle(teams)
        team_play = []
        week_matches = []

        for slot in slots:
            Week.append(week)
            Game.append(slot)
            remaining_teams = teams.copy()
            
            # Create a schedule dictionary to store matchups for each slot
            courts = {f'court {i}': [] for i in range(1, num_courts + 1)}
            
            # for each court, add teams remaining
            for court in courts:
                while True:
                    team1 = remaining_teams.pop()
                    team2 = remaining_teams.pop()

                    # Check if team1 vs. team2 was played last week
                    if f'{team1} vs. {team2}' not in prev_week_matches and f'{team2} vs. {team1}' not in prev_week_matches:
                        team_play.append(team1)
                        team_play.append(team2)

                        if team1[-1] < team2[-1]:
                            courts[court].append(f'{team1} vs. {team2}')
                            week_matches.append(f'{team1} vs. {team2}')
                        else:
                            courts[court].append(f'{team2} vs. {team1}')
                            week_matches.append(f'{team1} vs. {team2}')
                        break  # Exit the loop if a valid matchup is found

                    # If the matchup was played last week, swap team1 and team2 and try again
                    remaining_teams.insert(0, team2)
                    remaining_teams.insert(0, team1)

            # Rotate the teams in a circular manner
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]

            # Add court schedule dictionary to Courts list
            Courts.append(courts)
        
        # Update the previous week's matchups
        prev_week_matches = week_matches 
        print(prev_week_matches)

    Courts = pd.DataFrame(Courts)
    schedule = pd.DataFrame({'Week': Week, 'Game': Game})
    schedule = pd.merge(schedule, Courts, left_index=True, right_index=True)
    schedule = schedule.astype(str)

    court_columns = [col for col in schedule.columns if col.startswith('court')]
    unique_values = np.unique(schedule[court_columns].values)

    for value in unique_values:
        count = (schedule == value).sum().sum()
        counts.append(count)
    
    return schedule, list(court_columns), max(counts), min(counts)

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
    
    # Create list to create dataframe
    Week = []
    Game = []
    Courts = []
    Bye = []
    
    # Generate the schedule
    for week in schedule:
        random.shuffle(teams)
        team_play = []
        

        for slot in slots:
            Week.append(week)
            Game.append(slot)
            
            remaining_teams = teams.copy()
            bye = []
            teams_round_play = []
            
            # Create a schedule dictionary to store matchups for each slot
            courts = {f'courts {i}': [] for i in range(1, num_courts + 1)}
            courts_cols = courts.keys()

            for value in team_play:
                count = len([item for item in team_play if item == value])
                
                #if the team played the first 2 round remove from remaining teams
                if count == 2:
                    if value in remaining_teams:
                        remaining_teams.remove(value)
                        
                    else: 
                        pass
                else:
                    remaining_teams = remaining_teams

            for court in courts:

                if len(remaining_teams) > 1:
                    if slot == 'Game 2':
                        team1 = teams_not_played.pop()
                        team2 = remaining_teams.pop()
                        team_play.append(team1)
                        team_play.append(team2)
                        teams_round_play.append(team1)
                        teams_round_play.append(team2)

                        if team1[-1] < team2[-1]:
                            courts[court].append(f'{team1} vs. {team2}')
                        else:
                            courts[court].append(f'{team2} vs. {team1}')

                    else:
                        team1 = remaining_teams.pop()
                        team2 = remaining_teams.pop()
                        team_play.append(team1)
                        team_play.append(team2)
                        teams_round_play.append(team1)
                        teams_round_play.append(team2)

                        if team1[-1] < team2[-1]:
                            courts[court].append(f'{team1} vs. {team2}')
                        else:
                            courts[court].append(f'{team2} vs. {team1}')
                
                else:
                    pass
                

            
            teams_not_played = remaining_teams.copy()
            bye =list(filter(lambda x: x not in teams_round_play, teams))
            Bye.append(bye)


            # Rotate the teams in a circular manner
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]

            Courts.append(courts)


    Courts = pd.DataFrame(Courts)
    schedule = pd.DataFrame({'Week': Week, 'Game': Game, 'Bye': Bye})
    schedule = pd.merge(schedule, Courts, left_index=True, right_index=True)
    schedule = schedule.astype(str)

    court_columns = [col for col in schedule.columns if col.startswith('court')]
    unique_values = np.unique(schedule[court_columns].values)

    for value in unique_values:
        count = (schedule == value).sum().sum()
        counts.append(count)

    
    return schedule, list(courts_cols), max(counts), min(counts), counts

def main(num_teams = int, num_weeks = int, num_courts = int, bye = str):

    if bye == 'True':
        print(f'Creating schedule with 3 time slots, 1 bye, {num_teams} teams')
        schedule, courts, max_count, min_count, counts = generate_schedule_with_bye(num_teams = num_teams,
                                                        num_weeks = num_weeks, 
                                                        num_courts = num_courts
                                                    )
        # check schedule that teams dont play more than n and every team plays eachother at least once
        while (max_count > ((num_weeks/2)-1)) and (min_count < 1):
            schedule, courts, max_count, min_count, counts = generate_schedule_with_bye(num_teams = num_teams,
                                                            num_weeks = num_weeks, 
                                                            num_courts = num_courts
                                                        )

        return schedule

    elif bye == 'False':

        if num_teams < 10:
            max_team_matchups = 4
        else:
            max_team_matchups = 3

        print(f'Creating schedule with 2 time slots, {num_teams} teams')
        schedule, courts, max_count, min_count = generate_schedule_without_bye(num_teams = num_teams,
                                                        num_weeks = num_weeks, 
                                                       num_courts = num_courts
                                                    )
        while max_count > 4:
            schedule, courts, max_count, min_count = generate_schedule_without_bye(num_teams = num_teams,
                                                            num_weeks = num_weeks, 
                                                            num_courts = num_courts
                                                        )
        while min_count < 1:
            schedule, courts, max_count, min_count = generate_schedule_without_bye(num_teams = num_teams,
                                                        num_weeks = num_weeks, 
                                                        num_courts = num_courts
                                                    )

        return schedule
    
    else:
        print('Bye must = True or False')

num_teams = int(input('Number of Teams:'))
num_weeks = int(input('Number fo Weeks:'))
num_courts = int(input('Number of Courts:'))
bye = input('Bye (True or False):')
FILE_NAME = input('File Name:')

schedule = main(num_teams = num_teams, num_weeks = num_weeks , num_courts = num_courts , bye = bye)

schedule.to_csv(f'schedules/{FILE_NAME}.csv', index=False)
