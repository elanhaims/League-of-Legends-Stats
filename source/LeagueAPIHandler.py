import requests
from Database import database

APIKEY = "Left Blank"
PLATFORM = "na1"
REGION = "americas"
SUMMONER = "terice1"

SUMMONERS = ["terice1", "Mrs Fizzle", "kickboy9", "yeehaw342", "QuadForm"]


def getAccount(summonerName):
    url = "https://" + PLATFORM + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + \
          "?api_key=" + APIKEY
    response = requests.get(url)
    return response.json()


def getMatchesForAccount(puuid, numMatches=20):
    url = "https://" + "americas" + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?api_key=" + \
          APIKEY + '&queue=450&count=' + str(numMatches) + '&start=0'
    response = requests.get(url)
    return response.json()


def getMatchByID(match_id):
    url = "https://" + "americas.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + APIKEY
    response = requests.get(url)
    return response.json()


def getMatchIDsForUser(summoner_name, num_matches=20):
    account = getAccount(summoner_name)
    if 'puuid' not in account:
        raise Exception("Could not find account with that summoner name")
    puuid = account['puuid']

    match_ids = getMatchesForAccount(puuid, num_matches)

    new_match_ids = list(filter(database.match_id_not_in_table, match_ids))
    return list(new_match_ids)


def getMatchesFromMatchIDs(match_ids):
    matches = []
    for match_id in match_ids:
        match = getMatchByID(match_id)
        matches.append(match)

    return matches


def getMatchesForUser(summoner_name, num_matches=20):
    match_ids = getMatchIDsForUser(summoner_name, num_matches)

    print(f"Adding {len(match_ids)} match ids")
    matches = getMatchesFromMatchIDs(match_ids)

    return matches


def getLastMatchIDsForUser(summoner_name, num_matches=1):
    match_id = getMatchIDsForUser(summoner_name, num_matches)

    return match_id
