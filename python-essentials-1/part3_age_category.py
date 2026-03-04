# Part 3: Age Category and Eligibility Checker

name = input("Enter your name: ")
age_input = input("Enter your age: ")

try:
    age = int(age_input)

    if age < 0:
        print("Age cannot be negative")
    else:
        print("Hello " + name)

        if age < 13:
            print("You are a Child")
        elif age <= 17:
            print("You are a Teenager")
        elif age <= 59:
            print("You are an Adult")
        else:
            print("You are a Senior Citizen")

        if age >= 18:
            print("You are eligible to vote")
        else:
            print("You are not eligible to vote")

except ValueError:
    print("Invalid age input")
