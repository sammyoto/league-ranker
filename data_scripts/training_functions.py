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
            for vector in feature_vectors:
                vector.append(match_result)
                df.loc[len(df)] = vector       

    return df


# TODO main training function, needs to:
# 1. Take in a list of tournament ID's to get the games from
# 2. Train a model on the feature vectors from that game
# 3. Log important info acc, loss, etc. to wandb
# 4. Save weights from model

def train_model(tournaments, download_games, load_from_csv):
    
    column_names =   ["level", "shutdownValue", "totalGold", "MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED", 
                      "NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE", "NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE", 
                      "CHAMPIONS_KILLED", "NUM_DEATHS", "ASSISTS", "WARD_PLACED", "WARD_KILLED", "VISION_SCORE", "TOTAL_DAMAGE_DEALT",
                      "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", "TOTAL_DAMAGE_TAKEN", "TOTAL_DAMAGE_SELF_MITIGATED", "TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES", 
                      "TOTAL_DAMAGE_DEALT_TO_BUILDINGS", "TOTAL_DAMAGE_DEALT_TO_TURRETS", "TOTAL_DAMAGE_DEALT_TO_OBJECTIVES", 
                      "TOTAL_TIME_CROWD_CONTROL_DEALT_TO_CHAMPIONS", "TOTAL_HEAL_ON_TEAMMATES", "RESULT"]

    weighter = Weighter()

    #load the data and format in dataframe
    if load_from_csv:
        final_vectors_df = pd.read_csv("data/df_csv/out.csv", index_col=[0])
    else:
        final_vectors_df = pd.DataFrame(columns=column_names)

        for tournament in tournaments:
            if download_games:
                download_games_for_tournament(tournament)
            feature_vectors = get_tournament_feature_vectors(tournament)
            vectors_df = create_final_vectors(feature_vectors)
            final_vectors_df = pd.concat([final_vectors_df, vectors_df])

    #splt data into test and train
    X = final_vectors_df.loc[:, final_vectors_df.columns != "RESULT"].values
    y = final_vectors_df["RESULT"].values

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)

    #fit the model
    weighter.fit(column_names=column_names[:-1], Xtrain=Xtrain, ytrain=ytrain, scaled=False)
    
    accuracy_score = weighter.clf_.score(Xtest, ytest)
    print(f"Accuracy Score: {accuracy_score}\n")

    if not load_from_csv:
        filepath = Path('data/df_csv/out.csv') 
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        final_vectors_df.to_csv(filepath) 

    return weighter

if __name__ == "__main__":

    # Test get_tournament_feature_vectors
    train_model(["110733838935136200"], False, True)
