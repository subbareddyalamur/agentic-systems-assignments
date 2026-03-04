# Part 1: User Registration Validation using Pydantic

from pydantic import BaseModel, EmailStr, Field, ValidationError


class UserRegister(BaseModel):
    username: str = Field(min_length=5)
    email: EmailStr
    age: int = Field(ge=18)


# Test with valid data
print("--- Valid Input ---")
try:
    user = UserRegister(username="johndoe", email="john@example.com", age=25)
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Age: {user.age}")
except ValidationError as e:
    print(e)

# Test with short username
print("\n--- Invalid Username (too short) ---")
try:
    user = UserRegister(username="joe", email="joe@example.com", age=20)
except ValidationError as e:
    print(e)

# Test with invalid email
print("\n--- Invalid Email ---")
try:
    user = UserRegister(username="janedoe", email="not-an-email", age=22)
except ValidationError as e:
    print(e)

# Test with underage
print("\n--- Invalid Age (under 18) ---")
try:
    user = UserRegister(username="younguser", email="young@example.com", age=15)
except ValidationError as e:
    print(e)
