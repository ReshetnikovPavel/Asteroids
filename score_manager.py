import shelve


class BestScore:
    def __init__(self):
        with shelve.open("score.txt") as f:
            if "score" not in f:
                f["score"] = 0
            self.value = f["score"]

    def update_score(self, value):
        if value > self.value:
            self.value = value
            with shelve.open("score.txt") as f:
                f["score"] = value
