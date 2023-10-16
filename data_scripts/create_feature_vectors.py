from data_helper_functions import get_mapping
from data_helper_functions import get_team
from data_helper_functions import get_tournament
from data_helper_functions import get_game_data


# Create a feature vector for a given player to feed to the ML model
# Written this way so it's not all one massive for loop

def create_game_meta_data(tournament_game_data, tournament_team_data, gamefile_player_data, mapping):

    # {Team data: 
    #       ID, Name, Side, Win/Loss
    # }
    # {Player data: 
    #       Player, champion, summonerName, role
    # }

    metadata = {"team": {}, "players": {}}

    # Create team data
    team_id = tournament_team_data["id"]

    metadata["team"]["id"] = team_id
    metadata["team"]["name"] = get_team(tournament_team_data["id"])["name"]
    
    for team in tournament_game_data["teams"]:
        if team["id"] == team_id:
            metadata["team"]["side"] = team["side"]
            metadata["team"]["result"] = team["result"]["outcome"]

    # Create player data
    new_players = mapping["participantMapping"]
    players = {}

    team_side = 200
    if metadata["team"]["side"] == "blue":
        team_side = 100

    for key in new_players:
        player_id = new_players[key]

        for player in gamefile_player_data:
            if player["participantID"] == int(key) and player["teamID"] == team_side:
                 players[key] = {"id" : player_id, "champion" : player["championName"], "summonerName" : player["summonerName"]}
                 break
        
        for player in tournament_team_data["players"]:
            if player["id"] == player_id:
                players[key]["role"] = player["role"]
                break
        
    metadata["players"] = players

    return metadata


def create_participant_feature_vector(participant_data):
    feature_vector = []
    relevant_stats = ["MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE", "NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE", 
                      "CHAMPIONS_KILLED", "NUM_DEATHS", "ASSISTS", "WARD_PLACED", "WARD_KILLED", "VISION_SCORE", "TOTAL_DAMAGE_DEALT",
                      "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", "TOTAL_DAMAGE_TAKEN", "TOTAL_DAMAGE_SELF_MITIGATED", "TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES", 
                      "TOTAL_DAMAGE_DEALT_TO_BUILDINGS", "TOTAL_DAMAGE_DEALT_TO_TURRETS", "TOTAL_DAMAGE_DEALT_TO_OBJECTIVES", 
                      "TOTAL_TIME_CROWD_CONTROL_DEALT_TO_CHAMPIONS", "TOTAL_HEAL_ON_TEAMMATES"]

    # Append relevant features
    feature_vector.append(participant_data["participantID"])
    feature_vector.append(participant_data["level"])
    feature_vector.append(participant_data["shutdownValue"])
    feature_vector.append(participant_data["totalGold"])

    # Append relevant stats features
    for stat in participant_data["stats"]:
        if stat["name"] in relevant_stats:
            feature_vector.append(stat["value"])

    return feature_vector

def create_feature_vectors(game, keys):

    # Just one relevant typr for now, will likely add more later
    relevant_event_types = ["stats_update"]
    feature_vectors = []
    
    # Create a feature vector for all players on a team T in a given game M
    # TODO Check each event type and get relevant data from event

    for dictionary in game:
        event_type = dictionary["eventType"]
        if  event_type in relevant_event_types:
            if event_type == "stats_update":
                if dictionary["gameOver"] == True:
                    for participant in dictionary["participants"]:
                        if str(participant["participantID"]) in keys:
                            participant_feature_vector = create_participant_feature_vector(participant)
                            feature_vectors.append(participant_feature_vector)
            else:
                continue

    return feature_vectors

# extracts the performance vector of team T in match M
# performance vector is calculated by summing all corresponding features for each player on team T in match M
# basically calculate a performance vector for each player on the team and sum them to get the team performance vector

def get_team_feature_vectors(game, team, mapping):
    game_data = get_game_data(mapping["platformGameId"])
    metadata = create_game_meta_data(game, team, game_data[0]["participants"], mapping)
    keys = []

    for key in metadata["players"]:
        keys.append(key)

    player_feature_vectors = create_feature_vectors(game_data, keys)   

    return [metadata, player_feature_vectors]

def get_game_feature_vectors(game, teams):
    mapping = get_mapping(game["id"])

    if isinstance(mapping, str):
        return "Game mapping doesn't exist."
    
    # TODO make sure teams[0] is blue and teams[1] is red
    
    blue_team_feature_vectors = get_team_feature_vectors(game, teams[0], mapping)
    red_team_feature_vectors = get_team_feature_vectors(game, teams[1], mapping)

    return [red_team_feature_vectors, blue_team_feature_vectors]

def get_tournament_feature_vectors(tournamentID):
    tournament = get_tournament(tournamentID)
    game_counter = 0
    load_failed_count = 0
    tournament_feature_vectors = []

    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                teams = match["teams"]
                for game in match["games"]:
                    if game["state"] == "completed":
                        try:
                            tournament_feature_vectors.append(get_game_feature_vectors(game, teams))
                        except:
                            print(f"Game {game_counter} could not be loaded, continuing...")
                            load_failed_count += 1
                            continue
                        if game_counter == 5:
                            return tournament_feature_vectors


                        
                        game_counter += 1
                        print(f"Games loaded: {game_counter}")
  

    tournament_slug = tournament["slug"]
    print(f"Total Games For {tournament_slug}: {game_counter}")
    print(f"Total Games Failed To Load For {tournament_slug}: {load_failed_count}")
    return tournament_feature_vectors


if __name__ == "__main__":

    # Test get_tournament_feature_vectors
    print("Testing get_tournament_feature_vectors:\n")
    tournament_feature_vectors = get_tournament_feature_vectors("110733838935136200")
    print("Should be:\n83\n")
    print("Returned:")
    print(len(tournament_feature_vectors))

    print(tournament_feature_vectors[0][0])


  

