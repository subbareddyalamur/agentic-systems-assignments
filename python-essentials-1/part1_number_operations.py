# Part 1: Number Operations with Error Handling

try:
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    print("Sum:", num1 + num2)

    if num2 == 0:
        print("Cannot divide by zero")
    else:
        print("Division:", num1 / num2)

except ValueError:
    print("Invalid input")
