# league-ranker
A work in progress solution for ranking teams in League of Legends esports. Made for submission to Global Power Rankings Hackathon 2023.

[See API here](https://kzap4edi6h.execute-api.us-west-2.amazonaws.com/global_rankings)

Method used based on paper: Pappalardo, Luca, et al. "PlayeRank: Data-Driven Performance Evaluation and Player Ranking in Soccer via a Machine Learning Approach." ACM Transactions on Intelligent Systems and Technology, vol. 10, no. 5, 2019, article 59

[See their github here](https://github.com/mesosbrodleto/playerank)

Frontend currently not functional. For details on implementation please read Readme located in data_scripts folder.

Sample Ranking:

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

