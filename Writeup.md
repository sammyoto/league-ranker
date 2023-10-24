# Accessing the Data

While working through this project we used multiple tools to help in creating a rankings system for League of Legends Esports teams. 
Figuring out which pieces of data we needed, how to get it efficiently and effectively, and cleaning the data took the majority of the time. 
For accessing the data from the s3 bucket, we built a small library of functions to help make accessing and manipulating the data easier and more efficient. 
We didn’t have the means to download and store all of the game data for 2023, so we had to download in batches, process each batch one at a time, delete the data batch, then rinse and repeat. 

Processing on each batch followed these processes:
- Download each game for a tournament
- Create a vector of necessary game data for each player in the game
- Add these vectors to a dataframe
- Repeat for every tournament

After all the processing was complete, we saved the dataframe to a CSV file for easy access to the data in the future. The vector of game data for each player was comprised of the following features:

```
["level", "shutdownValue", "totalGold", "MINIONS_KILLED", "NEUTRAL_MINIONS_KILLED",
"NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE", "NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE",
"CHAMPIONS_KILLED", "NUM_DEATHS", "ASSISTS", "WARD_PLACED", "WARD_KILLED", "VISION_SCORE",
"TOTAL_DAMAGE_DEALT", "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", "TOTAL_DAMAGE_TAKEN",
"TOTAL_DAMAGE_SELF_MITIGATED", "TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES", "TOTAL_DAMAGE_DEALT_TO_BUILDINGS",
"TOTAL_DAMAGE_DEALT_TO_TURRETS", "TOTAL_DAMAGE_DEALT_TO_OBJECTIVES",
"TOTAL_TIME_CROWD_CONTROL_DEALT_TO_CHAMPIONS", "TOTAL_HEAL_ON_TEAMMATES","RESULT"]
```

The feature values were taken at the end of each match along with the outcome of the match.

# Training the Model and Calculating Performance Scores

Our ranking system is based on one Support Vector Machine (SVM), which was trained on the data we processed. 
Essentially, the SVM learns how to classify a performance between a win and a loss. For example, the SVM learned to associate a high number of assists with a game win. 
And on the flipside, a high number of deaths was correlated with a game loss. The SVM was trained to classify a performance correctly with 90% accuracy. 
The number of assists was the most critical component in the SVM’s decision on who would be the victor of a match.

The ability to classify between a win and a loss is great. However, since we already know the outcome of each game, this alone is not enough to justify using it to rank teams. 
The magic of the model comes from using the weights the SVM learned to give each player a score for their performance in a game. 
We were introduced to this concept in a research paper we found, *Pappalardo, Luca, et al. "PlayeRank: Data-Driven Performance Evaluation and Player Ranking in Soccer via a Machine Learning Approach." ACM Transactions on Intelligent Systems and Technology, vol. 10, no. 5, 2019, article 59*. 
In the paper, the authors propose a framework for ranking soccer teams using features from game data, having an SVM learn to classify between a win and a loss, and using the SVM’s learned weights to assign a player a performance score for a given game. 
The paper goes into more detail on classifying players by their position and updating scores with every new game added to a database. But for our purposes, knowing how to rank players and rank teams was all we needed to discover.

Assigning a player a performance score for a game is quite simple. We take their vector of game data and multiply it element wise with the SVM’s learned weights for each feature.
For example, our SVM’s weights for NUM_DEATHS and ASSISTS are as follows:

```
{"NUM_DEATHS": -0.30217788760492076, "ASSISTS": 0.45300663359040183}
```

The calculation would simply involve multiplying the player’s number of deaths for that game with the weight for NUM_DEATHS, doing the same for ASSISTS, and then adding them together to get a performance score. 
If you do this for all of the features  and their weights you get a performance score for the whole game.
Creating a team’s performance score for a given game is even more simple. For each player on the team, sum their performance score for the game to get the team’s performance score for the game.

The following graph shows a sample calculation for a given game using only features NUM_DEATHS and ASSISTS for simplicity.

