from espn_api.basketball import League

import datetime

LEAGUE_ID = 526732270
YEAR = 2024
# COOKIES
SWID = '{A6CB1D09-36A4-4EB1-9B79-D8CFEE3D4548}'
ESPN_S2 = 'AEApaeF/1xQ1lj8MsViwiITyEWUFje068+XJkX1znsnSHj5l6ss7iEv+k551ewcLJkUQMeFwtcioqehwlbrTcNWMCaIbaBP8OPmE9CgXG6XOlKp1B5SCfrk0s1JcYkcakWWENKcs+OBWpPOIBUY1Dn3xYNZcq/Fi4AccFWAloJttGD+j/eZ5Gn9fvP/iBPdDsZmILm2udctu2G85rTYrLjz66XYoGM8RipxEPyfO7YG3A2vq/yXbH4lhX1a7dEN0GG/K5gS2OPpU8oyns72+aHFZ3GEc6bbq4IMrI9tl8Vwg8A=='

TT_LEAGUE = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)

# creating a map of team id's to team name and team owners
TEAM_MAP = {}
TEAM_NAMES = {}
for team in TT_LEAGUE.teams:
    TEAM_MAP[team.team_id] = {
        'team_name': team.team_name,
        'owner': team.owners[0].get('firstName') + ' ' + team.owners[0].get('lastName'),
        'roster': team.roster,
        'schedule': team.schedule
    }
    TEAM_NAMES[team.team_id] = team.team_name

CATEGORIES = ['FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
NINE_CATS = ['FG%', 'FT%', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']

FIRST_DAY = datetime.datetime(2023, 10, 24)

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

## DEPRECATE IN FUTURE
IR_MAP = {
    JUSTIN_ID: None,
    ERKAN_ID: 'Jalen Duren',
    ALBERT_ID: 'Wendell Carter Jr.',
    ANTHONY_ID: 'Jalen Johnson',
    VIJAY_ID: 'Bradley Beal',
    SADYANT_ID: None,
    JEFFREY_ID: None,
    ETHAN_ID: 'Marcus Smart',
    LUCAS_ID: 'Mitchell Robinson',
    ALLAN_ID: 'Bam Adebayo',
    ERNESTO_ID: None,
    ANDREW_ID: 'Kristaps Porzingis'
}