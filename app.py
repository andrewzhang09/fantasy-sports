from drews_fantasy_sports_helper import app

if __name__ == '__main__':
    app.run(debug=True)


# ## DEPRECATED
# def get_opponent_team_id(id1, matchup_num):
#     team1_sched = TEAM_MAP.get(id1).get('schedule')
#     home_team = team1_sched[matchup_num - 1].home_team
#     # if YOUR team is home team
#     if home_team.team_id == id1:
#         opponent = team1_sched[matchup_num - 1].away_team
#     else:
#         opponent = home_team
#     return opponent.team_id

## stretch goals: TRADE TARGETS TO BEST IMPROVE TEAM

## stretch goal: identify which player to trade on your team