![SVM_flow](https://github.com/sammyoto/league-ranker/assets/67492097/ded08bdc-09a9-43a3-8b57-a9de25f817fe)

With this, as long as we have the features for each player in a game, we can create a performance score for each team that takes into account factors that normally can’t be computed manually.

# Ranking Teams
Ranking teams using our model is very straightforward. The teams are ranked based on average performance score. The higher the performance score, the higher your rank. Our API knows this and ranks teams according to their average performance score.
A sample API response for global rankings is shown below:
```
[
  {
    "team_id": "107581765633427097",
    "team_name": "Fuego",
    "team_code": "FUE",
    "power_score": 25.591098274766477,
    "rank": 1
  },
  {
    "team_id": "106827844148688268",
    "team_name": "SG Academy",
    "team_code": "SG",
    "power_score": 23.179425562870446,
    "rank": 2
  },
  {
    "team_id": "106827832203113865",
    "team_name": "SHG Academy",
    "team_code": "SHG",
    "power_score": 22.957386627289846,
    "rank": 3
  },
  {
    "team_id": "99566404852189289",
    "team_name": "Beijing JDG Intel Esports Club",
    "team_code": "JDG",
    "power_score": 21.225856147863784,
    "rank": 4
  },
  {
    "team_id": "98767991926151025",
    "team_name": "G2 Esports",
    "team_code": "G2",
    "power_score": 21.085196729278085,
    "rank": 5
  }
]
```
A team’s rank is based solely off of their power_score (same as average performance score) and nothing else. 
Accessing different endpoints of the API, such as tournaments, will provide rankings for a given tournament and only average the performance score of the games in the tournament.

# AWS Tools
The main tool we used to build this project on AWS was API Gateway integrated with AWS Lambda. Our API handles all incoming requests with one Lambda function that parses the HTTP endpoint and any query parameters in the URL, then responds to the request accordingly. 
In the beginning of the project, we tried using AWS Sagemaker and AWS Data Wrangler to process the data, however despite having a $100 AWS credit the cost of Sagemaker and Data Wrangler quickly became too much for two college students to handle. 
We decided it was best to work with the data locally and host a working model on AWS after it was already complete in order to minimize the cost of our project.

# Findings, Learnings, and Recognizing Issues With Our Model

## Findings
Through building this project, our key finding in the data was that Assists are the highest correlated feature with winning in professional League of Legends. 
We are both casual League of Legends players, so this was a shock to us, as we both never want to play with our teams in our own ranked games. In the professional scene however, it makes sense that assists are the most important factor in deciding who wins a game. 
Professional games are often played so controlled and intelligently, it is very difficult for any one team to gain a significant lead over another team. 
Solo kills happen much less often than in solo queue, players die much less often, and players are all extremely good at taking advantage of resources around the map like minions, jungle camps, and objectives. 
Due to professionals being so principled at the game, if laners stayed in their lanes and farmed perfectly and played perfectly the entire game (which they often do), gold and player power level would be almost dead-even the entire game. 
However, if teams play together, play towards objectives, gank often, and press their advantages together, they will be much more likely to gain a lead over the enemy team. This is why Assists have so much weight in determining who wins a match. 
Not only do Assists give the killing team an extra 50% of the bounty in gold split among assistants, they can also translate into huge advantages for the killing team. 
For example, if a jungler ganks bot lane and assists the bot lane in killing the enemy ADC, the jungler, ADC, and support are now 3 versus 1 against the enemy support. 
This can easily translate into a turret plating, uncontested dragon kill, a good base for bot lane, and many other advantages that come from a single kill. This is why assists are so important. 
Teams that play as a team and play together can press advantages much easier than a team that is uncoordinated and doesn’t play together.

## Learnings
Aside from findings from the League of Legends data, we learned a lot about real world data science and applying it to solve a problem. The biggest takeaway for us was that data is not always clean. 
There were countless times where we thought we had the right algorithm to access the data and get all of the different features we needed from all of the necessary files, but then there would be some sort of error.
We would re-read our code and be stumped for hours on why it wasn’t working, but always eventually come to the conclusion that there was some piece of information missing in one of the files.
Due to this, we learned that we should implement error checking while writing our methods so that we can solve our issues with the data easily and quickly. 
Another problem with incomplete data is that it can skew the accuracy of a machine learning model. For example, there would often be mapping data that didn’t have all 10 participants for a given game. 
If we let the model learn on this data it could have skewed the model and made it less accurate as missing participants could have had vital data that was important for the model to see.
We were often told in university machine learning and data science courses that a machine learning engineer or data scientist spends 80% of their time analyzing and cleaning data.
This project proved that notion to us and showed us what it is like to work with big data, specifically S3 buckets.

## Recognizing Issues
Our model takes a strictly data-driven approach to solving the ranking problem for League of Legends Esports. The better a team’s performance over all of their games, the higher their ranking.
This seems like it would produce the desired outcome on paper, however our rankings don’t exactly reflect the current state of League of Legends Esports. 
There are many different factors that our model does not take into account, such as the difference in skill levels between leagues, the difficulty of any given matchup, and the actual number of games played. 
Our model assumes all matches are of equal weight, even though a world final should have more impact on a ranking than a normal LoL game. We recognize these issues, and had we had more time, we would have liked to implement solutions to address these problems.
