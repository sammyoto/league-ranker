# data-scripts
Most files in this folder hold functions that help get and manipulate data from the 
[Global Power Rankings Hackathon](https://lolglobalpowerrankings.devpost.com/?ref_feature=challenge&ref_medium=your-open-hackathons&ref_content=Submissions+open) s3 bucket.

**get_data.py** 
- holds functions that retreive data from the s3 bucket.

**data_helper_functions.py** 
- holds functions that retreive already downloaded data.

**create_feature_vectors.py** 
- holds functions that can access already downloaded data by tournament_id and format desired features into a list.

**training_functions.py** 
- holds functions that finalize features and saves them to a csv.

**weighter.py** 
- is a class that takes in test and training data and inputs them into an SVM. It saves the SVM weights to a json file **weights.json**.

**train_model.ipynb** 
- contains the code and experiments associated with training a **weighter** on previously saved features.

**add_final_features.ipynb** 
- adds metadata features such as team_ids and tournament_ids to existing feature vectors and saves them to a new csv.

**create_rankings.ipynb** 
- contains the code and experiments associated with creating rankings and saving them to json files.

**2023_vectors** 
- holds the feature vectors created off of league of legends e sports data for tournaments in 2023 saved in csv format.
