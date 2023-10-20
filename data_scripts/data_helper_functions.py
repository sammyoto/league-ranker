import json

# Helper Functions

# Actually just opens the file and returns a list of JSON objects
def get_JSON_dict(filepath):
   f = open(filepath, "r")
   data = json.load(f)
   f.close()
   return data

def get_all_keys(data):
  keys = []
  for json in data:
    for key in json.keys():
      if key not in keys:
        keys.append(key)
  return keys


# GET functions

def get_participant(participantID, filepath="data/esports-data/players.json"):
    data = get_JSON_dict(filepath)

    for player in data:
       if player["player_id"] == participantID:
          return player
       
    return "Participant Not Found"

def get_team(teamID, filepath="data/esports-data/teams.json"):
    data = get_JSON_dict(filepath)

    for team in data:
       if team["team_id"] == teamID:
          return team
       
    return "Team Not Found"

def get_league(leagueID, filepath="data/esports-data/leagues.json"):
    data = get_JSON_dict(filepath)

    for league in data:
       if league["id"] == leagueID:
          return league
    
    return "League Not Found"

def get_tournament(tournamentID, filepath="data/esports-data/tournaments.json"):
    data = get_JSON_dict(filepath)

    for tournament in data:
       if tournament["id"] == tournamentID:
          return tournament
       
    return "Tournament Not Found"

def get_mapping(esportsID, filepath="data/esports-data/mapping_data.json"):
    data = get_JSON_dict(filepath)

    for mapping in data:
       if mapping["esportsGameId"] == esportsID:
          return mapping
       
    return "Mapping Not Found"

def get_game_data(platformGameId):
   try:
      data = get_JSON_dict(f"data/games/{platformGameId}.json")
      return data
   except:
      return "Game Not Found"
   
def get_tournament_ids_by_year(year, filepath="data/esports-data/tournaments.json"):
   data = get_JSON_dict(filepath)

   tournament_ids = []
   
   for tournament in data:
       start_date = tournament.get("startDate", "")
       if start_date.startswith(str(year)):
          tournament_ids.append(tournament["id"])

   return tournament_ids


# TESTS
if __name__ == "__main__":

   #Get player data
   print("Testing get participant:\n")
   participant = get_participant("99921042949122311")
   print("Should be:\nSkanito\n")
   print("Returned:")
   print(participant["handle"])

   #Get team data
   print("\nTesting get team:\n")
   team = get_team("107582169874155554")
   print("Should be:\nGod's Plan\n")
   print("Returned:")
   print(team["name"])

   #Get league data
   print("\nTesting get league:\n")
   league = get_league("98767991299243165")
   print("Should be:\nLCS\n")
   print("Returned:")
   print(league["name"])

   #Get tournament data
   print("\nTesting get tournament:\n")
   tournament = get_tournament("110733838935136200")
   print("Should be:\nnacl_qualifiers_2_summer_2023\n")
   print("Returned:")
   print(tournament["slug"])

   #Get mapping data
   print("\nTesting get mapping:\n")
   mapping = get_mapping("110378429158160389")
   print("Should be:\nESPORTSTMNT01:3416295\n")
   print("Returned:")
   print(mapping["platformGameId"])

   #Get game data
   print("\nTesting get game data:\n")
   game_data = get_game_data("ESPORTSTMNT03:3196037")
   print("Should be:\nESPORTSTMNT03:3196037\n")
   print("Returned:")
   print(game_data[0]["platformGameId"])