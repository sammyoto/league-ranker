import requests
import json
import gzip
import shutil
import time
import os
from data_helper_functions import get_tournament
from data_helper_functions import get_mapping
from io import BytesIO

S3_BUCKET_URL = "https://power-rankings-dataset-gprhack.s3.us-west-2.amazonaws.com"

def download_gzip_and_write_to_json(file_name):
   # If file already exists locally do not re-download game
   if not os.path.exists("data"):
       os.makedirs("data")

   if os.path.isfile(f"data/{file_name}.json"):
       return

   response = requests.get(f"{S3_BUCKET_URL}/{file_name}.json.gz")
   if response.status_code == 200:
       try:
           gzip_bytes = BytesIO(response.content)
           with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
               with open(f"data/{file_name}.json", 'wb') as output_file:
                   shutil.copyfileobj(gzipped_file, output_file)
       except Exception as e:
           print("Error:", e)
   else:
       print(f"Failed to download {file_name}")

def download_esports_files():
   directory = "esports-data"
   if not os.path.exists("data/esports-data"):
       os.makedirs("data/esports-data")

   esports_data_files = ["leagues", "tournaments", "players", "teams", "mapping_data"]
   for file_name in esports_data_files:
       download_gzip_and_write_to_json(f"{directory}/{file_name}")

def download_games(year):
   start_time = time.time()
   with open("data/esports-data/tournaments.json", "r") as json_file:
       tournaments_data = json.load(json_file)
   with open("data/esports-data/mapping_data.json", "r") as json_file:
       mappings_data = json.load(json_file)

   directory = "games"
   if not os.path.exists("data/games"):
       os.makedirs("data/games")

   mappings = {
       esports_game["esportsGameId"]: esports_game for esports_game in mappings_data
   }
        
   game_counter = 0

   for tournament in tournaments_data:
       start_date = tournament.get("startDate", "")
       if start_date.startswith(str(year)):
           print(f"Processing {tournament['slug']}")
           for stage in tournament["stages"]:
               for section in stage["sections"]:
                   for match in section["matches"]:
                       for game in match["games"]:
                           if game["state"] == "completed":
                               try:
                                   platform_game_id = mappings[game["id"]]["platformGameId"]
                               except KeyError:
                                   print(f"{platform_game_id} {game['id']} not found in the mapping table")
                                   continue

                               download_gzip_and_write_to_json(f"{directory}/{platform_game_id}")
                               game_counter += 1


                           if game_counter % 10 == 0:
                               print(
                                   f"----- Processed {game_counter} games, current run time: \
                                   {round((time.time() - start_time)/60, 2)} minutes"
                               )
                               return
                           
# Basically the same as download games, but do it by tournament ID
def download_games_for_tournament(tournamentID):
    start_time = time.time()

    # delete all games from previous tournament
    print("Removing data from previous tournament...")
    if os.path.exists("data/games"):
        shutil.rmtree("data/games")
    print("\nData removed successfully.")

    tournament = get_tournament(tournamentID)
    with open("data/esports-data/mapping_data.json", "r") as json_file:
       mappings_data = json.load(json_file)

    # make games directory again
    directory = "games"
    if not os.path.exists("data/games"):
        os.makedirs("data/games")

    mappings = {
        esports_game["esportsGameId"]: esports_game for esports_game in mappings_data
    }

    game_counter = 0

    tournament_name = tournament["name"]

    print(f"\nWriting tournament {tournament_name} game files...\n")

    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                for game in match["games"]:
                    if game["state"] == "completed":
                        try:
                            platform_game_id = mappings[game["id"]]["platformGameId"]
                        except KeyError:
                            print(f"{platform_game_id} {game['id']} not found in the mapping table")
                            continue

                        download_gzip_and_write_to_json(f"{directory}/{platform_game_id}")
                        game_counter += 1

                        if game_counter % 10 == 0:
                            print(
                                f"----- Processed {game_counter} games, current run time: \
                                {round((time.time() - start_time)/60, 2)} minutes"
                            )

    print(
          f"----- Processed {game_counter} games total, in: {round((time.time() - start_time)/60, 2)} minutes"
         )
            

# DOWNLOADS 61 GAMES approximately 6 GB of data.
if __name__ == "__main__":
   download_esports_files()
   download_games_for_tournament("110733838935136200")