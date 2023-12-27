from flask import current_app, session

import datetime
from pprint import pprint

from ..constants import FIRST_DAY, CATEGORIES, NINE_CATS, TEAM_MAP, TT_LEAGUE, AvgStatIntervals

PlayerAvgStatIntervals = AvgStatIntervals()


def fetch_team(team_id):
    LEAGUE_TEAMS = session.get('TEAMS', [])
    if not LEAGUE_TEAMS:
        return
    for team in LEAGUE_TEAMS:
        if team.team_id == team_id:
            return team


def get_opponent_team_id(id1, matchup_num):
    team = fetch_team(id1)
    team1_sched = team.schedule
    home_team = team1_sched[matchup_num - 1].home_team
    # if YOUR team is home team
    if home_team.team_id == id1:
        opponent = team1_sched[matchup_num - 1].away_team
    else:
        opponent = home_team
    return opponent.team_id


def calculate_win_loss(MATCHUP_MAP):
    # returns a tuple of (wins, losses, ties)
    category_wins, category_losses, category_ties = 0, 0, 0
    for cat in NINE_CATS:
        if MATCHUP_MAP.get(cat)[0] > MATCHUP_MAP.get(cat)[1]:
            if cat == 'TO':
                category_losses += 1
            else:
                category_wins += 1
        elif MATCHUP_MAP.get(cat)[0] == MATCHUP_MAP.get(cat)[1]:
            category_ties += 1
        else:
            if cat == 'TO':
                category_wins += 1
            else:
                category_losses += 1
    return (category_wins, category_losses, category_ties)


def fetch_curr_box_score(MATCHUP_MAP, id1):
    # def box_scores(matchup_period: int = None, scoring_period: int = None, matchup_total: bool = True) -> List[BoxScore]
    # find box score that corresponds to the teams we want
    for box_score in TT_LEAGUE.box_scores():
        if box_score.home_team.team_id == id1:
            for cat in CATEGORIES:
                # Error: If it is Monday, then there will be no box score
                team1_cat = box_score.home_stats.get(cat)
                team2_cat = box_score.away_stats.get(cat)
                if not team1_cat or not team2_cat:
                    MATCHUP_MAP[cat] = (0, 0, 0)
                    return
                team1_cat = team1_cat.get('value')
                team2_cat = team2_cat.get('value')
                # we will calculate cat_diff at the end, set to 0 for now
                MATCHUP_MAP[cat] = (team1_cat, team2_cat, 0)
            break
        elif box_score.away_team.team_id == id1:
            for cat in CATEGORIES:
                team1_cat = box_score.away_stats.get(cat)
                team2_cat = box_score.home_stats.get(cat)
                if not team1_cat or not team2_cat:
                    MATCHUP_MAP[cat] = (0, 0, 0)
                    return
                team1_cat = team1_cat.get('value')
                team2_cat = team2_cat.get('value')
                MATCHUP_MAP[cat] = (team1_cat, team2_cat, 0)
            break


def calculate_fg_ft_percentage(MATCHUP_MAP):
    team1_fg_percentage = MATCHUP_MAP.get('FGM')[0] / MATCHUP_MAP.get('FGA')[0]
    team2_fg_percentage = MATCHUP_MAP.get('FGM')[1] / MATCHUP_MAP.get('FGA')[1]
    team1_ft_percentage = MATCHUP_MAP.get('FTM')[0] / MATCHUP_MAP.get('FTA')[0]
    team2_ft_percentage = MATCHUP_MAP.get('FTM')[1] / MATCHUP_MAP.get('FTA')[1]
    
    MATCHUP_MAP['FG%'] = (team1_fg_percentage, team2_fg_percentage, team1_fg_percentage - team2_fg_percentage)
    MATCHUP_MAP['FT%'] = (team1_ft_percentage, team2_ft_percentage, team1_ft_percentage - team2_ft_percentage)
    for cat in ['FGM', 'FGA', 'FTM', 'FTA']:
        del MATCHUP_MAP[cat]              
    

# gets number of games player has REMAINING this week
def get_player_num_games(date, schedule):
    # Input: takes in datetime object and player schedule
    # Output: number of games a player has REMAINING this week, including today
    curr_weekday = date.weekday()
    time_diff = date - FIRST_DAY
    days_since_start = time_diff.days
    week_start = days_since_start - curr_weekday + 1

    num_games = 0
    today = days_since_start + 1
    # NOTE: box score updates at 12am most likely, so start projecting from today instead of tomorrow
    for day in range(today, week_start + 7):
        if str(day) in schedule:
            num_games += 1
    return num_games


## get projections based on averages for players on team roster for CURRENT week
def get_projections(team_id, time_interval, is_curr_matchup=False, trade_dict={}):
    # time_interval : last 15, last 30, etc.
    # ERRORS: PLAYER MIGHT NOT HAVE 'time_interval' FIELD (eg. '2024 projections') eg. Goga Bitadze
    # ERRORS: PLAYER MIGHT NOT HAVE 'avg' field in their player.stats.get('time_interval') eg. Ja Morant
    # ANOTHER ERROR: player might not have a certain stat (eg. center with 3ptm) eg. Ivica Zubac
    
    team = fetch_team(team_id)
    team_roster = team.roster
    ROSTER_STATS = {cat: 0 for cat in CATEGORIES}
    for i in range(len(team_roster)):
        player = team_roster[i]
        # TODO: add feature where you can choose whether a player is out for long period of time or not
        if is_curr_matchup:
            if player.injuryStatus == 'OUT':
                continue
            sched = player.schedule
            num_games = get_player_num_games(datetime.datetime.now(), sched)
        # Project all/Project trade when there is player on IR
        # -> we want to exclude the last person on roster which is likely a stream
        # TODO: add feature where you can choose which player to keep or not
        else:
            if i == 13:
                continue
            num_games = 4

        player_avg_stats = player.stats.get(time_interval, {})
        # Player that has not played this season will not have the 'avg' field
        if 'avg' not in player_avg_stats:
            continue
        player_avg_stats = player_avg_stats.get('avg')

        for cat in CATEGORIES:
            ROSTER_STATS[cat] += num_games * player_avg_stats.get(cat, 0)
    
    # add player stats that you are receiving, subtract the ones you trade away
    num_games = 4
    if trade_dict:
        pprint(trade_dict)
        players_trading, players_receiving = trade_dict.get('trade', []), trade_dict.get('receive', [])
        for player in players_receiving:
            # for some reason, these player stats only have the '2024 total' and '2024 projected' fields
            player_avg_stats = player.stats.get(PlayerAvgStatIntervals.TOTAL, {})
            if 'avg' not in player_avg_stats:
                continue
            player_avg_stats = player_avg_stats.get('avg')

            for cat in CATEGORIES:
                ROSTER_STATS[cat] += num_games * player_avg_stats.get(cat, 0)

        for player in players_trading:
            player_avg_stats = player.stats.get(PlayerAvgStatIntervals.TOTAL, {})
            if 'avg' not in player_avg_stats:
                continue
            player_avg_stats = player_avg_stats.get('avg')

            for cat in CATEGORIES:
                ROSTER_STATS[cat] -= num_games * player_avg_stats.get(cat, 0)
    
    return ROSTER_STATS