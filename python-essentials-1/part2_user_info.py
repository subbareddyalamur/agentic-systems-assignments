# Part 2: User Information and String Concatenation

first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
age_input = input("Enter your age: ")

try:
    age = int(age_input)

    if age < 0:
        print("Age cannot be negative")
    else:
        print("Full Name: " + first_name + " " + last_name)
        print("You will be " + str(age + 1) + " next year")

except ValueError:
    print("Invalid age input")
