# Part 3: Difference Between First and Last Score

class StudentPerformance:
    def __init__(self, scores):
        self.scores = scores

    def score_difference(self):
        try:
            if len(self.scores) == 0:
                raise ValueError
            diff = self.scores[-1] - self.scores[0]
            print("Difference between last and first score is:", diff)
        except (ValueError, IndexError):
            print("No scores available to calculate difference")


# Test
scores = [55, 65, 75, 85]
s = StudentPerformance(scores)
s.score_difference()

# Edge case: empty list
s2 = StudentPerformance([])
s2.score_difference()
