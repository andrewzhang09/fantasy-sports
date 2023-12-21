from flask import render_template

from ..constants import AvgStatIntervals, NINE_CATS, ANDREW_ID, ERKAN_ID, TT_LEAGUE, TEAM_NAMES
from .project_matchup import project_matchup
from .project_all import generate_all_projections

PlayerAvgStatIntervals = AvgStatIntervals()


def create_trade_map(trading_player_names, receiving_player_names):
    players_trading = [TT_LEAGUE.player_info(name) for name in trading_player_names]
    players_receiving = [TT_LEAGUE.player_info(name) for name in receiving_player_names]
    return {
        'trade': players_trading,
        'receive': players_receiving
    }


def compare_after_trade_all_teams(id, time_interval, trading_player_names, receiving_player_names):
    POST_TRADE_ALL_TEAMS_MAP = {}
    trade_dict = create_trade_map(trading_player_names, receiving_player_names)
    for opponent_team_id in range(1, 13):
        if opponent_team_id == id:
            continue
        matchup_map = project_matchup(id, 
                                      opponent_team_id, 
                                      time_interval,
                                      False,
                                      trade_dict)
        POST_TRADE_ALL_TEAMS_MAP[(id, opponent_team_id)] = matchup_map

    PRE_TRADE_ALL_TEAMS_MAP = generate_all_projections(id, time_interval)
    
    # do something with pre trade and post trade maps, modify post_trade map and return it
    for id_tuple in PRE_TRADE_ALL_TEAMS_MAP.keys():
        pre_trade_matchup_map = PRE_TRADE_ALL_TEAMS_MAP.get(id_tuple)
        post_trade_matchup_map = POST_TRADE_ALL_TEAMS_MAP.get(id_tuple)
        print(TEAM_NAMES.get(id_tuple[1]))
        for cat in NINE_CATS:
            # improve_from_trade is 1 if trade makes you go from lose -> win against team in that cat
            # 0 if win/loss stays same
            # -1 if you go from win -> lose in that cat 
            improve_from_trade = 0
            pre_trade_cat_diff, post_trade_cat_diff = pre_trade_matchup_map.get(cat)[2], post_trade_matchup_map.get(cat)[2]
            if pre_trade_cat_diff < 0 and post_trade_cat_diff >= 0:
                if cat == 'TO':
                    improve_from_trade = -1
                else:
                    improve_from_trade = 1
            elif pre_trade_cat_diff > 0 and post_trade_cat_diff <= 0:
                if cat == 'TO':
                    improve_from_trade = 1
                else:
                    improve_from_trade = -1
            print(cat + ': (pre_trade_cat_diff, post_trade_cat_diff, improve_from_trade)')
            print((pre_trade_cat_diff, post_trade_cat_diff, improve_from_trade))

            post_trade_team1_stat, post_trade_team2_stat, _ = post_trade_matchup_map.get(cat)
            POST_TRADE_ALL_TEAMS_MAP[id_tuple][cat] = (post_trade_team1_stat, post_trade_team2_stat, post_trade_cat_diff, improve_from_trade)

    return POST_TRADE_ALL_TEAMS_MAP


def project_trade(id1, time_interval, trading_player_names, receiving_player_names):
    # project_matchup(id1, opponent_team_id, time_interval, is_curr_matchup=False)
    # project before AND after against all teams if you do this trade

    # TODO: add functionality to do a trade where trading and receiving num players is uneven (eg. trading 3 for 2 players)
    team1_trade = create_trade_map(trading_player_names, receiving_player_names)
    # PROJECTING MATCHUP AGAINST YOURSELF GIVEN THIS TRADE DICT
    team1_roster_stats = project_matchup(id1, 
                                         id1, 
                                         time_interval, 
                                         False,
                                         team1_trade)
    return team1_roster_stats


# GET /project-trade
def project_trade_handler():
    # TODO: change so that we don't manually have to code in inputs
    trading_player_names, receiving_player_names = ['Keldon Johnson', 'Karl-Anthony Towns'], ['Dennis Schroder', "De'Aaron Fox"]
    # trade projections are done using season avg's or projections, because that's the only fields for avg's that League.player_info() returns
    time_interval = PlayerAvgStatIntervals.TOTAL
    team1_roster_stats = project_trade(ANDREW_ID,
                                       time_interval,
                                       trading_player_names,
                                       receiving_player_names)
    POST_TRADE_ALL_TEAMS_MAP = compare_after_trade_all_teams(ANDREW_ID, 
                                                             time_interval, 
                                                             trading_player_names, 
                                                             receiving_player_names)
    return render_template('project_trade.html',
                    team1_roster=team1_roster_stats,
                    teams=[TEAM_NAMES.get(ANDREW_ID), TEAM_NAMES.get(ERKAN_ID)],
                    time_interval=time_interval,
                    nine_cats=NINE_CATS,
                    post_trade_matchup_maps=POST_TRADE_ALL_TEAMS_MAP,
                    team_names=TEAM_NAMES,
                    players_trading=trading_player_names,
                    players_receiving=receiving_player_names)