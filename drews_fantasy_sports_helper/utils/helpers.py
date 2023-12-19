import datetime

from ..constants import FIRST_DAY, CATEGORIES, TEAM_MAP

# gets number of games player has this week
def get_player_num_games(date, schedule):
    # Input: takes in datetime object and player schedule
    # Output: number of games a player has this week given their schedule dict
    # find index of the most recent Monday w/ respect to start of NBA season

    # TODO: change to current time instead of starting from Monday, accounting for UTC time diff
    curr_weekday = date.weekday()
    time_diff = date - FIRST_DAY
    days_since_start = time_diff.days
    week_start = days_since_start - curr_weekday + 1

    num_games = 0
    for day in range(week_start, week_start + 7):
        if str(day) in schedule:
            # print(sched.get(str(day)))
            num_games += 1
    return num_games

## get projections based on averages for players on team roster for CURRENT week
def get_projections(team_id, time_interval, ir, four_game_proj=False):
    # time_interval : last 15, last 30, etc.
    # ERRORS: PLAYER MIGHT NOT HAVE 'time_interval' FIELD (eg. '2024 projections') eg. Goga Bitadze
    # ERRORS: PLAYER MIGHT NOT HAVE 'avg' field in their player.stats.get('time_interval') eg. Ja Morant
    # ANOTHER ERROR: player might not have a certain stat (eg. center with 3ptm) eg. Ivica Zubac

    # TODO: if current_matchup is True, calculate num_games starting from current date
    ROSTER_STATS = {cat: 0 for cat in CATEGORIES}
    team_roster = TEAM_MAP.get(team_id).get('roster', [])
    for player in team_roster:
        if player.name in ir:
            continue
        sched = player.schedule
        # standardize projections to 4 games for each player
        if four_game_proj:
            num_games = 4
        else:
            num_games = get_player_num_games(datetime.datetime.now(), sched)
        player_avg_stats = player.stats.get(time_interval, {})
        # Player that has not played this season will not have the 'avg' field
        if 'avg' not in player_avg_stats:
            continue
        player_avg_stats = player_avg_stats.get('avg')

        for cat in CATEGORIES:
            ROSTER_STATS[cat] += num_games * player_avg_stats.get(cat, 0)
    
    ROSTER_STATS['FG%'] = ROSTER_STATS.get('FGM') / ROSTER_STATS.get('FGA')
    ROSTER_STATS['FT%'] = ROSTER_STATS.get('FTM') / ROSTER_STATS.get('FTA')
    for cat in ['FGM', 'FGA', 'FTM', 'FTA']:
        del ROSTER_STATS[cat]
    return ROSTER_STATS