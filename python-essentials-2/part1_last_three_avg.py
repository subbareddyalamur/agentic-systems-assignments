# Part 1: Last Three Average

class StudentMarks:
    def __init__(self, marks):
        self.marks = marks

    def last_three_avg(self):
        try:
            if len(self.marks) < 3:
                raise ValueError
            last_three = self.marks[-3:]
            avg = sum(last_three) / 3
            print("Average of last 3 marks is:", avg)
        except (ValueError, IndexError):
            print("Not enough marks to calculate average")


# Test
marks = [50, 60, 70, 80, 90]
s = StudentMarks(marks)
s.last_three_avg()

# Edge case: less than 3 marks
s2 = StudentMarks([50])
s2.last_three_avg()
