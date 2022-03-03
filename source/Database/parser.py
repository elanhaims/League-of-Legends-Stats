from .mappings import Game, Participant
from datetime import datetime


def parse_game(game, summoners):
    game_info = game['info']
    date_occurred = datetime.fromtimestamp(game_info['gameCreation'] / 1e3)
    game_duration = game_info['gameDuration']
    match_id = game['metadata']['matchId']
    won_game = [participant['win'] for participant in game_info['participants'] if participant['summonerName']
                in summoners][0]

    participants = []
    for participant in game_info['participants']:
        if participant['summonerName'] in summoners:
            participant = parse_participant(participant, match_id)
            participants.append(participant)

    game = Game(id=match_id, date=date_occurred, duration=game_duration, won=won_game, participants=participants)
    return game


def parse_participant(participant, match_id):
    name = participant['summonerName']
    participant_id = match_id + name
    champion = participant['championName']
    damage = participant['totalDamageDealtToChampions']
    won = participant['win']
    kills = participant['kills']
    deaths = participant['deaths']
    pentakills = participant['pentaKills']
    quadrakills = participant['quadraKills']

    participant = Participant(id=participant_id, summoner_name=name, champion=champion, won=won, kills=kills,
                              deaths=deaths, damage=damage, pentakills=pentakills, quadrakills=quadrakills,
                              game_id=match_id)
    return participant


def parse_games(games, summoners):
    parsed_games = []
    for game in games:
        parsed_games.append(parse_game(game, summoners))

    return parsed_games


def get_team_id(participants, summoner):
    for participant in participants:
        if participant['summonerName'] == summoner:
            return participant['teamId']

    raise Exception("Could not find summoner with that name")
