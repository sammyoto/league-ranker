from get_data import download_games_for_tournament
from create_feature_vectors import get_tournament_feature_vectors
from sklearn.model_selection import train_test_split
from weighter import Weighter
from pathlib import Path
import pandas as pd

# Returns dataframe of vectors

def create_final_vectors(features):
    # features 0 is a game, features[0][0] is a team

    column_names =   ["level", "shutdownValue", "totalGold", "MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED", 
                      "NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE", "NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE", 
                      "CHAMPIONS_KILLED", "NUM_DEATHS", "ASSISTS", "WARD_PLACED", "WARD_KILLED", "VISION_SCORE", "TOTAL_DAMAGE_DEALT",
                      "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", "TOTAL_DAMAGE_TAKEN", "TOTAL_DAMAGE_SELF_MITIGATED", "TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES", 
                      "TOTAL_DAMAGE_DEALT_TO_BUILDINGS", "TOTAL_DAMAGE_DEALT_TO_TURRETS", "TOTAL_DAMAGE_DEALT_TO_OBJECTIVES", 
                      "TOTAL_TIME_CROWD_CONTROL_DEALT_TO_CHAMPIONS", "TOTAL_HEAL_ON_TEAMMATES", "participantID", "CHAMPION", "SUMMONER_NAME", 
                      "ESPORTS_ID", "PLATFORM_ID", "SIDE", "RESULT"]

    df = pd.DataFrame(columns=column_names)

    for game in features:

        team_1_vectors = game[0][1]
        team_2_vectors = game[1][1]

        # Make sure game is 5v5, otherwise throw it out

        if len(team_1_vectors) < 5 or len(team_2_vectors) < 5:
            continue

        for team in game:
            match_result = team[0]["team"]["result"]

            if match_result == "loss":
                match_result = 0
            else:
                match_result = 1

            #append all necessary data
            metadata = team[0]
            esports_id = metadata["team"]["esportsGameId"]
            platform_id = metadata["team"]["platformGameId"]
            side = metadata["team"]["side"]

            feature_vectors = team[1]

            for vector in feature_vectors:
                participant_id = vector[23]
                player = metadata["players"][participant_id]
                
                # Appends
                vector.append(player["champion"])
                vector.append(player["summonerName"])
                vector.append(esports_id)
                vector.append(platform_id)
                vector.append(side)
                vector.append(match_result)
                df.loc[len(df)] = vector       

    return df

# downloads games for a list of tournaments, creates feature vectors, and saves features vectors to csv
def load_data_to_csv(tournaments):
    column_names =   ["level", "shutdownValue", "totalGold", "MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED", 
                      "NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE", "NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE", 
                      "CHAMPIONS_KILLED", "NUM_DEATHS", "ASSISTS", "WARD_PLACED", "WARD_KILLED", "VISION_SCORE", "TOTAL_DAMAGE_DEALT",
                      "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", "TOTAL_DAMAGE_TAKEN", "TOTAL_DAMAGE_SELF_MITIGATED", "TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES", 
                      "TOTAL_DAMAGE_DEALT_TO_BUILDINGS", "TOTAL_DAMAGE_DEALT_TO_TURRETS", "TOTAL_DAMAGE_DEALT_TO_OBJECTIVES", 
                      "TOTAL_TIME_CROWD_CONTROL_DEALT_TO_CHAMPIONS", "TOTAL_HEAL_ON_TEAMMATES", "participantID", "CHAMPION", "SUMMONER_NAME", 
                      "ESPORTS_ID", "PLATFORM_ID", "SIDE", "RESULT"]
    
    final_vectors_df = pd.DataFrame(columns=column_names)

    checkpoint_num = 0
    tournaments_loaded = 0

    for tournament in tournaments:
        download_games_for_tournament(tournament)
        feature_vectors = get_tournament_feature_vectors(tournament)
        vectors_df = create_final_vectors(feature_vectors)
        final_vectors_df = pd.concat([final_vectors_df, vectors_df])

        tournaments_loaded += 1

        if tournaments_loaded % 5 == 0:
                path = f'data/df_csv/features{checkpoint_num}.csv'
                filepath = Path(path)
                filepath.parent.mkdir(parents=True, exist_ok=True)  
                final_vectors_df.to_csv(filepath)
                checkpoint_num += 1


    filepath = Path('data/df_csv/features_final.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    final_vectors_df.to_csv(filepath)

if __name__ == "__main__":

    # Test get_tournament_feature_vectors
    load_data_to_csv(["110733838935136200"])
