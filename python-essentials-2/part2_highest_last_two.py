# Part 2: Highest of Last Two Scores

class StudentScores:
    def __init__(self, scores):
        self.scores = scores

    def highest_last_two(self):
        try:
            if len(self.scores) < 2:
                raise ValueError
            highest = max(self.scores[-1], self.scores[-2])
            print("Highest score among last two is:", highest)
        except (ValueError, IndexError):
            print("Not enough scores to find highest value")


# Test
scores = [45, 67, 89, 72]
s = StudentScores(scores)
s.highest_last_two()

# Edge case: less than 2 scores
s2 = StudentScores([45])
s2.highest_last_two()
