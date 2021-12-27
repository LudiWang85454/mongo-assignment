from typing import *

import json
import pymongo


class Team:
        """Docstring"""
        
        def __init__(self, team_number: int, num_balls: int, climbed: bool):
                self.team_number = team_number
                self.balls_scored: List[int] = [num_balls]
                self.successful_climbs = 0 + climbed
                self.n_matches = 1
                
        def update(self, balls_scored: int, climb_success: bool):
                self.n_matches += 1     # Assumes that a team doesn't play in one match more than once (Doesn't make sense)
                self.successful_climbs += climb_success
                self.balls_scored.append(balls_scored)
        
        @property
        def average_balls_scored(self):
                return sum(self.balls_scored)/len(self.balls_scored)
        
        @property
        def least_balls_scored(self):
                return min(self.balls_scored)
        
        @property
        def most_balls_scored(self):
                return max(self.balls_scored)
        
        @property
        def avg_climb_success(self):
                return self.successful_climbs/self.n_matches
        
teams = {}

for entry in json.load("example_tim_data.json"):
        if entry["team_num"] in teams:
                teams[entry["team_num"]].update(entry["num_balls"], entry["climbed"])
        else:
                teams[entry["team_num"]] = Team(entry["team_num"])

client = pymongo.MongoClient("mongodb://localhost:27017/")      # Assumes default MongoDB, not specified in instructions
db = client["mongo-assignment"] # Assumes random database name, none specified in instructions
collection = db["mongo-assignment"]     # Assumes random collection name, none specified in instructions

requests = [InsertOne(
        {
                "team_number": i.team_number,
                "average_balls_scored": i.average_balls_scored,
                "least_balls_scored": i.least_balls_scored,
                "most_balls_scored": i.most_balls_scored,
                "matches_played": i.n_matches,
                "percent_climb_success": i.average_climb_success
        }
) for i in teams]
collection.bulk_write(requests)
