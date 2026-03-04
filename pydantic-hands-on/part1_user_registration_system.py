# Part 1: User Registration System for E-Commerce Platform

from pydantic import BaseModel, EmailStr, Field, ValidationError, ConfigDict
from typing import Optional


class Address(BaseModel):
    city: str = Field(min_length=3)
    pincode: str = Field(pattern=r"^\d{6}$")


class User(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    user_id: int
    name: str
    email: EmailStr
    age: int = Field(ge=18)
    address: Address
    is_premium: Optional[bool] = False


# --- Test 1: Valid user ---
print("--- Valid User ---")
try:
    user = User(
        user_id=1,
        name="John Doe",
        email="john@example.com",
        age=25,
        address={"city": "Mumbai", "pincode": "400001"},
    )
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"City: {user.address.city}")
    print(f"Pincode: {user.address.pincode}")
    print(f"Premium: {user.is_premium}")
except ValidationError as e:
    print(e)

# --- Test 2: Invalid pincode ---
print("\n--- Invalid Pincode ---")
try:
    user = User(
        user_id=2,
        name="Jane Doe",
        email="jane@example.com",
        age=22,
        address={"city": "Delhi", "pincode": "12AB"},
    )
except ValidationError as e:
    print(e)

# --- Test 3: Underage user ---
print("\n--- Underage User ---")
try:
    user = User(
        user_id=3,
        name="Young User",
        email="young@example.com",
        age=15,
        address={"city": "Chennai", "pincode": "600001"},
    )
except ValidationError as e:
    print(e)

# --- Test 4: City name too short ---
print("\n--- City Too Short ---")
try:
    user = User(
        user_id=4,
        name="Test User",
        email="test@example.com",
        age=30,
        address={"city": "NY", "pincode": "100001"},
    )
except ValidationError as e:
    print(e)

# --- Test 5: Assignment validation ---
print("\n--- Assignment Validation (changing age to invalid) ---")
try:
    user = User(
        user_id=5,
        name="Valid User",
        email="valid@example.com",
        age=20,
        address={"city": "Bangalore", "pincode": "560001"},
    )
    print(f"Age before: {user.age}")
    user.age = 10  # Should fail due to validate_assignment
except ValidationError as e:
    print(e)
