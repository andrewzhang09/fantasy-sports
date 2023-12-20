from flask import render_template

from ..constants import AvgStatIntervals, NINE_CATS, ANDREW_ID, ERKAN_ID, TT_LEAGUE, TEAM_NAMES
from .project_matchup import project_matchup

PlayerAvgStatIntervals = AvgStatIntervals()

def project_trade(id1, partner_team_id, trading_player_names, receiving_player_names):
    # project_matchup(id1, opponent_team_id, time_interval, is_curr_matchup=False)
    # MVP: project net gain and loss for team cats based on this trade for both teams
    # project before AND after against all teams if you do this trade
    players_trading = [TT_LEAGUE.player_info(name) for name in trading_player_names]
    players_receiving = [TT_LEAGUE.player_info(name) for name in receiving_player_names]
    team1_trade = {
        'trade': players_trading,
        'receive': players_receiving
    }
    team2_trade = {
        'trade': players_receiving,
        'receive': players_trading
    }
    # PROJECTING MATCHUP AGAINST YOURSELF GIVEN THIS TRADE DICT
    team1_roster_stats = project_matchup(id1, 
                                         id1, 
                                         PlayerAvgStatIntervals.LAST_30, 
                                         False,
                                         team1_trade)
    team2_roster_stats = project_matchup(partner_team_id, 
                                         partner_team_id, 
                                         PlayerAvgStatIntervals.LAST_30, 
                                         False,
                                         team2_trade)
    return team1_roster_stats, team2_roster_stats


# GET /project-trade
def project_trade_handler():
    # TODO: change so that we don't manually have to code in inputs
    team1_roster_stats, team2_roster_stats = project_trade(ANDREW_ID,
                                                           ERKAN_ID,
                                                           ['Keldon Johnson'],
                                                           ['Dennis Schroder'])
    return render_template('project_trade.html',
                    team1_roster=team1_roster_stats,
                    partner_team_roster=team2_roster_stats,
                    teams=[TEAM_NAMES.get(ANDREW_ID), TEAM_NAMES.get(ERKAN_ID)],
                    time_interval=PlayerAvgStatIntervals.LAST_30,
                    nine_cats=NINE_CATS)