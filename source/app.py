import json

from flask import Flask, render_template
import LeagueAPIHandler
from Database import database, parser
from threading import Timer

SUMMONERS = ["terice1", "Mrs%20Fizzle", "kickboy9", "yeehaw342", "QuadForm"]

app = Flask(__name__)


@app.route('/admin/retrieveMatchesForPlayer/<string:summoner_name>/<int:num_matches>', methods=['GET'])
def retrieve_matches_for_player(summoner_name, num_matches):
    matches = LeagueAPIHandler.getMatchesForUser(summoner_name, num_matches)
    parsed_matches = parser.parse_games(matches, SUMMONERS)
    database.add_games_to_table(parsed_matches)
    return "Success!"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getGamesPlayed/<string:player>', methods=['GET'])
def get_num_games_played_for_player(player):
    games_played = database.get_number_of_games_played_for_player(player)
    _dict = {player: games_played}
    return json.dumps(games_played)


@app.route('/getWinrate/<string:player>', methods=['GET'])
def get_winrate_for_player(player):
    num_games, num_wins, winrate = database.get_win_rate_for_player(player)
    _dict = {'num_games': num_games, 'num_wins': num_wins, 'winrate': format_as_percent(winrate)}
    return json.dumps(_dict)


@app.route('/getDamageRate/<string:player>', methods=['GET'])
def get_most_damage_rate_for_player(player):
    num_games, num_times_most_damage, most_damage_rate = database.get_most_damage_rate_for_player(player)
    _dict = {'num_games': num_games, 'times_most_damage': num_times_most_damage,
             'damage_rate': format_as_percent(most_damage_rate)}
    return json.dumps(_dict)


@app.route('/getDamageRateTwoPlayers/<string:player1>/<string:player2>', methods=['GET'])
def get_most_damage_rate_for_player1_with_player2(player1, player2):
    num_games, num_times_most_damage, damage_rate = database.get_most_damage_rate_for_player1_with_player2(player1,
                                                                                                           player2)
    _dict = {'num_games': num_games, 'num_times_most_damage': num_times_most_damage,
             'damage_rate': format_as_percent(damage_rate)}
    return json.dumps(_dict)


@app.route('/getWinrateWhenMostDamage/<string:player>', methods=['GET'])
def get_winrate_when_most_damage_for_player(player):
    num_games, num_wins, winrate = database.get_winrate_when_most_damage_for_player(player)
    _dict = {'num_games': num_games, 'num_wins': num_wins, 'winrate': format_as_percent(winrate)}
    return json.dumps(_dict)


@app.route('/getWinrateWhenMostDamageTwoPlayers/<string:player1>/<string:player2>', methods=['GET'])
def get_winrate_when_most_damage_two_players(player1, player2):
    num_games, num_wins, winrate = database.get_winrate_when_most_damage_for_player1_with_player2(player1, player2)
    _dict = {'num_games': num_games, 'num_wins': num_wins, 'winrate': format_as_percent(winrate)}
    return json.dumps(_dict)


@app.route('/getWinrateForPlayers/<string:player1>/<string:player2>', methods=['GET'])
def get_win_rate_for_players(player1, player2):
    games, wins, winrate = database.get_win_rate_for_players(player1, player2)
    _dict = {"games": games, "wins": wins, "winrate": format_as_percent(winrate)}
    return json.dumps(_dict)


@app.route('/getChampsPlayed/<string:player>', methods=['GET'])
def get_champs_played_for_player(player):
    champs = database.get_champions_played_for_player(player)
    return json.dumps(champs, sort_keys=False)


@app.route('/getChampsPlayedWhenMostDamage/<string:player>', methods=['GET'])
def get_champs_played_when_most_damage(player):
    champs = database.get_champs_played_when_most_damage_for_player(player)
    return json.dumps(champs, sort_keys=False)


@app.route('/getDamageStats/<string:player>', methods=['GET'])
def get_damage_stats_for_player(player):
    average_damage = database.get_average_damage_for_player(player)
    max_damage = database.get_max_damage_for_player(player)
    _dict = {"average_damage": dec_to_str(average_damage), "max_damage": dec_to_str(max_damage)}
    return json.dumps(_dict)


@app.route('/getKillStats/<string:player>', methods=['GET'])
def get_kill_stats_for_player(player):
    average_kills = database.get_average_kills_for_player(player)
    max_kills = database.get_max_kills_for_player(player)
    _dict = {"average_kills": dec_to_str(average_kills), "max_kills": dec_to_str(max_kills)}
    return json.dumps(_dict)


@app.route('/getDeathStats/<string:player>', methods=['GET'])
def get_death_stats_for_player(player):
    average_deaths = database.get_average_deaths_for_player(player)
    max_deaths = database.get_max_deaths_for_player(player)
    _dict = {"average_deaths": dec_to_str(average_deaths), "max_deaths": dec_to_str(max_deaths)}
    return json.dumps(_dict)


@app.route('/getMultikills/<string:player>', methods=['GET'])
def get_multikills_for_player(player):
    pentakills = database.get_pentakills_for_player(player)
    quadrakills = database.get_quadrakills_for_player(player)
    _dict = {"pentakills": pentakills, "quadrakills": quadrakills}
    return json.dumps(_dict)


def format_as_percent(value):
    return "{:.1%}".format(value)


def dec_to_str(value):
    return str(round(value, 2))


def add_recent_game():
    total_match_ids = []
    for summoner in SUMMONERS:
        match_ids = LeagueAPIHandler.getLastMatchIDsForUser(summoner, 10)
        for match_id in match_ids:
            total_match_ids.append(match_id)
    total_match_ids = list(set(total_match_ids))
    matches = LeagueAPIHandler.getMatchesFromMatchIDs(total_match_ids)
    parsed_matches = parser.parse_games(matches, SUMMONERS)
    database.add_games_to_table(parsed_matches)
    if len(parsed_matches):
        print(f"Adding {len(parsed_matches)} game{'s' * (len(parsed_matches) > 1)} to database")
    timer = Timer(interval=600, function=add_recent_game)
    timer.daemon = True
    timer.start()


add_recent_game()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
