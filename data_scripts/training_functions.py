from get_data import download_games_for_tournament
from create_feature_vectors import get_tournament_feature_vectors
from weighter import Weighter
import pandas as pd

# Returns dataframe of vectors

def create_final_vectors(features):
    # features 0 is a game, features[0][0] is a team

    column_names =   ["participantID", "level", "shutdownValue", "totalGold", "MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED", 
                      "NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE", "NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE", 
                      "CHAMPIONS_KILLED", "NUM_DEATHS", "ASSISTS", "WARD_PLACED", "WARD_KILLED", "VISION_SCORE", "TOTAL_DAMAGE_DEALT",
                      "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", "TOTAL_DAMAGE_TAKEN", "TOTAL_DAMAGE_SELF_MITIGATED", "TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES", 
                      "TOTAL_DAMAGE_DEALT_TO_BUILDINGS", "TOTAL_DAMAGE_DEALT_TO_TURRETS", "TOTAL_DAMAGE_DEALT_TO_OBJECTIVES", 
                      "TOTAL_TIME_CROWD_CONTROL_DEALT_TO_CHAMPIONS", "TOTAL_HEAL_ON_TEAMMATES", "RESULT"]

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

            feature_vectors = team[1]
            print(len(feature_vectors))
            for vector in feature_vectors:
                vector.append(match_result)
                df.loc[len(df)] = vector       

    return df


# TODO main training function, needs to:
# 1. Take in a list of tournament ID's to get the games from
# 2. Train a model on the feature vectors from that game
# 3. Log important info acc, loss, etc. to wandb
# 4. Save weights from model

def train_model(tournaments, download_games):
    
    column_names =   ["participantID", "level", "shutdownValue", "totalGold", "MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED", 
                      "NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE", "NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE", 
                      "CHAMPIONS_KILLED", "NUM_DEATHS", "ASSISTS", "WARD_PLACED", "WARD_KILLED", "VISION_SCORE", "TOTAL_DAMAGE_DEALT",
                      "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", "TOTAL_DAMAGE_TAKEN", "TOTAL_DAMAGE_SELF_MITIGATED", "TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES", 
                      "TOTAL_DAMAGE_DEALT_TO_BUILDINGS", "TOTAL_DAMAGE_DEALT_TO_TURRETS", "TOTAL_DAMAGE_DEALT_TO_OBJECTIVES", 
                      "TOTAL_TIME_CROWD_CONTROL_DEALT_TO_CHAMPIONS", "TOTAL_HEAL_ON_TEAMMATES", "RESULT"]

    model = Weighter()
    final_vectors_df = pd.DataFrame(columns=column_names)

    for tournament in tournaments:
        if download_games:
            download_games_for_tournament(tournament)
        feature_vectors = get_tournament_feature_vectors(tournament)
        vectors_df = create_final_vectors(feature_vectors)
        final_vectors_df.append(vectors_df)


    # Train model!!! Reference weighter class from paper
    model.fit(final_vectors_df, "RESULT")

if __name__ == "__main__":

    # Test get_tournament_feature_vectors
    df = train_model(["110733838935136200"], False)
