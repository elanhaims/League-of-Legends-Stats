from .base import Session, engine, Base
from .mappings import Game, Participant
from sqlalchemy import func
from sqlalchemy.sql import label
from collections import Counter

Base.metadata.create_all(engine)

"""Check existence of games in table"""


def check_if_match_id_in_table(match_id):
    with Session() as session:
        exists = session.query(Game).filter(Game.id == match_id).first() is not None
    return exists


def match_id_not_in_table(match_id):
    with Session() as session:
        exists = session.query(Game).filter(Game.id == match_id).first() is not None
    return not exists


def check_if_game_in_table(game):
    with Session() as session:
        exists = session.query(Game).filter(Game.id == game.id).first() is not None

    return exists


"""Add Game instances to table"""


def add_game_to_table(game):
    if check_if_game_in_table(game):
        print("Game was already in table")
        return
    with Session() as session, session.begin():
        session.add(game)


def add_games_to_table(games):
    for game in games:
        add_game_to_table(game)


"""Get Rates for player"""


def get_win_rate_for_player(player_name):
    number_of_games = get_number_of_games_played_for_player(player_name)
    number_of_wins = get_number_of_wins_for_player(player_name)
    winrate = number_of_wins / number_of_games if number_of_games != 0 else 0
    return number_of_games, number_of_wins, winrate


def get_win_rate_for_players(player1, player2):
    games = get_games_with_players(player1, player2)

    games_query = games.subquery()

    number_of_wins = get_number_of_wins_for_player(player1, games_query)
    number_of_games = get_number_of_games_played_for_player(player1, games_query)
    win_rate = number_of_wins / number_of_games if number_of_games != 0 else 0
    return number_of_games, number_of_wins, win_rate


def get_most_damage_rate_for_player(player_name):
    number_of_games = get_number_of_games_played_for_player(player_name)
    number_of_times_most_damage = get_num_times_most_damage_for_player(player_name)
    damage_rate = number_of_times_most_damage / number_of_games if number_of_games != 0 else 0
    return number_of_games, number_of_times_most_damage, damage_rate


def get_most_damage_rate_for_player1_with_player2(player1, player2):
    games = get_games_with_players(player1, player2)
    games_query = games.subquery()
    number_of_games = get_number_of_games_played_for_player(player1, games_query)
    number_of_time_most_damage = get_num_times_most_damage_for_player(player1, games_query)
    damage_rate = number_of_time_most_damage / number_of_games if number_of_games != 0 else 0
    return number_of_games, number_of_time_most_damage, damage_rate


def get_winrate_when_most_damage_for_player(player_name, table=Game):
    participants = get_participant_when_most_damage(player_name, table)
    subq = participants.subquery()
    with Session() as session, session.begin():
        wins_when_most_damage = session.query(subq).filter(subq.c.summoner_name == player_name). \
            filter(subq.c.won == True).count()
        number_of_games = session.query(subq).count()
    winrate_when_most_damage = wins_when_most_damage / number_of_games if number_of_games != 0 else 0
    return number_of_games, wins_when_most_damage, winrate_when_most_damage


def get_winrate_when_most_damage_for_player1_with_player2(player1, player2):
    games = get_games_with_players(player1, player2)
    games_query = games.subquery()

    return get_winrate_when_most_damage_for_player(player1, games_query)


def get_champs_played_when_most_damage_for_player(player_name):
    participants = get_participant_when_most_damage(player_name)
    subq = participants.subquery()
    with Session() as session, session.begin():
        champions = session.query(subq.c.champion)

    champs = [champ.champion for champ in champions]
    champ_dict = Counter(champs)
    sorted_dict = sort_dict(champ_dict)
    return sorted_dict


"""Get number of for player"""


def get_number_of_games_played_for_player(player_name, table=Game):
    with Session() as session, session.begin():
        if table == Game:
            table = session.query(Game).subquery()
        games_count = session.query(Game).filter(Game.id == table.c.id) \
            .filter(Game.participants.any(Participant.summoner_name == player_name)).count()

        return games_count


