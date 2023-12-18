from pprint import pprint
from collections import defaultdict
from espn_api.basketball import League
import datetime

LEAGUE_ID = 526732270
YEAR = 2024
# COOKIES
SWID = '{A6CB1D09-36A4-4EB1-9B79-D8CFEE3D4548}'
ESPN_S2 = 'AEApaeF/1xQ1lj8MsViwiITyEWUFje068+XJkX1znsnSHj5l6ss7iEv+k551ewcLJkUQMeFwtcioqehwlbrTcNWMCaIbaBP8OPmE9CgXG6XOlKp1B5SCfrk0s1JcYkcakWWENKcs+OBWpPOIBUY1Dn3xYNZcq/Fi4AccFWAloJttGD+j/eZ5Gn9fvP/iBPdDsZmILm2udctu2G85rTYrLjz66XYoGM8RipxEPyfO7YG3A2vq/yXbH4lhX1a7dEN0GG/K5gS2OPpU8oyns72+aHFZ3GEc6bbq4IMrI9tl8Vwg8A=='

TT_LEAGUE = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)

# TEAM ID'S
JUSTIN_ID = 1
ERKAN_ID = 2
ALBERT_ID = 3
ANTHONY_ID = 4
VIJAY_ID = 5
SADYANT_ID = 6
JEFFREY_ID = 7
ETHAN_ID = 8
LUCAS_ID = 9
ALLAN_ID = 10
ERNESTO_ID = 11
ANDREW_ID = 12

# PLAYER AVERAGES
class AvgStatIntervals:
    def __init__(self):
        self.LAST_15 = '2024_last_15'
        self.LAST_30 = '2024_last_30'
        self.LAST_7  = '2024_last_7'
        self.TOTAL = '2024_total'
        self.PROJECTED = '2024_projected'
PLAYER_AVG_STAT_INTERVALS = AvgStatIntervals()

CATEGORIES = ['FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
NINE_CATS = ['FG%', 'FT%', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']

FIRST_DAY = datetime.datetime(2023, 10, 24)

# creating a map of team id's to team name and team owners
TEAM_MAP = {}
for team in TT_LEAGUE.teams:
    TEAM_MAP[team.team_id] = {
        'team_name': team.team_name,
        'owner': team.owners[0].get('firstName') + ' ' + team.owners[0].get('lastName'),
        'roster': team.roster,
        'schedule': team.schedule
    }

# gets number of games player has this week
def get_player_num_games(date, schedule):
    # Input: takes in datetime object and player schedule
    # Output: number of games a player has this week given their schedule dict
    # find index of the most recent Monday w/ respect to start of NBA season
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
def get_projections(team_id, time_interval, project_trade=False):
    # time_interval : last 15, last 30, etc.
    # ERRORS: PLAYER MIGHT NOT HAVE 'time_interval' FIELD (eg. '2024 projections') eg. Goga Bitadze
    # ERRORS: PLAYER MIGHT NOT HAVE 'avg' field in their player.stats.get('time_interval') eg. Ja Morant
    # ANOTHER ERROR: player might not have a certain stat (eg. center with 3ptm) eg. Ivica Zubac
    ROSTER_STATS = {cat: 0 for cat in CATEGORIES}
    team_roster = TEAM_MAP.get(team_id).get('roster', [])
    for player in team_roster:
        sched = player.schedule
        if project_trade:
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


def get_opponent_team_id(id1, matchup_num):
    team1_sched = TEAM_MAP.get(id1).get('schedule')
    home_team = team1_sched[matchup_num - 1].home_team
    # if YOUR team is home team
    if home_team.team_id == id1:
        opponent = team1_sched[matchup_num - 1].away_team
    else:
        opponent = home_team
    return opponent.team_id


def project_matchup(id1, matchup_num, time_interval, id2=-1):
    # NOTE: ID1 IS YOUR TEAM
    # ex. time_interval: last 7, last 15
    if id2 >= 0:
        opponent_team_id = id2
    else:
        opponent_team_id = get_opponent_team_id(id1, matchup_num)

    opponent_team_name = TEAM_MAP.get(opponent_team_id).get('team_name')
    print(TEAM_MAP.get(id1).get('team_name') + ' vs. ' + opponent_team_name)
    team1_projections = get_projections(id1, time_interval)
    team2_projections = get_projections(opponent_team_id, time_interval)
    print(time_interval)
    category_wins, category_ties, category_losses = 0, 0, 0
    MATCHUP_MAP = {}
    for cat in NINE_CATS:
        if team1_projections.get(cat) > team2_projections.get(cat):
            if cat == 'TO':
                category_losses += 1
            else:
                category_wins += 1
        elif team1_projections.get(cat) == team2_projections.get(cat):
            category_ties += 1
        else:
            if cat == 'TO':
                category_wins += 1
            else:
                category_losses += 1
        cat_diff = team1_projections.get(cat) - team2_projections.get(cat)
        MATCHUP_MAP[cat] = (team1_projections.get(cat), team2_projections.get(cat), cat_diff)
    print(str(category_wins) + '-' + str(category_losses) + '-' + str(category_ties))
    return MATCHUP_MAP

print("Projecting next week's matchup")
pprint(project_matchup(ANDREW_ID, 9, PLAYER_AVG_STAT_INTERVALS.LAST_15))

print("Projecting how you currently stand against Lucas")
pprint(project_matchup(ANDREW_ID, -1, PLAYER_AVG_STAT_INTERVALS.LAST_15, LUCAS_ID))

## compare trade for player

## stretch goals: TRADE TARGETS TO BEST IMPROVE TEAM

## stretch goal: identify which player to trade on your team