from drews_fantasy_sports_helper import app

if __name__ == '__main__':
    app.run(debug=True)

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'This is a Fantasy Sports app'


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


# print("Projecting next week's matchup")
# pprint(project_matchup(ANDREW_ID, 
#                        VIJAY_ID, 
#                        PLAYER_AVG_STAT_INTERVALS.LAST_15, 
#                        (None, 'Bradley Beal')))

# print("Projecting how you currently stand against Lucas")
# pprint(project_matchup(ANDREW_ID, 
#                        LUCAS_ID, 
#                        PLAYER_AVG_STAT_INTERVALS.LAST_15, 
#                        (None, 'Mitchell Robinson')))
# print('Projecting Matchups')
# generate_all_projections(ANDREW_ID, PLAYER_AVG_STAT_INTERVALS.LAST_30)
## compare trade for player

## stretch goals: TRADE TARGETS TO BEST IMPROVE TEAM

## stretch goal: identify which player to trade on your team