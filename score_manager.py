import shelve


class BestScore:
    def __init__(self):
        with shelve.open("score.txt") as f:
            if "best_score" not in f:
                f["best_score"] = 0
            if "score_list" not in f:
                f["score_list"] = []
            self.value = f["best_score"]
            self.scores = f["score_list"]

    def update_score(self, value, player_name):
        with shelve.open("score.txt") as f:
            if value > self.value:
                self.value = value
                f["best_score"] = value
            self.scores.append((player_name, value))
            f["score_list"] = self.scores
