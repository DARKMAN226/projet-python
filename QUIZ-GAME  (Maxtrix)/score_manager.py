import json

class ScoreManager:
    def __init__(self):
        self.scores_file = "data/scores.json"
        self.scores_data = self.load_scores()
    
    def load_scores(self):
        try:
            with open(self.scores_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": {}}
    
    def save_scores(self):
        with open(self.scores_file, "w") as f:
            json.dump(self.scores_data, f, indent=4)