def get_number_of_wins_for_player(player_name, table=Game):
    with Session() as session, session.begin():
        if table == Game:
            table = session.query(Game).subquery()

        wins_count = session.query(Game).filter(Game.id == table.c.id) \
            .filter(Game.participants.any(Participant.summoner_name == player_name)) \
            .filter(Game.participants.any(Participant.won == True)).count()
        return wins_count


def get_num_times_most_damage_for_player(player_name, table=Game):
    with Session() as session, session.begin():
        if table == Game:
            table = session.query(Game).subquery()

        participants = get_participant_when_most_damage(player_name, table)
        subq = participants.subquery()

        num_times_most_damage = session.query(subq).count()

        return num_times_most_damage


def get_champions_played_for_player(player_name):
    with Session() as session, session.begin():
        champions = session.query(Participant.champion).select_from(Participant). \
            filter(Participant.summoner_name == player_name)

    champions = [champ.champion for champ in champions]
    champ_dict = Counter(champions)
    filtered_dict = dict(filter(lambda x: x[1] >= 3, champ_dict.items()))
    sorted_dict = sort_dict(filtered_dict)
    return sorted_dict


def get_games_with_players(player1, player2):
    with Session() as session, session.begin():
        games = session.query(Game).filter(Game.participants.any(Participant.summoner_name == player1)). \
            filter((Game.participants.any(Participant.summoner_name == player2)))

    return games


def get_participant_when_most_damage(player_name, table=Game):
    with Session() as session, session.begin():
        if table == Game:
            table = session.query(table).subquery()

        max_damage = session.query(Participant.game_id, label('max_damage', func.max(Participant.damage))). \
            select_from(Participant).join(table, table.c.id == Participant.game_id).group_by(Participant.game_id)

        subq1 = max_damage.subquery()

        all_participants = session.query(Participant).join(subq1, Participant.game_id == subq1.c.game_id). \
            filter(Participant.game_id == subq1.c.game_id).filter(Participant.damage == subq1.c.max_damage)

        subq2 = all_participants.subquery()
        res = session.query(subq2).filter(subq2.c.summoner_name == player_name)

        return res


def get_max_damage_for_player(player_name):
    with Session() as session, session.begin():
        max_val = session.query(func.max(Participant.damage)).filter(Participant.summoner_name == player_name).scalar()
    return max_val


def get_average_damage_for_player(player_name):
    with Session() as session, session.begin():
        average = session.query(func.avg(Participant.damage)).filter(Participant.summoner_name == player_name).scalar()
    return average


def get_pentakills_for_player(player_name):
    with Session() as session, session.begin():
        num_pentakills = session.query(func.sum(Participant.pentakills)) \
            .filter(Participant.summoner_name == player_name).scalar()
    return num_pentakills


def get_quadrakills_for_player(player_name):
    with Session() as session, session.begin():
        num_quadrakills = session.query(func.sum(Participant.quadrakills)) \
            .filter(Participant.summoner_name == player_name).scalar()
    return num_quadrakills


def get_max_kills_for_player(player_name):
    with Session() as session, session.begin():
        max_val = session.query(func.max(Participant.kills)).filter(Participant.summoner_name == player_name).scalar()
    return max_val


def get_average_kills_for_player(player_name):
    with Session() as session, session.begin():
        avg = session.query(func.avg(Participant.kills)).filter(Participant.summoner_name == player_name).scalar()
    return avg


def get_max_deaths_for_player(player_name):
    with Session() as session, session.begin():
        max_val = session.query(func.max(Participant.deaths)).filter(Participant.summoner_name == player_name).scalar()
    return max_val


def get_average_deaths_for_player(player_name):
    with Session() as session, session.begin():
        avg = session.query(func.avg(Participant.deaths)).filter(Participant.summoner_name == player_name).scalar()
    return avg


def sort_dict(_dict):
    sorted_dict = {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1], reverse=True)}
    return sorted_dict
